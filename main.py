import matplotlib as matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
import requests
# %matplotlib inline


def importing_data(filename: str):
    """
    The function takes file as an input parameter, converts it into a python DataFrame and returns the Dataframe.
    :param filename: Name of the file for which DataFrame should be created.
    :return: DataFrame of the input file consisting of all rows and columns.

    """
    df = pd.read_csv(filename)

    return df


def clean_bchecks(bcheck):
    """
    In this function we extract year from month column and add it to the input dataframe.
    Further we add two new columns to display the total dealer and total private checks conducted.
    :param dataframe: DataFrame containing NICS firearm background checks data.
    :return: updated DataFrame for firearm background checks

    """
    bcheck['date'] = pd.to_datetime(bcheck['month'])
    bcheck['date'] = bcheck['date'].astype(str)
    bcheck['year'] = bcheck['date'].apply(lambda x: x[:4])
    bcheck['total_dealer_checks'] = bcheck.iloc[:, 3:8].agg(sum, axis=1)
    bcheck['total_private'] = bcheck.iloc[:, 21:23].agg(sum, axis=1)
    return bcheck


def data_aggregation_by_one_parameter(bcheck,list_of_cols_to_aggregate, on_colums_to_aggregate):
    # take a list of columns as input and another list for aggreagtion
    """
    This function is used to aggregate year wise data for total backgroud checks, total dealer checks and total private checks
    :param bcheck: Updated DataFrame containing NICS firearm background checks data
    :param list_of_cols_to_aggregate: Column to be aggregated
    :param on_colums_to_aggregate: Column based on which data is aggregated
    :return: DataFrame of the aggregated data

    """
    bcheck_year = bcheck[list_of_cols_to_aggregate].groupby(on_colums_to_aggregate).sum()
    bcheck_year = bcheck_year.reset_index()
    return bcheck_year


def state_abbreviations():
    """
    Mapping state names to their corresponding initials
    :return: Correctly mapped state initials DataFrame
    """
    us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}
    us_state_codes= pd.DataFrame.from_dict(us_state_to_abbrev, orient='index')
    us_state_codes= us_state_codes.reset_index()
    us_state_codes=us_state_codes.set_axis(['states','codes'],axis=1)
#     bcheck_year_state.info()
#     us_state_codes.info()
    return us_state_codes

def merge_datasets(df1, df2,how_to_join,columns_on_join): #how should be added as a parameter
    """
    This function is used to merge two datasets based on a common column.
    :param df1:
    :param df2:
    :param how_to_join:
    :param columns_on_join:
    :return:
    """
    bcheck_year_state_with_codes = pd.merge(df1, df2, how=how_to_join, on=columns_on_join)
    return bcheck_year_state_with_codes


def violentcrime_data(start_year, end_year, state_list):
    """

    :param start_year:
    :param end_year:
    :param state_list:
    :return:
    """
    df = pd.DataFrame()
    for state in state_list:
        url = "https://api.usa.gov/crime/fbi/sapi/api/arrest/states/offense/{}/violent_crime/{}/{}?API_KEY=1mL3ffuFKhgkkiHWBy5bFzhSDNjN6IJYQQVIypY9".format(
            state, start_year, end_year)
        #     print(url)
        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        #     print(response.text)

        data1 = response.json()
        try:
            df1 = pd.json_normalize(data1['data'])
            df1['state'] = state
            df = df.append(df1)
        except KeyError:
            pass

    return df

def correlationplotnew(dataframe,plot_name):
    """

    :param dataframe:
    :param plot_name:
    :return:
    """
    plt.figure(figsize=(16, 6))
    mask = np.triu(np.ones_like(dataframe.corr(), dtype=bool))
    heatmap = sns.heatmap(dataframe.corr(), mask=mask, vmin=-1, vmax=1, annot=True, cmap='BrBG')
    heatmap.set_title(plot_name, fontdict={'fontsize':18}, pad=16)
    return heatmap


def statefilter(states, bcheck_crimes_state_year):
    """

    :param states:
    :param bcheck_crimes_state_year:
    :return:
    """
    list_of_states = states
    df = bcheck_crimes_state_year[bcheck_crimes_state_year['codes'].isin(list_of_states)]
    df = df.reset_index()
    return df

def arrestdataviolentcrimes(df_arrest):
    """

    :param df_arrest:
    :return:
    """
    list_of_violent_crimes =['Murder and Nonnegligent Homicide','Aggravated Assault','Rape','Robbery','Sex Offenses','Manslaughter by Negligence','Simple Assault']
    df_arrest_violent_crimes=df_arrest[df_arrest['offense_name'].isin(list_of_violent_crimes)]
    df_arrest_violent_crimes=df_arrest_violent_crimes[['year','total_arrests','white','black','asian_pacific_islander','american_indian']].groupby('year').sum().reset_index()

    return df_arrest_violent_crimes

def arrestdatahomicide(df_arrest):
    """

    :param df_arrest:
    :return:
    """
    list_of_homicides=['Murder and Nonnegligent Homicide','Manslaughter by Negligence']
    df_arrest_homicides=df_arrest[df_arrest['offense_name'].isin(list_of_homicides)]
    df_arrest_homicides=df_arrest_homicides[['year','total_arrests','white','black','asian_pacific_islander','american_indian']].groupby('year').sum().reset_index()
    return df_arrest_homicides


if __name__ == '__main__':
    bchecks=clean_bchecks(importing_data('/Users/venkatasaisahitpotnuru/Downloads/nics-firearm-background-checks.csv'))

    print(bchecks)