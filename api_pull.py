import pandas as pd
import numpy as np
import pprint as p
import itertools
import keys
import requests
import json
api_key = keys.get_key()

def get_json(congress,chamber):
    # construct url
    api_key = keys.get_key()
    headers = {'X-API-Key': api_key}
    url = "https://api.propublica.org/congress/v1/{congress}/{chamber}/members.json".format(congress=congress,chamber=chamber)
#     print(url)
    # Make request
    r = requests.get(url=url, headers=headers)
    return r

def get_all_members(start=102,end=115,chamber='senate',verbose=False):
    import pandas as pd

    # change this to default to 'both'; check that data is same
    df_list = []
    # set min congress values
    if chamber == 'house':
        if start < 102:
            start = 102
    elif chamber == 'senate':
        if start < 80:
            start = 80
    else:
        print('please select chamber')
        return none
    # set max congress value - 115 for both chambers
    if end > 115:
        end = 115
    
    # get memeber list for each congress-chamber
    for congress in range(start,end+1):
        if verbose:
            print("...downloading {chamber} member list for congress {congress}...".format(chamber=chamber,congress=congress))
        r = get_json(congress = congress, chamber = chamber)
#         dict_list.append(r.json()['results'][0])
        df_list.append(
            pd.DataFrame(
                r.json()['results'][0]['members']
            )
        )
        df_list[len(df_list)-1]['chamber'] = chamber
        df_list[len(df_list)-1]['congress'] = congress
    full_df = pd.concat(df_list)
    full_df.reset_index(drop=True,inplace=True)
    path = "data/dirty_data_{}_members.csv".format(chamber)
    full_df.to_csv(path,index=False)
#     return full_df

def get_json_from_url(url):
    api_key = keys.get_key()
    headers = {'X-API-Key': api_key}
    r = requests.get(url=url, headers=headers)
    return r.content

def list_times_senate_house():
    senate_years = []
    for i in range(1947, 2019):
        senate_years.append(str(i))

    house_years = []
    for i in range(1993,2019):
        house_years.append(str(i))

    months = ["01", "02", "03", "04", "05",
              "06", "07", "08", "09", "10", "11", "12"]

    house_list_times = list(itertools.product(house_years, months))   
    senate_list_times = list(itertools.product(senate_years, months))
    for i in list(range(0, 8)):
        senate_list_times.append(["2019", months[i]])
        house_list_times.append(["2019", months[i]])
    return senate_list_times,house_list_times

def get_vote_data():
    vote_list_senate = []
    vote_list_house = []
    chambers = ['senate', 'house']
    for i in [0, 1]:
        chamber = chambers[i]
        if chamber == 'senate':
            _,time = list_times_senate_house()
        else:
            time,_ = list_times_senate_house()
        for i in time:
            year = i[0]
            month = i[1]
            url = f"https://api.propublica.org/congress/v1/{chamber}/votes/{year}/{month}.json"
            print(url)
            responses = json.loads(get_json_from_url(url))
            bill = responses['results']['votes']
            bill_rang = list(range(0, len(bill)))
            for i in bill_rang:
                vote = {}
                for key, value in bill[i].items():
                    if key == 'bill' or key == 'democratic' or key == 'republican' or key == 'independent' or key == 'total':
                        for key1, value1 in value.items():
                            vote.update({f"{key} {key1}": value1})
                    else:
                        vote.update({key: value})
                if chamber == 'senate':
                    vote_list_senate.append(dict(vote))
                else:
                    vote_list_house.append(dict(vote))

    df_s_bills = pd.DataFrame(vote_list_senate)
    df_s_bills['chamber'] = 'senate'
    path_s = "data/dirty_data_senate.csv"
    df_s_bills.to_csv(path_s,index=False)

    df_h_bills = pd.DataFrame(vote_list_house)
    df_h_bills['chamber'] = 'house'
    path_h = "data/dirty_data_house.csv"
    df_h_bills.to_csv(path_h,index=False)