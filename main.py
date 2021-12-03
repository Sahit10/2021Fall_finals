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
    :param bcheck: DataFrame containing NICS firearm background checks data.
    :return: updated DataFrame for firearm background checks

    """
    bcheck['date'] = pd.to_datetime(bcheck['month'])
    bcheck['date'] = bcheck['date'].astype(str)
    bcheck['year'] = bcheck['date'].apply(lambda x: x[:4])
    bcheck['total_dealer_checks'] = bcheck.iloc[:, 3:8].agg(sum, axis=1)
    bcheck['total_private'] = bcheck.iloc[:, 21:23].agg(sum, axis=1)
    bcheck = bcheck.rename(columns={'totals': 'total_checks'})
    bcheck['year'] = bcheck['year'].astype(str).astype(int)
    return bcheck


def data_aggregation_by_parameter(df,list_of_cols_to_aggregate, on_colums_to_aggregate):
    """
    This function is used to aggregate year wise data for total backgroud checks, total dealer checks and total private checks
    :param df: Updated DataFrame containing NICS firearm background checks data
    :param list_of_cols_to_aggregate: Column to be aggregated
    :param on_colums_to_aggregate: Column based on which data is aggregated
    :return: DataFrame of the aggregated data

    """
    df = df[list_of_cols_to_aggregate].groupby(on_colums_to_aggregate).sum().reset_index()

    return df


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
    us_state_codes=us_state_codes.set_axis(['state','codes'],axis=1)
#     bcheck_year_state.info()
#     us_state_codes.info()
    return us_state_codes

def merge_datasets(df1, df2,how_to_join,columns_on_join): #how should be added as a parameter
    """
    This function is used to merge two datasets based on a common column.
    :param df1: First dataframe that has to be merged
    :param df2: Second dataframe that has to be merged
    :param how_to_join: Type of join we want to perform
    :param columns_on_join: On which columns the join should happen
    :return:
    """
    bcheck_year_state_with_codes = pd.merge(df1, df2, how=how_to_join, on=columns_on_join)
    return bcheck_year_state_with_codes


def violentcrime_data(start_year, end_year, state_list):
    """
    This function is used to fetch the violent crime data from fbi site through API.
    :param start_year: Starting year from where the API has to fetch the data.
    :param end_year:  Ending year till when the API has to fetch the data.
    :param state_list: The list of state of which the API should fetch the data.
    :return: Returns a dataframe with violent crimes from various states.
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

def cleaning_violent_crime(df_violent_crime):
    """
    This fucntion is used to clean the data from API to make it more meaningful and useful
    :param df_violent_crime: The data from API goes as an input to this function
    :return: It returns with cleaning activity for the data fetched from API
    """
    df_violent_crime = df_violent_crime.set_axis(['crimes', 'year', 'month', 'crime_type', 'state'], axis=1)
    df_violent_crime = df_violent_crime.drop(['month'], axis=1)

    return df_violent_crime


def correlationplot(dataframe,plot_name):
    """
    This function is used to plot a correlation plot for the given dataframes
    :param dataframe: The dataframe for which the correlation plot has to be plotted.
    :param plot_name: The name of the plot we have plotted using the mentioned dataframe
    :return: Return a heatmap with the correlation plot
    """
    plt.figure(figsize=(20, 15))
    mask = np.triu(np.ones_like(dataframe.corr(), dtype=bool))
    heatmap = sns.heatmap(dataframe.corr(), mask=mask, vmin=-1, vmax=1, annot=True, cmap='BrBG')
    heatmap.set_title(plot_name, fontdict={'fontsize':18}, pad=16)
    return heatmap


def statefilter(states, bcheck_crimes_state_year):
    """
    This function is used to apply a filter on the data for the qualifying states.
    :param states: States for which the data has to be filtered
    :param bcheck_crimes_state_year: The dataframe which has to be filtered for the mentioned states.
    :return: Return a dataframe with the filtered data
    """
    list_of_states = states
    df = bcheck_crimes_state_year[bcheck_crimes_state_year['codes'].isin(list_of_states)]
    df = df.reset_index()
    return df

def arrestdataviolentcrimes(df_arrest):
    """
    This function is used to clean the arrest data with filtering out to violent crimes
    :param df_arrest: The dataframe which has arrest data loaded in it.
    :return: A dataframe which is filtered with violent crimes and aggregated at year level
    """

    df_arrest['total_arrests']=df_arrest['total_male']+df_arrest['total_female']
    list_of_violent_crimes =['Murder and Nonnegligent Homicide','Aggravated Assault','Rape','Robbery','Sex Offenses','Manslaughter by Negligence','Simple Assault']
    df_arrest_violent_crimes=df_arrest[df_arrest['offense_name'].isin(list_of_violent_crimes)]
    df_arrest_violent_crimes=df_arrest_violent_crimes[['year','total_arrests','white','black','asian_pacific_islander','american_indian']].groupby('year').sum().reset_index()

    return df_arrest_violent_crimes

