import time
import pandas as pd
import numpy as np

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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    month = ''
    day = ''

    while city.lower() not in CITY_DATA:
        city = input('\nHello! Let\'s explore some US bikeshare data!\n would you like to see data for Chicago, New York City, or Washington?\n')

        if city.lower() in CITY_DATA:
            # load data file into a dataframe
            filter_cond = input('\nWould you like to filter the data by month, day, both, or not at all? Type "none" for no time filter.\n').lower()
            if filter_cond == 'both':
                month = input('\nWhich month? January, February, March, April, May, or June?\n').lower()
                day = input('\nWhich day? Please type your response (e.g., Sunday).\n').lower()
            elif filter_cond =='month':
                month = input('\nWhich month? January, February, March, April, May, or June?\n').lower()
                day='all'
            elif filter_cond == 'day':
                month = 'all'
                day = input('\nWhich day? Please type your response (e.g., Sunday).\n').lower()
            else:
                month = 'all'
                day = 'all'
        else:
            print("Sorry, we do not have any match in our database. Please input either ",
            "Chicago, New York, or Washington")

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
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    index = int(df['Start Time'].dt.month.mode()[0])
    most_pop_month = months[index - 1]
    print('The most popular month is {}.'.format(most_pop_month))


    # display the most common day of week
    most_pop_day = df['Start Time'].dt.weekday_name.mode()[0]
    print('The most popular day of week for start time is {}.'.format(most_pop_day))


    # display the most common start hour
    most_pop_hour = int(df['Start Time'].dt.hour.mode()[0])
    if most_pop_hour == 0:
        am_pm = 'am'
        pop_hour = 12
    elif 1 <= most_pop_hour < 13:
        am_pm = 'am'
        pop_hour = most_pop_hour
    elif 13 <= most_pop_hour < 24:
        am_pm = 'pm'
        pop_hour = most_pop_hour - 12
    print('The most popular hour of day for start time is {}{}.'.format(pop_hour, am_pm))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station Start Station
    pop_start_st = df['Start Station'].mode()[0]
    print('The most popular start station is {}.'.format(pop_start_st))

    # display most commonly used end station End Station
    pop_end_st = df['End Station'].mode()[0]
    print('The most popular end station is {}.'.format(pop_end_st))

    # display most frequent combination of start station and end station trip
    print('The most popular comvination of start and end station trip is {} and {}.'.format(pop_start_st, pop_end_st))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_duration = df['Trip Duration'].sum()
    second = tot_duration % 60
    minutes = (tot_duration-second)/60
    minute = minutes % 60
    hour = (minutes-minute)/60

    print('The total trip duration is {} hours, {} minutes and {}'
          ' seconds.'.format(hour, minute, second))
    # display mean travel time

    average_duration = round(df['Trip Duration'].mean())
    s = average_duration % 60
    ms = (average_duration-s)/60

    if ms > 60:
        m = ms % 60
        h = (ms-m)/60
        print('The average trip duration is {} hours, {} minutes and {}'
              ' seconds.'.format(h, m, s))
    else:
        print('The average trip duration is {} minutes and {} seconds.'.format(ms, s))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    Sub_scr_count = df['User Type'].value_counts().loc['Subscriber']
    Customer_count = df['User Type'].value_counts().loc['Customer']
    print('There are {} subscriber users users and {} cutomer users.'.format(Sub_scr_count, Customer_count))

    # Display counts of gender
    if 'Gender' in df:
        male_count = df['Gender'].value_counts().loc['Male']
        female_count = df['Gender'].value_counts().loc['Female']
        print('There are {} male users and {} female users.'.format(male_count, female_count))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest = int(df['Birth Year'].min())
        latest = int(df['Birth Year'].max())
        mode = int(df['Birth Year'].mode())
        print('The oldest users are born in {}.\nThe youngest users are born in {}.'
              '\nThe most popular birth year is {}.'.format(earliest, latest, mode))


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

        show_raw_data = input('\nDo you want to view the first 5 lines of raw day from the top?\n')
        start = 0
        while show_raw_data.lower() =='yes':
            print(df[start:start+5].head() )
            show_raw_data = input('\nDo you want to see the next 5 lines?\n')
            start+=5

        restart = input('\nWould you like to restart? Enter yes or no.\n')

        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
