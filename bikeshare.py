import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

CITIES = ['chicago', 'new york city', 'washington']
MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
WEEKDAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please input the city you want to analyze (chicago, new york city, washington): ")
        if city.lower() in CITIES:
            break

    # TO DO: get user input for month (all, january, february, ..., june)
    while True:
        month = input("Please input the month you want to analyze (all, january, february, ..., june): ")
        if month.lower() in MONTHS:
            break
    
    # TO DO: get user input for day of week (all, monday, tuesday, ..., sunday)
    while True:
        day = input("Please input the day you want to analyze (all, monday, tuesday, ... sunday): ")
        if day.lower() in WEEKDAYS:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Rturns:
        df - Pandas DataFrame containing city data filtered by month and day
    """ 
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time, End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df.month.mode()[0]
    print('The most common month:', popular_month)

    # TO DO: display the most common day of week
    popular_day = df.day_of_week.mode()[0]
    print('The most common day of week:', popular_day)

    # TO DO: display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    popular_start_hour = df.start_hour.mode()[0]
    print('The most common start hour:', popular_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most common used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most common used start station:', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most common used end station:', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['journey'] = df['Start Station'] + ' -> ' + df['End Station']
    popular_journey = df['journey'].mode()[0]
    print('The most common journey:', popular_journey)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip durations"""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['travel_time'] = (df['End Time'] - df['Start Time']).dt.total_seconds()
    df = df[df['travel_time'] > 0]
    # TO DO: display total travel time
    print('Total travel time: %s seconds.' % (df['travel_time'].sum()))

    # TO DO: display mean travel time
    print('Average travel time: %s seconds.' % (df['travel_time'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The counts of user types\n', user_types)

    # TO DO: Displays counts of gender
    if 'Gender' in df.columns:
        print('The counts of gender\n', df['Gender'].value_counts())

    # TO DO: Display earliest, most recent, and common year of birth
    if 'Birth Year' in df.columns:
        print('The earliest year of birth:', int(df['Birth Year'].min()))
        print('The most recent year of birth:', int(df['Birth Year'].max()))
        print('The common year of birth:', int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while (view_data.lower() == 'yes'):
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()

        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == '__main__':
    main()
