import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello Udacity Team! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    print('*' * 40)
    city = 'not selected'
    while city not in ['chicago', 'new york city', 'washington', 'exit']:
        city = input("Select a city: Chicago, New York City, Washington or exit to exit ").lower()
        if city == 'exit':
            break

    # get user input for month (all, january, february, ... , june)
    month = 'not selected'
    day = 'not selected'
    if city != 'exit':
        while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'exit']:
            month = input("For which month do you want to see stats? all, january, ... , june or exit?").lower()
            if month == 'exit':
                day = 'exit'
                break

    # get user input for the day (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday)
        while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'exit']:
            if city == 'exit' or month == 'exit':
                day = 'exit'
                break
            else:
                day = input("For which day do you want to see stats? all, monday, .. , sunday or exit?").lower()
            if day == 'exit':
                break

    if city != 'exit' and month != 'exit' and day != exit:
        print("Your selection -- city: {}, month: {}, day of the week: {}".format(city.title(), month.title(), day.title()))
    return city, month, day


def load_data(city, month, day):
    """Loads the City data and applies the date filters. Returns the DataFrame."""

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extract month, day and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable

    if month != 'all':
        # use the index of the months list to get the corresponding int #
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        df = df[df['day_of_week'] == day]
    return df


def load_raw_data(df):
    """Displays filtered raw data in 5 line steps until users input"""
    i = 0
    lines = len(df)
    while i < lines:
        restart = input('\nWould you like see or continue displaying raw data? Enter yes or no.')
        if restart.lower() != 'yes':
            break
        else:
            print(df.iloc[[i, i+1, i+2, i+3, i+4]].transpose())
            i += 5
            

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    print(popular_hour, ' - is the most frequent start hour in your selected city.')

    # display the most common month
    popular_day = df['day_of_week'].mode()[0]
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    popular_day = days[popular_day]
    print(popular_day,  ' - is the Day of the week with the most frequent usage in your selected city.')

    # display the most common day of week
    popular_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[popular_month-1]
    print(popular_month, ' - is the month with the most frequent usage in your selected city.')
    print("This took %s seconds." % (round((time.time() - start_time), 5)))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    print(popular_start_station, ' - is the most frequent used start station with your selected city, month and day.')

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    print(popular_end_station, ' - is the most frequent used end station with your selected city, month and day.')
    # display most frequent combination of start station and end station trip
    popular_station_combination = df["Start Station"] + ' -- ' + df["End Station"]
    popular_station_combination = popular_station_combination.value_counts().idxmax()
    print(popular_station_combination, ' - is the most used station combination in the selected city, month and day.')
    print("This took %s seconds." % (round((time.time() - start_time), 5)))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Travel_Time'] = df['End Time'] - df['Start Time']
    print(df['Travel_Time'].sum(), ' - total travel time in the selected city, month and day.')
    # display mean travel time
    travel_time = df['Travel_Time'].mean()
    print(travel_time, ' - average time duration in the selected city, month and day.')
    print("This took %s seconds." % (round((time.time() - start_time), 5)))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    #  Display counts of user types
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    print('User type count in the selected city, month and day.')
    user_type = df['User Type'].value_counts()
    print(user_type.to_string(dtype=False))

    # Display counts of gender
    if 'Gender' in df.columns:
        print('\nGender count in the selected city, month and day.')
        gender = df.loc[:, 'Gender'].value_counts()
        print(gender.to_string(dtype=False), '\n')
    else:
        print('No gender data for this city available.')
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        df = df.dropna(axis=0)
        oldest = int(df['Birth Year'].min())
        print(oldest, ' -- is the birth year of the oldest customer in the selected city, month and day.')
        youngest = int(df['Birth Year'].max())
        print(youngest, ' -- is the birth year of the youngest customer in the selected city, month and day.')
        year_freq = df['Birth Year'].mode()
        print(int(year_freq[0]), ' -- is the birth year of most of the customers in the selected city, month and day.')
    else:
        print('No Birth year information for this city available.')
    print("This took %s seconds." % (round((time.time() - start_time), 5)))


def main():
    while True:
        city, month, day = get_filters()
        if city == 'exit' or month == 'exit' or day == 'exit':
            print('Evaluation stopped.')
            break
        else:
            df = load_data(city, 'all', 'all')
            load_raw_data(df)
            time_stats(df)
            df = load_data(city, month, day)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            restart = input('\nWould you like to restart? Enter yes or no.')
            if restart.lower() != 'yes':
                break
            else:
                print('Evaluation completed.')


if __name__ == "__main__":
    main()
