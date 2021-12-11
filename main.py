import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import seaborn as sns
import sys


def importing_data(filename: str) -> pd.DataFrame:
    """
    The function takes csv file as an input and reads it using read_csv().
    It then converts this file into a python DataFrame and returns the Dataframe.
    :param filename: Name of the file for which DataFrame should be created.
    :return: DataFrame of the input file consisting of all rows and columns.
    >>> importing_data('Test.csv')
       Test_col1  Test_col2
    0          1          2
    1          1          2
    >>> importing_data('Test2.csv')
    Traceback (most recent call last):
    UnboundLocalError: local variable 'df' referenced before assignment
    """
    try:
        df = pd.read_csv(filename)

    except (FileNotFoundError, UnboundLocalError):
        pass

    return df


def clean_bchecks(bcheck: pd.DataFrame) -> pd.DataFrame:
    """
    In this function we extract year from month column and add it to the input dataframe.
    Further we add two new columns to display the total dealer and total private checks conducted.
    :param bcheck: DataFrame containing NICS firearm background checks data.
    :return: updated DataFrame for firearm background checks
    >>> clean_bchecks(pd.read_csv('nics-firearm-background-checks.csv',nrows=4))
       year     state  total_checks  total_dealer_checks  total_private
    0  2021   Alabama         66499                37242             29
    1  2021    Alaska          7572                 7065             17
    2  2021   Arizona         38523                32597              7
    3  2021  Arkansas         21518                16770             13
    >>>
    """
    bcheck = bcheck.fillna(0)
    bcheck['date'] = pd.to_datetime(bcheck['month'])
    bcheck['date'] = bcheck['date'].astype(str)
    bcheck['year'] = bcheck['date'].apply(lambda x: x[:4])
    bcheck['total_dealer_checks'] = bcheck.iloc[:, 3:8].agg(sum, axis=1)
    bcheck['total_private'] = bcheck.iloc[:, 21:23].agg(sum, axis=1)
    bcheck = bcheck.rename(columns={'totals': 'total_checks'})
    bcheck['year'] = bcheck['year'].astype(str).astype(int)
    bcheck = bcheck[['year', 'state', 'total_checks', 'total_dealer_checks', 'total_private']]

    return bcheck


def data_aggregation_by_parameter(df: pd.DataFrame, list_of_cols_to_aggregate: list, on_colums_to_aggregate) -> pd.DataFrame:
    """
    This function is used to aggregate year wise data for total background checks, total dealer checks
    and total private checks
    :param df: Updated DataFrame containing NICS firearm background checks data
    :param list_of_cols_to_aggregate: Column to be aggregated
    :param on_colums_to_aggregate: Column based on which data is aggregated
    :return: DataFrame of the aggregated data
    >>> df = importing_data('Test.csv')
    >>> df1 = data_aggregation_by_parameter(df,['Test_col1','Test_col2'],['Test_col2'])
    >>> df1
       Test_col2  Test_col1
    0          2          2
    """
    df = df[list_of_cols_to_aggregate].groupby(on_colums_to_aggregate).sum().reset_index()

    return df


