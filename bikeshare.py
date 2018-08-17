import time
import pandas as pd
import numpy as np
from datetime import datetime
import time
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
    # get user raw_input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid raw_inputs

    city = ""
    while city.lower() not in CITY_DATA.keys():

        try:
            var_raw_input=input("Would you like to see data for Chicago, New York City or Washington?\n")
            if var_raw_input.lower() not in CITY_DATA.keys():
                print('I don\'t understand your raw_input. Please try again.')
            else:
                city=var_raw_input.lower()
                print('You chose the city: {}'.format(city))
        except ValueError as e:
            print('That\'s not a valid raw_input. Please try again. {}'.format(e))

    available_filters=["none","day","month","both"]
    filter = ""
    while filter.lower() not in available_filters:

        try:
            var_raw_input=input('Would you like to filter the data by month, day, both or not at all? Type "none" for no time filter.\n')
            if var_raw_input.lower() not in available_filters :
                print("The valid values for filter are day,month,both or none. Please try again.\n")
            else :
                filter=var_raw_input.lower()
        except ValueError as e:
            print("An error occured while setting the filter, please try again.\n")

    month=""
    if filter == "both" or filter == "month":
        available_months=["january","february","march","april","may","june"]
        while month.lower() not in available_months:
            try:
                var_raw_input=input('Which month - January, February, March, April, May, or June?\n')
                if var_raw_input.lower() not in available_months:
                    print("This month is not in the availble choices. Please try again.\n")
                else:
                    month=var_raw_input.lower()
            except ValueError as e:
                print("An error occured while setting the month, please try again.\n")
    else:
        month="none"

    if filter == "both" or filter == "day":
        valid_value=False
        while (valid_value != True):
            try:
                var_raw_input=input("Which day-Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday? Please type your response as an integer (e.g., 0=Monday,6=Sunday).")
                if not (int(var_raw_input) >= 0 and int(var_raw_input) <= 6):
                    print("The provided value should be an integer between 0 to 6.\n")
                else:
                    day=int(var_raw_input)
                    valid_value=True
            except ValueError as e:
                print("An error occured while setting the day, please try again.\n")
    else:
        day="none"

    print('Search informations: city={} filter={} month={} day={}'.format(city,filter,month,day))



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
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['month']=df['Start Time'].dt.month
    df['day_of_week']=df['Start Time'].dt.weekday_name

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month=df['month'].mode()[0]
    print('The most common month: ', popular_month)

    # display the most common day of week
    popular_day_of_week=df['day_of_week'].mode()[0]
    print('The most common day of week: ', popular_day_of_week)

    # display the most common start hour
    popular_start_hour=df['Start Time'].mode()[0]
    print('The most common start hour: ', popular_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station=df["Start Station"].mode()[0]
    print('The most commonly used start station: ', popular_start_station)

    # display most commonly used end station
    popular_end_station=df["End Station"].mode()[0]
    print('The most commonly used end station: ', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['station mapping']=df["Start Station"].map(str)+df["End Station"]
    popular_station_combination=df["station mapping"].mode()[0]
    print('The most frequent combination of start station and end station trip:', popular_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    duration=df["Trip Duration"].sum()
    minute, second = divmod(duration, 60)
    hour, minute = divmod(minute, 60)
    print('The total travel time is: {} hours, {} minutes {}seconds.'.format(hour,minute,second))

    # display mean travel time
    mean_duration=df["Trip Duration"].mean()
    minute1, second1 = divmod(mean_duration, 60)
    hour1, minute1 = divmod(minute, 60)
    print('The mean travel time is:{} hours, {} minutes {} seconds.'.format(hour1, minute1, second1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    try :
        gender=df['Gender'].value_counts()
        print(gender)
    except KeyError as e:
        print("There is no gender data")

    # Display earliest, most recent, and most common year of birth
    try :
        birth_year_min1 = int(df['Birth Year'].min())
        birth_year_max1 = int(df['Birth Year'].max())
        birth_year_mean1 = int(df['Birth Year'].mean())

        print("The earliest year of bith is: {}.".format(birth_year_min1))
        print("The most recent year of birth is: {}.".format(birth_year_max1))
        print("The most common year of birth is: {}.".format(birth_year_mean1))
    except KeyError as e:
        print("No Birth data")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def getTripData(df):
        try:
            filter_2 = input ('Would you like to see individual trip data? Type "yes" or "no".')
            if filter_2.lower() == "yes":
            	count=0
            	for i in df.iterrows():
                	print(i)
                	count += 1
                	if (count == 5):
                		count = 0
                		var_input=input('Type anything to continue or "no" to stop.')
                		if var_input == "no":
                			break

        except KeyError as e:
            print ('I don\t understand your raw_input. The valid raw_input is "yes" or "no".\n')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        getTripData(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
