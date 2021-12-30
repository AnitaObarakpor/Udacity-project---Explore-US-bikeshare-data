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
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        cities = ['chicago', 'new york city', 'washington']
        city = input("\n Which city would you like to analyse? (Chicago, New york city, Washington) \n").lower()
        if city in cities:
            print("\nYou have chosen {} as your city.".format(city.title()))
            break
        else:
            print("\n Invalid input. Please enter a valid city name.")    

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        months= ['January','February','March','April','May','June','All']
        month = input("\n Which month would you like to consider? (January, February, March, April, May, June)? Type 'All' for no month filter\n").title()
        if month in months:
            print("\nYou have chosen {} as your month.".format(month))
            break
        else:
            print("\n Invalid input. Please enter a valid month")    

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days= ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All']
        day = input("\n Which day of the week would you like to consider? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)? Type 'All' for no day filter \n").title()         
        if day in days:
            print("\nYou have chosen {} as your day of the week.".format(day))
            break
        else:
            print("\n Invalid input! Please enter a valid day") 

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

    # extract month,day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month] 

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print("The most common month is {}.".format(popular_month))

    # TO DO: display the most common day of week
    popular_dow = df['day_of_week'].mode()[0]
    print("The most common day of the week is {}.".format(popular_dow))
             
    # TO DO: display the most common start hour
    popular_start_hour = df['hour'].mode()[0]
    print("The most common start hour is {}.".format(popular_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station= df['Start Station'].mode()[0]
    print("The most commonly used Start Station is {}.".format(popular_start_station))

    # TO DO: display most commonly used end station
    popular_end_station= df['End Station'].mode()[0]
    print("The most commonly used End Station is {}.".format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['Trip Route']=df['Start Station'] + " " + "to" + " "+ df['End Station']
    popular_route = df['Trip Route'].mode()[0]
    print("The most frequent combination of Start and End Station is {}.".format(popular_route))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    #calculate duration in minutes and seconds
    minute,second = divmod(total_travel_time,60)
    #calculate duration in hours and minutes
    hour,minute = divmod(minute,60)
    print("The total trip duration is {} hour(s), {} minute(s) and {} second(s).".format(hour,minute,second))

    # TO DO: display mean travel time
    avg_travel_time = round(df['Trip Duration'].mean())
    minute,second = divmod(avg_travel_time,60)
    if minute > 60:
        hour,minute =divmod(minute,60)
        print("The total trip duration: {} hour(s), {} minute(s) and {} second(s).".format(hour,minute,second))
    else:
        print("The total trip duration: {} minute(s) and {} second(s).".format(minute,second))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_count= df['User Type'].value_counts()
    print("\nThe number of users by type is: \n{}".format(user_type_count))

    # Display counts of gender
    # The try clause ensures only files containing a 'gender' column are displayed
    try: 
        gender_count= df['Gender'].value_counts()
        print("\nThe number of users by gender is:\n{}".format(gender_count))
    except:
        print("\nThere is no 'Gender' column in this file.")
             
    # Display earliest, most recent, and most common year of birth 
    # Try clause ensures only files with column 'birth year' are displayed
    try:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print("\nThe earliest birth occurred inn {}.".format(earliest))
        print("\nThe most recent birth occurred in {}.".format(most_recent))
        print("\nThe most common birth year is {}.".format(most_common_year))
    except:
        print("\nThere are no 'Birth Year' details in this file.")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def display_data(df):
    """Displays 5 rows of data from the file for the selected city"""
    
    while True:
        valid_response = ['yes','no']
        response = input("Would you like to view individual trip data (5 entries)? Enter 'yes' or 'no'\n").lower()
        if response in valid_response:
            if response == 'yes':
                start=0
                end=5
                trip_data = df.iloc[start:end,:9]
                print(trip_data)
            break     
        else:
            print("Please enter a valid response")
    if  response == 'yes':       
            while True:
                response_again = input("Would you like to view more trip data? Enter 'yes' or 'no'\n").lower()
                if response_again in valid_response:
                    if response_again == 'yes':
                        start += 5
                        end += 5
                        trip_data = df.iloc[start:end,:9]
                        print(trip_data)
                    else:    
                        break  
                else:
                    print("Please enter a valid response")  

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


if __name__ == "__main__":
	main()