def state_abbreviations() -> pd.DataFrame:
    """
    This function maps state names to their corresponding initials
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
    us_state_codes = pd.DataFrame.from_dict(us_state_to_abbrev, orient='index')
    us_state_codes = us_state_codes.reset_index()
    us_state_codes = us_state_codes.set_axis(['state', 'codes'], axis=1)

    return us_state_codes


def merge_datasets(df1: pd.DataFrame, df2: pd.DataFrame, how_to_join, columns_on_join) -> pd.DataFrame:
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
    joined_df = pd.merge(df1, df2, how=how_to_join, on=columns_on_join)
    return joined_df


def violentcrime_data(start_year: str, end_year: str, state_list) -> pd.DataFrame:
    """
    This function is used to fetch the violent crime data from fbi site through API.
    :param start_year: Starting year from where the API has to fetch the data.
    :param end_year:  Ending year till when the API has to fetch the data.
    :param state_list: The list of state of which the API should fetch the data.
    :return: Returns a dataframe with violent crimes from various states.
    >>> df=violentcrime_data('2011','2011',['RI'])
    >>> df
    ... # doctest: +NORMALIZE_WHITESPACE
       value  data_year  ...                                                key state
    0    587       2011  ...                                 Aggravated Assault    RI
    1     94       2011  ...  Sex Offenses (Except Rape, and Prostitution an...    RI
    2      1       2011  ...                         Manslaughter by Negligence    RI
    3      7       2011  ...               Murder and Nonnegligent Manslaughter    RI
    4     56       2011  ...                                               Rape    RI
    5    190       2011  ...                                            Robbery    RI
    6   4441       2011  ...                                     Simple Assault    RI
    7      0       2011  ...            Human Trafficking - Commercial Sex Acts    RI
    8      0       2011  ...          Human Trafficking - Involuntary Servitude    RI
    <BLANKLINE>
    [9 rows x 5 columns]
    """
    df = pd.DataFrame()
    for state in state_list:
        url = "https://api.usa.gov/crime/fbi/sapi/api/arrest/states/offense/{}/violent_crime/{}/{}?API_KEY=1mL3ffuFKhgkkiHWBy5bFzhSDNjN6IJYQQVIypY9".format(
            state, start_year, end_year)

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        crime_data = response.json()
        try:
            df1 = pd.json_normalize(crime_data['data'])
            df1['state'] = state
            df = df.append(df1)
        except KeyError:
            pass

    return df


def cleaning_violent_crime(df_violent_crime: pd.DataFrame) -> pd.DataFrame:
    """
    This fucntion is used to clean the data from API to make it more meaningful and useful
    :param df_violent_crime: The data from API goes as an input to this function
    :return: It returns with cleaning activity for the data fetched from API
    >>> cleaning_violent_crime(violentcrime_data('2011','2011',['RI']))
       crimes  year                                         crime_type state
    0     587  2011                                 Aggravated Assault    RI
    1      94  2011  Sex Offenses (Except Rape, and Prostitution an...    RI
    2       1  2011                         Manslaughter by Negligence    RI
    3       7  2011               Murder and Nonnegligent Manslaughter    RI
    4      56  2011                                               Rape    RI
    5     190  2011                                            Robbery    RI
    6    4441  2011                                     Simple Assault    RI
    7       0  2011            Human Trafficking - Commercial Sex Acts    RI
    8       0  2011          Human Trafficking - Involuntary Servitude    RI

    """
    df_violent_crime = df_violent_crime.set_axis(['crimes', 'year', 'month', 'crime_type', 'state'], axis=1)
    df_violent_crime = df_violent_crime.drop(['month'], axis=1)

    return df_violent_crime


# The correlationplot function has been designed from the mentioned blog below
# https://medium.com/@szabo.bibor/how-to-create-a-seaborn-correlation-heatmap-in-python-834c0686b88e


def correlationplot(dataframe: pd.DataFrame, plot_name):
    """
    This function is used to plot a correlation plot for the given dataframes.
    :param dataframe: The dataframe for which the correlation plot has to be plotted.
    :param plot_name: The name of the plot we have plotted using the mentioned dataframe
    :return: Return a heatmap with the correlation plot
    """
    plt.figure(figsize=(20, 15))
    mask = np.triu(np.ones_like(dataframe.corr(), dtype=bool))
    heatmap = sns.heatmap(dataframe.corr(), mask=mask, vmin=-1, vmax=1, annot=True, cmap='BrBG', annot_kws={"size": 20})
    heatmap.set_title(plot_name, fontdict={'fontsize': 24}, pad=16, ha="center")
    heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=30, ha="right", fontdict={'fontsize': 14})
    heatmap.set_yticklabels(heatmap.get_yticklabels(), rotation=45, ha="right", fontdict={'fontsize': 14})
    plt.show()


def statefilter(states, bcheck_crimes_state_year: pd.DataFrame) -> pd.DataFrame:
    """
    This function is used to apply a filter on the data for the qualifying states.
    :param states: States for which the data has to be filtered
    :param bcheck_crimes_state_year: The dataframe which has to be filtered for the mentioned states.
    :return: Return a dataframe with the filtered data

    """
    df = bcheck_crimes_state_year[bcheck_crimes_state_year['codes'].isin(states)]
    df = df.reset_index()
    return df


def arrestdata_filter(df_arrest: pd.DataFrame, list_of_crimes) -> pd.DataFrame:
    """
    This function is used to clean the arrest data with filtering out to homicides
    :param df_arrest: The dataframe which has arrest data loaded in it.
    :param list_of_crimes: list of crimes used to filter the data for homicides.
    :return: A dataframe which is filtered with homicides and aggregated at year level
    >>> arrestdata_filter(pd.read_csv('arrests_national_adults.csv') ,['Murder and Nonnegligent Homicide','Manslaughter by Negligence'])
        year  total_arrests  white  black  asian_pacific_islander  american_indian
    0   1994          16834   7628   8867                     188              130
    1   1995          16672   7668   8639                     205              138
    2   1996          13789   6429   7017                     173              166
    3   1997          13590   6049   7250                     171              113
    4   1998          12774   5998   6515                     130              116
    5   1999          11630   5491   5861                     147              118
    6   2000          11397   5324   5785                     141              117
    7   2001          11327   5594   5495                     128              102
    8   2002          10975   5553   5183                     133               97
    9   2003          10276   5306   4705                     129              119
    10  2004          10399   5535   4613                     123              112
    11  2005          10962   5680   4765                     129              112
    12  2006          10399   5364   4778                     116              117
    13  2007          10498   5387   4876                     120               98
    14  2008          10136   5223   4668                     113              103
    15  2009           9904   5151   4493                     106              114
    16  2010           9045   4760   4059                      93              108
    17  2011           8739   4425   4059                     122              114
    18  2012           9193   4646   4293                     142              103
    19  2013           8781   4246   4281                     138               98
    20  2014           8725   4298   4159                     142               88
    21  2015           9333   4470   4547                     173              118
    22  2016           9983   4757   4912                     153              106
    """
    df_arrest['total_arrests'] = df_arrest['total_male'] + df_arrest['total_female']
    df_arrest_new = df_arrest[df_arrest['offense_name'].isin(list_of_crimes)]
    df_arrest_new = df_arrest_new[
        ['year', 'total_arrests', 'white', 'black', 'asian_pacific_islander', 'american_indian']].groupby(
        'year').sum().reset_index()

    return df_arrest_new


def lineplot(x_axis, y_axis_1, y_axis_2):
    """
    This function is used to generate a line plot to analyze year wise total background checks and total dealer checks.
    :param x_axis: x axis column used for plotting.
    :param y_axis_1: y axis column used for plotting.
    :param y_axis_2: y axis column used for plotting.
    """
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(x_axis, y_axis_1, label='Total Checks')
    ax.plot(x_axis, y_axis_2, label='Total Dealer Checks')
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Background checks')
    ax.set_title('Background checks')
    ax.grid(True)
    fig.autofmt_xdate()
    plt.legend(loc='upper left')
    plt.xticks(x_axis)


def barplot(states_plotted: pd.DataFrame):
    """
    This function is used to generate a bar plot to analyze the states where maximum background checks are conducted.
    :param states_plotted: Dataframe of aggregated state wise data of total background checks.
    """
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(30, 10))
    bcheck_state = states_plotted.sort_values('total_checks')
    ax.bar(bcheck_state.state, bcheck_state.total_checks)
    ax.set_xlabel('States')
    ax.set_ylabel('Total Background checks')
    ax.set_title('Background checks from 1998 to 2021')
    ax.grid(True)
    fig.autofmt_xdate()
    plt.show()


if __name__ == '__main__':
    print('The Program has started running')
    # Importing data
    firearm_background = importing_data('nics-firearm-background-checks.csv')
    arrest_adults = importing_data('arrests_national_adults.csv')
    arrest_juveniles = importing_data('arrests_national_juvenile.csv')
    firearm_homicides = importing_data('firearm_homicides.csv')

    # Aggregating background data by year
    bchecks_year = data_aggregation_by_parameter(clean_bchecks(firearm_background),
                                                 ['year', 'total_checks', 'total_dealer_checks', 'total_private'],
                                                 'year')
    # Plotting a graph between years, total checks and total dealer checks
    lineplot(bchecks_year.year, bchecks_year.total_checks, bchecks_year.total_dealer_checks)

    # Aggregating checks by state and year
    bcheck_year_state = data_aggregation_by_parameter(clean_bchecks(firearm_background),
                                                      ['year', 'state', 'total_checks', 'total_dealer_checks',
                                                       'total_private'],
                                                      ['year', 'state'])

    # Merging States with their states codes
    bcheck_year_state_with_codes = merge_datasets(bcheck_year_state, state_abbreviations(),
                                                  'left',
                                                  ["state", "state"])
    # Aggregating checks by state to see which states have done maximum background checks
    bchecks_state = data_aggregation_by_parameter(clean_bchecks(firearm_background),
                                                  ['state', 'total_checks', 'total_dealer_checks', 'total_private'],
                                                  'state')

    barplot(bchecks_state)

    # List of states to fetch data from the API
    state_list = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY',
                  'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND',
                  'OH', 'OK', 'OR','PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

    # Fetching violent crime data from API
    violent_crime = cleaning_violent_crime(violentcrime_data(1999, 2020, state_list))

    # Aggregating violent crime data by year
    df_violent_crime_year = data_aggregation_by_parameter(violent_crime,
                                                          ['crimes', 'year', 'crime_type'],
                                                          'year')
    # Aggregating violent crime data by year and state
    df_violent_crime_year_state = data_aggregation_by_parameter(violent_crime,
                                                                ['crimes', 'year', 'crime_type', 'state'],
                                                                ['year', 'state'])

    # Combining violent crime data by year and state with background checks
    bcheck_crimes_state_year = pd.merge(bcheck_year_state_with_codes, df_violent_crime_year_state,
                                        how='right',
                                        left_on=['year', 'codes'],
                                        right_on=['year', 'state'])

    states_with_dealerchecks_mandatory = ['CA', 'CO', 'CT', 'DE', 'MD', 'NV', 'NJ', 'NM', 'NY', 'OR', 'RI', 'VT', 'VA',
                                          'WA']

    #
    correlationplot(merge_datasets(bchecks_year, df_violent_crime_year,
                                   'left',
                                   ["year", 'year']),
                    'violent crimes on background checks from 1998 to 2020')

    correlationplot(data_aggregation_by_parameter(statefilter(states_with_dealerchecks_mandatory,
                                                              bcheck_crimes_state_year),
                                                  ['year', 'total_checks',
                                                   'total_dealer_checks',
                                                   'total_private', 'crimes']
                                                  , 'year'
                                                  )
                    ,
                    'Violent crimes on background checks with states where dealer checks are mandatory from 1998 to 2020'
                    )


    correlationplot(merge_datasets(bchecks_year, firearm_homicides,
                                   'right',
                                   ['year', 'year']
                                   )
                    , 'Background checks effectiveness on firearm homicides from 2014 to 2020'
                    )

    correlationplot(merge_datasets(bchecks_year, arrestdata_filter(arrest_adults
                                                                   , ['Murder and Nonnegligent Homicide',
                                                                      'Aggravated Assault', 'Rape', 'Robbery',
                                                                      'Sex Offenses', 'Manslaughter by Negligence',
                                                                      'Simple Assault'])
                                   , 'right'
                                   , ['year', 'year']
                                   ),
                    'Arrests of Adult for Violent Crimes on background checks with ethnicity from 1998 to 2016')

    correlationplot(merge_datasets(bchecks_year, arrestdata_filter(arrest_adults
                                                                   , ['Murder and Nonnegligent Homicide',
                                                                      'Manslaughter by Negligence'])
                                   , 'right'
                                   , ['year', 'year']
                                   ),
                    'Arrests of Adult for homicides on background checks with ethnicity from 1998 to 2016')

    correlationplot(merge_datasets(bchecks_year, arrestdata_filter(arrest_juveniles
                                                                   , ['Murder and Nonnegligent Homicide',
                                                                      'Aggravated Assault', 'Rape', 'Robbery',
                                                                      'Sex Offenses', 'Manslaughter by Negligence',
                                                                      'Simple Assault'])
                                   , 'right'
                                   , ['year', 'year']
                                   ),
                    'Arrests of Juveniles for Violent Crimes on background checks with ethnicity from 1998 to 2016')

    correlationplot(merge_datasets(bchecks_year, arrestdata_filter(arrest_juveniles
                                                                   , ['Murder and Nonnegligent Homicide',
                                                                      'Manslaughter by Negligence'])
                                   , 'right'
                                   , ['year', 'year']
                                   ),
                    'Arrests of juveniles for homicides on background checks with ethnicity from 1998 to 2016')

    correlationplot(
        merge_datasets(bchecks_year, arrestdata_filter(pd.concat([arrest_adults,
                                                                  arrest_juveniles])
                                                       , ['Murder and Nonnegligent Homicide', 'Aggravated Assault',
                                                          'Rape', 'Robbery', 'Sex Offenses',
                                                          'Manslaughter by Negligence', 'Simple Assault'])
                       , 'right'
                       , ['year', 'year']
                       ),
        'Arrests of adults and juveniles for violent crimes on background checks with ethnicity from 1998 to 2016')

    correlationplot(
        merge_datasets(bchecks_year, arrestdata_filter(pd.concat([arrest_adults,
                                                                  arrest_juveniles])
                                                       , ['Murder and Nonnegligent Homicide',
                                                          'Manslaughter by Negligence'])
                       , 'right'
                       , ['year', 'year']
                       ),
        'Arrests of adults and juveniles for homicides on background checks with ethnicity from 1998 to 2016')

    print('The end')