def arrestdatahomicide(df_arrest):
    """

    This function is used to clean the arrest data with filtering out to homicides
    :param df_arrest: The dataframe which has arrest data loaded in it.
    :return: A dataframe which is filtered with homicides and aggregated at year level
    """

    df_arrest['total_arrests']=df_arrest['total_male']+df_arrest['total_female']
    list_of_homicides=['Murder and Nonnegligent Homicide','Manslaughter by Negligence']
    df_arrest_homicides=df_arrest[df_arrest['offense_name'].isin(list_of_homicides)]
    df_arrest_homicides=df_arrest_homicides[['year','total_arrests','white','black','asian_pacific_islander','american_indian']].groupby('year').sum().reset_index()
    return df_arrest_homicides


if __name__ == '__main__':

    bchecks_year=data_aggregation_by_parameter(clean_bchecks(importing_data('nics-firearm-background-checks.csv')),
                                               ['year','total_checks','total_dealer_checks','total_private'],
                                               'year')

    # Line graph has to be added here as part of EDA

    bcheck_year_state=data_aggregation_by_parameter(clean_bchecks(importing_data('nics-firearm-background-checks.csv')),
                                                    ['year','state','total_checks','total_dealer_checks','total_private'],
                                                    ['year','state'])


    bcheck_year_state_with_codes = merge_datasets(bcheck_year_state,state_abbreviations(),
                                                  'left',
                                                  ["state", "state"])

    bchecks_state = data_aggregation_by_parameter(clean_bchecks(importing_data('nics-firearm-background-checks.csv')),
                                                 ['state', 'total_checks', 'total_dealer_checks', 'total_private'],
                                                 'state')

    #bar graph has to be plotted here

    state_list = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY',
                  'LA', 'ME', 'MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR',
                  'PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']

    violent_crime=cleaning_violent_crime(violentcrime_data(1999,2020,state_list))

    df_violent_crime_year=data_aggregation_by_parameter(violent_crime,
                                                        ['crimes','year','crime_type'],
                                                        'year')

    df_violent_crime_year_state=data_aggregation_by_parameter(violent_crime,
                                                        ['crimes','year','crime_type','state'],
                                                        ['year','state'])

    correlationplot(merge_datasets(bchecks_year,df_violent_crime_year,
                                   'left',
                                   ["year",'year']),
                    'violent crimes on Bchecks')
    plt.show()

    bcheck_crimes_state_year = pd.merge(bcheck_year_state_with_codes, df_violent_crime_year_state,
                                        how='right',
                                        left_on=['year', 'codes'],
                                        right_on=['year', 'state'])


    states_with_dealerchecks_mandatory = ['CA','CO','CT','DE','MD','NV','NJ','NM','NY','OR','RI','VT','VA','WA']

    correlationplot( data_aggregation_by_parameter(statefilter(states_with_dealerchecks_mandatory,
                                                              bcheck_crimes_state_year),
                                                ['year', 'total_checks',
                                                'total_dealer_checks',
                                                'total_private', 'crimes']
                                                ,'year'
                                                 )
                  ,'Violent crimes on bchecks with filtered states where dealer checks are mandatory'
                  )
    plt.show()

    correlationplot(merge_datasets(bchecks_year,importing_data('firearm_homicides.csv'),
                                   'right',
                                   ['year','year']
                                   )
                    ,'Bchecks effectiveness across firearm homicides'
                    )
    plt.show()

    correlationplot(merge_datasets(bchecks_year, arrestdataviolentcrimes(importing_data('arrests_national_adults.csv'))
                                   ,'right'
                                   ,['year','year']
                                   ),
                    'Adult & Violent Crimes')
    plt.show()

    correlationplot(merge_datasets(bchecks_year, arrestdatahomicide(importing_data('arrests_national_adults.csv'))
                                   , 'right'
                                   , ['year', 'year']
                                   ),
                    'Adult & Homicides')
    plt.show()

    correlationplot(merge_datasets(bchecks_year, arrestdataviolentcrimes(importing_data('arrests_national_juvenile.csv'))
                                   , 'right'
                                   , ['year', 'year']
                                   ),
                    'Juvi & Violent Crimes')
    plt.show()

    correlationplot(merge_datasets(bchecks_year, arrestdatahomicide(importing_data('arrests_national_juvenile.csv'))
                                   , 'right'
                                   , ['year', 'year']
                                   ),
                    'Juvi & Homicides')

    plt.show()

    correlationplot(
        merge_datasets(bchecks_year, arrestdataviolentcrimes(pd.concat([importing_data('arrests_national_juvenile.csv'),
                                                                       importing_data('arrests_national_juvenile.csv')]))
                       , 'right'
                       , ['year', 'year']
                       ),
        'Adult,Juvi & Violent Crimes')

    plt.show()

    correlationplot(
        merge_datasets(bchecks_year, arrestdatahomicide(pd.concat([importing_data('arrests_national_juvenile.csv'),
                                                                       importing_data('arrests_national_juvenile.csv')]))
                                                             , 'right'
                                                             , ['year', 'year']
                                                             ),
                       'Adult,Juvi & Homicides')

    plt.show()


