"""
This module is for your data cleaning.
It should be repeatable.
## PRECLEANING
There should be a separate script recording how you transformed the json api calls into a dataframe and csv.
"""
import pandas as pd
import api_pull

def remove_extra_columns_house(dirty_data_senate, dirty_data_house)
    common_cols = []
    house_cols = list(dirty_data_house.columns)
    senate_cols = list(dirty_data_senate.columns)
    for column in house_cols:
        if column in senate_cols:
            common_cols.append(column)
    drop_these = list(set(house_cols) - set(common_cols))
    dirty_data_house_2 = dirty_data_house.drop(drop_these, axis = 1)
    return dirty_data_house_2

def merge_chambers(dirty_data_senate, dirty_data_house_2):
    common_cols = []
    house_cols = list(dirty_data_house_2.columns)
    senate_cols = list(dirty_data_senate.columns)
    for column in senate_cols:
        if column in house_cols:
            common_cols.append(column)
    dirty_data_house_2_1 = dirty_data_house_2[common_cols]
    return pd.concat([dirty_data_senate, dirty_data_house_2_1], join = 'outer')

def full_clean():
    """
    This is the one function called that will run all the support functions.
    Assumption: Your data will be saved in a data folder and named "dirty_data.csv"

    :return: cleaned dataset to be passed to hypothesis testing and visualization modules.
    """
    dirty_data_senate = pd.read_csv("./data/dirty_data_senate.csv")
    dirty_data_house = pd.read_csv("./data/dirty_data_house.csv")
    dirty_data_house_2 = remove_extra_columns_house(dirty_data_senate, dirty_data_house)
    cleaning_data_3 = merge_chambers(dirty_data_senate, dirty_data_house_2) 

    cleaning_data1 = support_function_one(dirty_data)
    cleaning_data2 = support_function_two(cleaning_data1)
    cleaned_data= support_function_three(cleaning_data2)
    cleaned_data.to_csv('./data/cleaned_for_testing.csv')
    
    return cleaned_data