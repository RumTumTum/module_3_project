# Pull data from API
import keys
import requests
import numpy as np
import statistics

def request(url):
    api_key = keys.get_key()
    headers = {'X-API-Key': api_key}
    r = requests.get(url=url, headers=headers)
    return r.content

# Collects samples from parties
def collect_sample_means_party(data, n=500):
    dem_means = []
    rep_means = []
    for i in list(range(0,n)):
        dem_absent_sample = np.random.choice(data.percentage_nonvoting_democratic, size=30)
        dem_mean = (dem_absent_sample).mean()
        dem_means.append(dem_mean)
        rep_absent_sample = np.random.choice(data.percentage_nonvoting_republican, size=30)
        rep_mean = (rep_absent_sample).mean()
        rep_means.append(rep_mean)
    return [rep_means, dem_means]

# Collects samples from chambers
def collect_sample_means_chamber(data, n=500):
    senate_data = data.loc[data.chamber == "senate"]
    house_data = data.loc[data.chamber == "house"]
    house_means = []
    senate_means = []
    for i in list(range(0,n)):
        senate_absent_sample = np.random.choice(senate_data.percentage_nonvoting_total, size=30)
        senate_mean = (senate_absent_sample).mean()
        senate_means.append(senate_mean)
        house_absent_sample = np.random.choice(house_data.percentage_nonvoting_total, size=30)
        house_mean = (house_absent_sample).mean()
        house_means.append(house_mean)
    return [senate_means, house_means]

# Collects samples from both parties in both chambers
def collect_sample_means_chamber_party(data, n=500):
    senate_data = data.loc[data.chamber == "senate"]
    house_data = data.loc[data.chamber == "house"]
    dem_sen_means = []
    dem_house_means = []
    rep_sen_means = []
    rep_house_means = []
    senate_means = collect_sample_means_party(senate_data, n=30)
    house_means = collect_sample_means_party(house_data, n=30)
    rep_sen_means = senate_means[0]
    dem_sen_means = senate_means[1]
    rep_house_means = house_means[0]
    dem_house_means = house_means[1]
    return [rep_sen_means, dem_sen_means, rep_house_means, dem_house_means]

def cohen_d(group1, group2):
    group1_mean = statistics.mean(group1)
    group2_mean = statistics.mean(group2)
    diff = group1_mean - group2_mean
    n1 = len(group1)
    n2 = len(group2)
    var1 = statistics.variance(group1)
    var2 = statistics.variance(group2)
    pooled_var = (n1 * var1 + n2 * var2) / (n1 + n2)
    d = diff / np.sqrt(pooled_var)
    return d