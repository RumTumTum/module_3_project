"""List of used functions"""

import statistics
import itertools
import json
import pandas as pd
import numpy as np
import requests
import keys


def get_json_from_url(url):
    """Returns content from ProPublica url"""
    api_key = keys.get_key()
    headers = {'X-API-Key': api_key}
    r_val = requests.get(url=url, headers=headers)
    return r_val.content


def list_times_congress():
    """Öbtains months and years for data scrape"""
    congress_years = []
    for i in range(1993, 2019):
        congress_years.append(str(i))
    months = ["01", "02", "03", "04", "05",
              "06", "07", "08", "09", "10", "11", "12"]
    congress_list_times = list(itertools.product(congress_years,
                                                 months))
    for i in list(range(0, 8)):
        congress_list_times.append(["2019", months[i]])
    return congress_list_times


def get_vote_data_senate():
    """Pulls and exports data from senate"""
    vote_list_senate = []
    time = list_times_congress()
    for j in time:
        year = j[0]
        month = j[1]
        url = f"https://api.propublica.org/congress/v1/senate"\
              f"/votes/{year}/{month}.json"
        print(url)
        responses = json.loads(get_json_from_url(url))
        bill = responses['results']['votes']
        for i in list(range(0, len(bill))):
            vote = {}
            for key, value in bill[i].items():
                if key in ['bill', 'democratic', 'republican',
                           'independent', 'total']:
                    for key1, value1 in value.items():
                        vote.update({f"{key}_{key1}": value1})
                else:
                    vote.update({key: value})
            vote_list_senate.append(dict(vote))
    df_s_bills = pd.DataFrame(vote_list_senate)
    df_s_bills['chamber'] = 'senate'
    df_s_bills.to_csv("data/dirty_data_senate.csv", index=False)


def get_vote_data_house():
    """Pulls and exports data from house"""
    vote_list_house = []
    time = list_times_congress()
    for j in time:
        year = j[0]
        month = j[1]
        url = f"https://api.propublica.org/congress/v1/house"\
              f"/votes/{year}/{month}.json"
        print(url)
        responses = json.loads(get_json_from_url(url))
        bill = responses['results']['votes']
        for i in list(range(0, len(bill))):
            vote = {}
            for key, value in bill[i].items():
                if key in ['bill', 'democratic', 'republican',
                           'independent', 'total']:
                    for key1, value1 in value.items():
                        vote.update({f"{key}_{key1}": value1})
                else:
                    vote.update({key: value})
            vote_list_house.append(dict(vote))

    df_h_bills = pd.DataFrame(vote_list_house)
    df_h_bills['chamber'] = 'house'
    df_h_bills.to_csv("data/dirty_data_house.csv", index=False)


def collect_sample_means_party(data, n_val=500):
    """Collects samples from parties"""
    dem_means = []
    rep_means = []
    i = 0
    while i <= n_val:
        dem_absent_sample = np.random.choice(data.
                                             percentage_nonvoting_democratic,
                                             size=30)
        dem_mean = (dem_absent_sample).mean()
        dem_means.append(dem_mean)
        rep_absent_sample = np.random.choice(data.
                                             percentage_nonvoting_republican,
                                             size=30)
        rep_mean = (rep_absent_sample).mean()
        rep_means.append(rep_mean)
        i += 1
    return [rep_means, dem_means]


def collect_sample_means_chamber(data, n_val=500):
    """Collects samples from chambers"""
    senate_data = data.loc[data.chamber == "senate"]
    house_data = data.loc[data.chamber == "house"]
    house_means = []
    senate_means = []
    i = 0
    while i <= n_val:
        senate_absent_sample = np.random.choice(senate_data.
                                                percentage_nonvoting_total,
                                                size=30)
        senate_mean = (senate_absent_sample).mean()
        senate_means.append(senate_mean)
        house_absent_sample = np.random.choice(house_data.
                                               percentage_nonvoting_total,
                                               size=30)
        house_mean = (house_absent_sample).mean()
        house_means.append(house_mean)
        i += 1
    return [senate_means, house_means]


def cohen_d(group1, group2):
    """Returns Cohen's D level"""
    group1_mean = statistics.mean(group1)
    group2_mean = statistics.mean(group2)
    diff = group1_mean - group2_mean
    n_1 = len(group1)
    n_2 = len(group2)
    var1 = statistics.variance(group1)
    var2 = statistics.variance(group2)
    pooled_var = (n_1 * var1 + n_2 * var2) / (n_1 + n_2)
    d_val = diff / np.sqrt(pooled_var)
    return d_val


def percent_yay(df_data):
    """Obtains yay percentanges"""
    parties = ['democratic', 'republican']
    return[
        df_data['{party}_yes'.format(party=party)].sum() /
        (df_data['{party}_yes'.format(party=party)].sum() +
         df_data['{party}_not_voting'.format(party=party)].sum() +
         df_data['{party}_no'.format(party=party)].sum())
        for party in parties]


def sample_percent_yays(df_data, n_val=1000,
                        replace=False, random_state=12345):
    """Obtains sample yay percentanges"""
    df_data = df_data.copy()
    parties = ['democratic', 'republican']
    df_sample = df_data.sample(n=n_val,
                               replace=replace, random_state=random_state)
    for party in parties:
        df_sample['{party}_percentage_yes'.format(party=party)] = (
            df_sample['{party}_yes'.format(party=party)] /
            (df_sample['{party}_yes'.format(party=party)] +
             df_sample['{party}_not_voting'.format(party=party)] +
             df_sample['{party}_no'.format(party=party)]))
    democratic_percent_yes = list(df_sample['democratic_percentage_yes'])
    republican_percent_yes = list(df_sample['republican_percentage_yes'])
    return republican_percent_yes, democratic_percent_yes


def sample_of_means_percent_yay(df_data, n_val=1000, size=20):
    """Obtains a sample of percent_yay means"""
    df_data = df_data.copy()
    set_1 = []
    set_2 = []
    for i in list(range(0, n_val)):
        df_sample = df_data.sample(n=size, replace=False, random_state=i+1)
        paired_sample = percent_yay(df_sample)
        set_1.append(paired_sample[0])
        set_2.append(paired_sample[1])
    return set_1, set_2
