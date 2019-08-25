"""Import necessary functions"""
import pandas as pd


def remove_extra_columns_house(dirty_data_senate, dirty_data_house):
    """Drops extra columns from House data"""
    common_cols = []
    house_cols = list(dirty_data_house.columns)
    senate_cols = list(dirty_data_senate.columns)
    for column in house_cols:
        if column in senate_cols:
            common_cols.append(column)
    drop_these = list(set(house_cols) - set(common_cols))
    return dirty_data_house.drop(drop_these, axis=1)


def merge_chambers(dirty_data_senate, dirty_data_house_2):
    """Merges Senate and House data"""
    common_cols = []
    house_cols = list(dirty_data_house_2.columns)
    senate_cols = list(dirty_data_senate.columns)
    for column in senate_cols:
        if column in house_cols:
            common_cols.append(column)
    dirty_data_house_2_1 = dirty_data_house_2[common_cols]
    return pd.concat([dirty_data_senate, dirty_data_house_2_1], join='outer')


def drop_unnecessary_columns(data):
    """Drops unnecessary columns"""
    drop_columns = ["bill api_uri", "bill bill_id", "bill latest_action",
                    "bill number", "bill sponsor_id",
                    "bill title", "document_number", "document_title",
                    "question_text", "url", "vote_uri"]
    return data.drop(drop_columns, axis=1)


def convert_to_datetime(data):
    """Changes date to datetime"""
    data["datetime"] = data.date.map(lambda x:
                                     pd.to_datetime(x[:10],
                                                    format='%Y/%m/%d'))
    return data.drop('date', axis=1)


def fill_null_object(data):
    """Changes null values to string"""
    data["democratic majority_position"] = \
        data["democratic majority_position"].fillna("Null")
    data["description"] = data["description"].fillna("Null")
    data["question"] = data["question"].fillna("Null")
    data["republican majority_position"] = \
        data["republican majority_position"].fillna("Null")
    data["tie_breaker"] = data["tie_breaker"].fillna("Null")
    data["tie_breaker_vote"] = data["tie_breaker_vote"].fillna("Null")
    return data


def lowercase_object(data):
    """Changes string variables to lower case"""
    data["chamber"] = data["chamber"].map(lambda x: x.lower())
    data["democratic majority_position"] = \
        data["democratic majority_position"].map(lambda x: x.lower())
    data["description"] = data["description"].map(lambda x: x.lower())
    data["question"] = data["question"].map(lambda x: x.lower())
    data["republican majority_position"] = \
        data["republican majority_position"].map(lambda x: x.lower())
    data["result"] = data["result"].map(lambda x: x.lower())
    data["source"] = data["source"].map(lambda x: x.lower())
    data["tie_breaker"] = data["tie_breaker"].map(lambda x: x.lower())
    data["tie_breaker_vote"] = data["tie_breaker_vote"].map(lambda x:
                                                            x.lower())
    return data


def remove_nulls(data):
    """Removes rows with blank voting data"""
    return data.loc[data['democratic no'].notnull()]


def fix_total(data):
    """Cleans the 'Democratic present' column"""
    data['democratic_present'] = data.apply(lambda row: row['democratic no']
                                            + row['democratic not_voting']
                                            + row['democratic yes'], axis=1)
    return data


def fix_total2(data):
    """Cleans the 'Republican present' column"""
    data['republican_present'] = data.apply(lambda row: row['republican no']
                                            + row['republican not_voting']
                                            + row['republican yes'], axis=1)
    return data


def fix_total3(data):
    """Cleans the 'independent present' column"""
    data['independent_present'] = data.apply(lambda row: row['independent no']
                                             + row['independent not_voting']
                                             + row['independent yes'], axis=1)
    return data


def fix_total4(data):
    """Cleans the 'total present' column"""
    data['total_present'] = data.apply(lambda row: row['democratic_present']
                                       + row['republican_present']
                                       + row['independent_present'], axis=1)
    return data


def fix_total5(data):
    """Cleans the 'total no' column"""
    data['total no'] = data.apply(lambda row: row['democratic no']
                                  + row['republican no']
                                  + row['independent no'], axis=1)
    return data


def fix_total6(data):
    """Cleans the 'total yes' column"""
    data['total yes'] = data.apply(lambda row: row['democratic yes']
                                   + row['republican yes']
                                   + row['independent yes'], axis=1)
    return data


def fix_total7(data):
    """Cleans the 'total not_voting' column"""
    data['total not_voting'] = data.apply(lambda row:
                                          row['democratic not_voting']
                                          + row['republican not_voting']
                                          + row['independent not_voting'],
                                          axis=1)
    return data


def fix_all(data):
    """Runs all the fix_total functions"""
    data1 = fix_total(data)
    data2 = fix_total2(data1)
    data3 = fix_total3(data2)
    data4 = fix_total4(data3)
    data5 = fix_total5(data4)
    data6 = fix_total6(data5)
    data7 = fix_total7(data6)
    data8 = data7.loc[data7.total_present != 0]
    return data8


def percentage_nonvoting(data):
    """Removes corrupted code with impossible outliers"""
    data['percentage_nonvoting_total'] = data.apply(
        lambda row: float(row['total not_voting'])
        / float(row['total_present']), axis=1)

    data['percentage_nonvoting_democratic'] = data.apply(
        lambda row: float(row['democratic not_voting'])
        / float(row['democratic_present']) if float(row['democratic_present'])
        else 0, axis=1)

    data['percentage_nonvoting_republican'] = \
        data.apply(lambda row: float(row['republican not_voting'])
                   / float(row['republican_present'])
                   if float(row['republican_present']) else 0, axis=1)

    data = data.loc[data.percentage_nonvoting_total <= .9]
    return data


def remove_column_whitespace(data):
    """Removes whitespace from columns"""
    space_list = []
    nospace_list = []
    list_columns = list(data.columns)
    for column in list_columns:
        if ' ' in column:
            space_list.append(column)
            nospace_list.append(column.replace(' ', '_'))
    for i in list(range(0, len(space_list))):
        col1 = space_list[i]
        col2 = nospace_list[i]
        data = data.rename(columns={col1: col2})
    return data


def full_clean():
    """Runs all the prior functions and exports csv"""
    dirty_data_senate = pd.read_csv("./data/dirty_data_senate.csv")
    dirty_data_house = pd.read_csv("./data/dirty_data_house.csv")
    dirty_data_house_2 = remove_extra_columns_house(dirty_data_senate,
                                                    dirty_data_house)
    cleaning_data_3 = merge_chambers(dirty_data_senate, dirty_data_house_2)
    cleaning_data_4 = drop_unnecessary_columns(cleaning_data_3)
    cleaning_data_5 = convert_to_datetime(cleaning_data_4)
    cleaning_data_6 = fill_null_object(cleaning_data_5)
    cleaning_data_7 = lowercase_object(cleaning_data_6)
    cleaning_data_8 = remove_nulls(cleaning_data_7)
    cleaning_data_9 = fix_all(cleaning_data_8)
    cleaning_data_10 = percentage_nonvoting(cleaning_data_9)
    cleaned_data = remove_column_whitespace(cleaning_data_10)
    cleaned_data.to_csv('./data/cleaned_for_testing.csv')

    return cleaned_data