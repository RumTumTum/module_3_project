import pandas as pd
import requests
import json
import keys
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
