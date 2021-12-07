import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import seaborn as sns


def importing_data(filename: str):
    """
    The function takes file as an input parameter, converts it into a python DataFrame and returns the Dataframe.
    :param filename: Name of the file for which DataFrame should be created.
    :return: DataFrame of the input file consisting of all rows and columns.
    >>> importing_data('Test.csv')
       Test_col1  Test_col2
    0          1          2
    1          1          2
    """
    df = pd.read_csv(filename)

    return df


def clean_bchecks(bcheck):
    """
    In this function we extract year from month column and add it to the input dataframe.
    Further we add two new columns to display the total dealer and total private checks conducted.
    :param bcheck: DataFrame containing NICS firearm background checks data.
    :return: updated DataFrame for firearm background checks
    >>> clean_bchecks( pd.read_csv('nics-firearm-background-checks.csv',nrows=4))
       year     state  total_checks  total_dealer_checks  total_private
    0  2021   Alabama         66499                37242             29
    1  2021    Alaska          7572                 7065             17
    2  2021   Arizona         38523                32597              7
    3  2021  Arkansas         21518                16770             13

    """
    bcheck['date'] = pd.to_datetime(bcheck['month'])
    bcheck['date'] = bcheck['date'].astype(str)
    bcheck['year'] = bcheck['date'].apply(lambda x: x[:4])
    bcheck['total_dealer_checks'] = bcheck.iloc[:, 3:8].agg(sum, axis=1)
    bcheck['total_private'] = bcheck.iloc[:, 21:23].agg(sum, axis=1)
    bcheck = bcheck.rename(columns={'totals': 'total_checks'})
    bcheck['year'] = bcheck['year'].astype(str).astype(int)
    bcheck=bcheck[['year','state','total_checks','total_dealer_checks','total_private']]
    return bcheck


def data_aggregation_by_parameter(df,list_of_cols_to_aggregate, on_colums_to_aggregate):
    """
    This function is used to aggregate year wise data for total backgroud checks, total dealer checks and total private checks
    :param df: Updated DataFrame containing NICS firearm background checks data
    :param list_of_cols_to_aggregate: Column to be aggregated
    :param on_colums_to_aggregate: Column based on which data is aggregated
    :return: DataFrame of the aggregated data
    >>> df=importing_data('Test.csv')
    >>> df1=data_aggregation_by_parameter(df,['Test_col1','Test_col2'],['Test_col2'])
    >>> df1
       Test_col2  Test_col1
    0          2          2
    """
    df = df[list_of_cols_to_aggregate].groupby(on_colums_to_aggregate).sum().reset_index()

    return df


def state_abbreviations():
    """
    Mapping state names to their corresponding initials
    :return: Correctly mapped state initials DataFrame
    >>> state_abbreviations()
                                       state codes
    0                                Alabama    AL
    1                                 Alaska    AK
    2                                Arizona    AZ
    3                               Arkansas    AR
    4                             California    CA
    5                               Colorado    CO
    6                            Connecticut    CT
    7                               Delaware    DE
    8                                Florida    FL
    9                                Georgia    GA
    10                                Hawaii    HI
    11                                 Idaho    ID
    12                              Illinois    IL
    13                               Indiana    IN
    14                                  Iowa    IA
    15                                Kansas    KS
    16                              Kentucky    KY
    17                             Louisiana    LA
    18                                 Maine    ME
    19                              Maryland    MD
    20                         Massachusetts    MA
    21                              Michigan    MI
    22                             Minnesota    MN
    23                           Mississippi    MS
    24                              Missouri    MO
    25                               Montana    MT
    26                              Nebraska    NE
    27                                Nevada    NV
    28                         New Hampshire    NH
    29                            New Jersey    NJ
    30                            New Mexico    NM
    31                              New York    NY
    32                        North Carolina    NC
    33                          North Dakota    ND
    34                                  Ohio    OH
    35                              Oklahoma    OK
    36                                Oregon    OR
    37                          Pennsylvania    PA
    38                          Rhode Island    RI
    39                        South Carolina    SC
    40                          South Dakota    SD
    41                             Tennessee    TN
    42                                 Texas    TX
    43                                  Utah    UT
    44                               Vermont    VT
    45                              Virginia    VA
    46                            Washington    WA
    47                         West Virginia    WV
    48                             Wisconsin    WI
    49                               Wyoming    WY
    50                  District of Columbia    DC
    51                        American Samoa    AS
    52                                  Guam    GU
    53              Northern Mariana Islands    MP
    54                           Puerto Rico    PR
    55  United States Minor Outlying Islands    UM
    56                   U.S. Virgin Islands    VI

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
    :return: A dataframe with the combination of required columns from both the given dataframes
    >>> df=importing_data('Test.csv')
    >>> d = {'Test_col1': [1, 2], 'Test_col3': [3, 4]}
    >>> df1 = pd.DataFrame(data=d)
    >>> df2 = merge_datasets(df,df1,'left',["Test_col1","Test_col1"])
    >>> df2
       Test_col1  Test_col2  Test_col3
    0          1          2          3
    1          1          2          3

    """
    Joined_df = pd.merge(df1, df2, how=how_to_join, on=columns_on_join)
    return Joined_df


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
    plt.figure(figsize=(15, 15))
    mask = np.triu(np.ones_like(dataframe.corr(), dtype=bool))
    heatmap = sns.heatmap(dataframe.corr(), mask=mask, vmin=-1, vmax=1, annot=True, cmap='BrBG',annot_kws={"size":20})
    heatmap.set_title(plot_name, fontdict={'fontsize':24}, pad=16)
    heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=30, ha="right",fontdict={'fontsize':14})
    heatmap.set_yticklabels(heatmap.get_yticklabels(), rotation=45, ha="right",fontdict={'fontsize':14})
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

    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(bchecks_year.year, bchecks_year.total_checks, label='Total Checks')
    ax.plot(bchecks_year.year, bchecks_year.total_dealer_checks,label = 'Total Dealer Checks')
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Background checks')
    ax.set_title('Background checks')
    ax.grid(True)
    fig.autofmt_xdate()
    ax.legend(loc='upper left')

    bcheck_year_state=data_aggregation_by_parameter(clean_bchecks(importing_data('nics-firearm-background-checks.csv')),
                                                    ['year','state','total_checks','total_dealer_checks','total_private'],
                                                    ['year','state'])


    bcheck_year_state_with_codes = merge_datasets(bcheck_year_state,state_abbreviations(),
                                                  'left',
                                                  ["state", "state"])

    bchecks_state = data_aggregation_by_parameter(clean_bchecks(importing_data('nics-firearm-background-checks.csv')),
                                                 ['state', 'total_checks', 'total_dealer_checks', 'total_private'],
                                                 'state')

    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(30, 10))
    bcheck_state = bchecks_state.sort_values('total_checks')
    ax.bar(bcheck_state.state, bcheck_state.total_checks)
    ax.set_xlabel('States')
    ax.set_ylabel('Total Background checks')
    ax.set_title('Background checks from 1998 to 2021')
    ax.grid(True)
    ax.legend(loc='upper left');
    fig.autofmt_xdate()
    plt.show()

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


