import time
import pandas as pd
import numpy as np

'''
Those things were imported!
'''

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    periods = ['month','day','neither']

    print('\nHello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = str(input("Would you like to see data for Chicago, New York City, or Washington?\n")).lower()
        if city in CITY_DATA:
            break
        else:
            print('\n\'{}\' is not an available city. Please try again.\n'.format(city))

    # get user input for which period of time: month, day, neither
        # if month, which (all, january, february, ... , june)
        # if day, which (all, monday, tuesday, ... sunday)

    while True:
        period = str(input("Would you like to filter the data by month, day, or neither?\n")).lower()
        if period == 'month':
            month = str(input("Which month (select from: all, January, February, March, April, May, or June)? ")).lower()
            if month in months:
                day = 'all'
                break
            else:
                print('\n\'{}\' is not an option. Please try again.\n'.format(month))
        elif period == 'day':
            day = str(input("Which day (select from: all, Monday, Tuesday, ...Sunday)?\n")).lower()
            if day in days:
                month = 'all'
                break
            else:
                print('\n\'{}\' is not an option. Please try again.\n'.format(day))
        elif period == 'neither':
            print('Okay. Neither it is. (Ha! That means you get to see EV-ER-Y-THING from ' + city.title() + '.)\n')
            month = 'all'
            day = 'all'
            break
        else:
            print('\n\'{}\' is not an option. Please try again.\n'.format(period))


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

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

    # display the most common month
    commonest_month = str(df['month'].mode()[0])
    print('Most common month: ' + commonest_month)

    # display the most common day of week
    commonest_day = str(df['day_of_week'].mode()[0])
    print('Most common day of week: ' + commonest_day)

    # display the most common start hour
    commonest_hour = str(df['hour'].mode()[0])
    print('Most common start hour: ' + commonest_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    commonest_start_station = (df['Start Station'].mode()[0])
    print('Most common start station: ' + commonest_start_station)

    # display most commonly used end station
    commonest_end_station = (df['End Station'].mode()[0])
    print('Most common end station: ' + commonest_end_station)

    # display most frequent combination of start station and end station trip
    df['combo'] = (df['Start Station']) + ' to ' + (df['End Station'])
    commonest_station_combo = (df['combo'].mode()[0])
    print('Most common start and end station combination: ' + commonest_station_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = str(int(df['Trip Duration'].sum()))
    print('Total travel time: ' + total_travel_time)

    # display mean travel time
    mean_travel_time = str(df['Trip Duration'].mean())
    print('Mean travel time: ' + mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCounts of user types:')
    print(df['User Type'].value_counts().to_frame())

    # Display counts of gender
    print('\nCounts of gender types:')
    if 'Gender' in df:
        blank_gender = str(int(df['Gender'].isna().sum()))
        print(df['Gender'].value_counts().to_frame())
        print('Users without a recorded gender: ' + blank_gender)
    else:
        print('Genders are not available for this city.')

    # Display earliest, most recent, and most common year of birth
    print('\nBirth Year Data')
    if 'Birth Year' in df:
        earliest_birth = str(int(df['Birth Year'].min()))
        latest_birth = str(int(df['Birth Year'].max()))
        commonest_birth = str(int(df['Birth Year'].mode()))
        blank_birth = str(int(df['Birth Year'].isna().sum()))
        print('Earliest year of birth:    ' + earliest_birth)
        print('Most recent year of birth: ' + latest_birth)
        print('Most common year of birth: ' + commonest_birth)
        print('Users without a recorded birth: ' + blank_birth)
    else:
        print('Birth Years are not available for this city.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #prompt the user if they want to see 5 lines of raw data
        i = 0
        while True:
            raw_data = input('Do you wish to view the raw data? (y/n)\n')
            if raw_data.lower() == 'yes' or raw_data.lower() == 'y':
                #iterate and print 5 rows at a time.
                i += 0
                print(df[df.columns[0:]].iloc[0+i:i+5])
                i += 5
            else:
                break


        restart = input('\nWould you like to restart? (y/n).\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
