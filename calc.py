#v1.2
#This is the main file unless I made a mistake
import time
import datetime
from datetime import date
import get_time
from pprint import pprint

def full_running_totals(dictionary1,days,unit):
    #creadted for use with master_dict
    #newest and working
    #limit days after this calculation for range
    #Creates running totals for each day - not just activity day
    calculation_range_time = []
    final_list = []
    dictionary = dictionary1.copy()
    x = days
    #time functions
    now = datetime.datetime.now()
    start_of_today = datetime.datetime(now.year, now.month, now.day, hour=0, minute=0, second=0)
    end_of_today = datetime.datetime(now.year, now.month, now.day, hour=23, minute=59, second=59)

    difference = start_of_today - get_time.forever() #fix start peroid

    calculation_range = list(range(0,(difference.days +1))) #creates list from past date(given) to current date
    calculation_range_rev = list(reversed(calculation_range))
    calculation_range_time = [end_of_today - datetime.timedelta(days=x) for x in range(0,(difference.days +1))]

    for i,f in zip(calculation_range_time,calculation_range): #for every calculation day ex 1,2,3,4,5 back
        dictionary_1 = dictionary.copy() #create a new dictionary
        oldest_time = end_of_today - (datetime.timedelta(days=(x+f)))
        for key in list(dictionary_1):
            if key > i:
                del dictionary_1[key] #delete keys newer than calculation day
        for key in list(dictionary_1):
            if key < oldest_time: #delete keys older than oldest time
                 del dictionary_1[key]
        value_list = []
        for key in dictionary_1:
            value_list.append(float(dictionary_1[key][unit])) #adds variables to list
        list_sum = sum(value_list)
        final_list.append(list_sum)
    new_date_list = []
    for i in calculation_range: #create list of days going backwards from today
        new_day = get_time.day(i)
        new_date_list.append(new_day)
    new_dict = dict(zip(new_date_list, final_list))
    return new_dict

def monthly_daily_totals(dictionary,time_input,unit_input):
    #for use with masterdict (get_data.my_filtered_activities())
    #01.29.18
    #takes in number for how many months ago. Ex 0 is current, 1 is last month
    x_list = []
    y_list = []

    #filters out only dates needed
    for key in list(dictionary):
        if key < get_time.FOM(time_input): #if older than first of month
            del dictionary[key]
    for key in list(dictionary):
       if key > get_time.LOM(time_input): #if newer than first of month
           del dictionary[key]

    calculation_day_count = (get_time.LOM(time_input) - get_time.FOM(time_input)).days #how many days in the month
    calculation_day_range = list(range(1,calculation_day_count+2)) #range of 1 to the days in the month - calculation days

    mile_count = 0
    mile_count_list = [] #list of miles
    day_count_list = [] #list of days miles occurred
    for day in calculation_day_range:  #ex 1-31
        for activity in dictionary:
            if activity.day == day: #if the day of the activity matches the day in the list
                mile_count = mile_count + float(dictionary[activity][unit_input])
                mile_count_list.append(mile_count) #add mile count
                day_count_list.append(activity.day) #add day that count occurs

    return dict(zip(day_count_list,mile_count_list))

def yearly_totals(dictionary,years_ago):
    #0 = this year
    #1 = last year
    #returns days of year as keys (1-365)
    now = datetime.datetime.now()
    start_of_year = datetime.datetime((now.year - years_ago), 1, 1)
    end_of_year = datetime.datetime((now.year - years_ago), 12, 31)

    for key in list(dictionary):
        if key < start_of_year: #if older than first of month
            del dictionary[key]
    for key in list(dictionary):
       if key > end_of_year: #if newer than first of month
           del dictionary[key]

    calculation_day_count = (end_of_year - start_of_year).days #how many days in the month
    calculation_day_range = list(range(1,calculation_day_count+2)) #range of 1 to the days in the month - calculation days

    mile_count = 0
    mile_count_list = [] #list of miles
    day_count_list = [] #list of days miles occurred
    for day in calculation_day_range:  #ex 1-31
        for activity in dictionary:
            if activity.timetuple().tm_yday == day: #if the day of the activity matches the day in the list
                mile_count = mile_count + float(dictionary[activity]['distance_miles'])
                mile_count_list.append(mile_count) #add mile count
                day_count_list.append(activity.timetuple().tm_yday) #add day that count occurs

    return dict(zip(day_count_list,mile_count_list))

def yearly_totals_dates(dictionary,years_ago):
    #0 = this year
    #1 = last year
    #returns event dates as keys (datetime objects)
    #used only for creating trendline
    now = datetime.datetime.now()
    start_of_year = datetime.datetime((now.year - years_ago), 1, 1)
    end_of_year = datetime.datetime((now.year - years_ago), 12, 31)

    for key in list(dictionary):
        if key < start_of_year: #if older than first of month
            del dictionary[key]
    for key in list(dictionary):
       if key > end_of_year: #if newer than first of month
           del dictionary[key]

    calculation_day_count = (end_of_year - start_of_year).days #how many days in the month
    calculation_day_range = list(range(1,calculation_day_count+2)) #range of 1 to the days in the month - calculation days

    mile_count = 0
    mile_count_list = [] #list of miles
    day_count_list = [] #list of days miles occurred
    for day in calculation_day_range:  #ex 1-31
        for activity in dictionary:
            if activity.timetuple().tm_yday == day: #if the day of the activity matches the day in the list
                mile_count = mile_count + float(dictionary[activity]['distance_miles'])
                mile_count_list.append(mile_count) #add mile count
                #print(activity)
                day_count_list.append(activity) #add datetime object as key

    return dict(zip(day_count_list,mile_count_list))
###########
#OLD
###########

def filter_by_username(dataset,user):
    #filters out strava by username, type and 0.0 distance removed
    keys1 = []
    values1 = []
    for i in dataset:
        if i['athlete']['username'] == user:
            if i['type'] == 'Run':
                if i['distance'] != 0.0:
                    keys1.append(i['start_date_local'])
                    values1.append(i['distance'])
    keys2 = convert_timestamps(keys1)
    new_dictionary = merge_lists(keys2,values1)
    return new_dictionary

def filter(dataset):
    #used for strava activites that do not require a username
    #return dictionary time + distance and time + pace
    keys1 = []
    distance1 = []
    elapsed1 = []
    elevation1 = []
    av_heartrate1 = []
    mx_heartrate1 = []
    title = []
    for i in dataset:
        if i['type'] == 'Run':
            if i['distance'] != 0.0:
                keys1.append(i['start_date_local'])
                distance1.append(i['distance'])
                elapsed1.append(i['elapsed_time'])
                elevation1.append(i['total_elevation_gain'])
                title.append(i['name'])
                if i['has_heartrate'] == True:
                    av_heartrate1.append(i['average_heartrate'])
                    mx_heartrate1.append(i['max_heartrate'])
                else:
                    av_heartrate1.append(0)
                    mx_heartrate1.append(0)
    pace2 = convert_pace(distance1,elapsed1)
    keys2 = convert_timestamps(keys1)
    elapsed2 = convert_seconds_to_minutes(elapsed1) #
    elevation2 = convert_elevation(elevation1) #

    dict_time_title = merge_lists(keys2,title)
    dict_time_elapsed = merge_lists(keys2,elapsed2)
    dict_time_elevation = merge_lists(keys2,elevation2)
    dict_time_av_heartrate = merge_lists(keys2,av_heartrate1)
    dict_time_mx_heartrate = merge_lists(keys2,mx_heartrate1)
    dict_time_dist = merge_lists(keys2,distance1)
    dict_time_pace = merge_lists(keys2,pace2)
    return dict_time_dist,dict_time_pace,dict_time_elapsed,dict_time_elevation,dict_time_av_heartrate,dict_time_mx_heartrate,dict_time_title

def solo_filter(dataset):
    #used for strava activites that do not require a username
    #return dictionary time + distance and time + pace
    keys1 = []
    distance1 = []
    elapsed1 = []
    for i in dataset:
        if i['type'] == 'Run':
            if i['distance'] != 0.0:
                if i['athlete_count'] == 1:
                    keys1.append(i['start_date_local'])
                    distance1.append(i['distance'])
                    elapsed1.append(i['elapsed_time'])
    pace2 = convert_pace(distance1,elapsed1)
    keys2 = convert_timestamps(keys1)
    dict_time_dist = merge_lists(keys2,distance1)
    dict_time_pace = merge_lists(keys2,pace2)
    return dict_time_dist,dict_time_pace

def partner_filter(dataset):
    #used for strava activites that do not require a username
    #return dictionary time + distance and time + pace
    keys1 = []
    distance1 = []
    elapsed1 = []
    for i in dataset:
        if i['type'] == 'Run':
            if i['distance'] != 0.0:
                if i['athlete_count'] > 1:
                    keys1.append(i['start_date_local'])
                    distance1.append(i['distance'])
                    elapsed1.append(i['elapsed_time'])
    pace2 = convert_pace(distance1,elapsed1)
    keys2 = convert_timestamps(keys1)
    dict_time_dist = merge_lists(keys2,distance1)
    dict_time_pace = merge_lists(keys2,pace2)
    return dict_time_dist,dict_time_pace

def convert_elevation(elevation_list):
    #converts list of metric elevations to imperial
    new_elevation_list = []
    for i in elevation_list:
        new_elevation =("{0:.2f}".format(i*3.28))
        new_elevation_list.append(new_elevation)
    return new_elevation_list

def convert_seconds_to_minutes(elapsed_list):
    #converts seconds to minutes/seconds for elapsed time
    new_elapsed_list = []
    for i in elapsed_list:
        new_elapsed = datetime.timedelta(seconds=i)
        new_elapsed_list.append(new_elapsed)
    return new_elapsed_list

def convert_timestamps(time_list):
    #converts strava time to datetime format
    new_time_list = []
    for i in time_list:
        new_stamp = datetime.datetime.strptime(i, "%Y-%m-%dT%H:%M:%SZ")
        #unix = time.mktime(datetime.datetime.strptime(i, "%Y-%m-%dT%H:%M:%SZ").timetuple())
        #unix_int = int(unix)
        new_time_list.append(new_stamp)
    return new_time_list

def convert_pace(distance,elapsed):
    minutes_list = []
    miles_list = []
    pace_decimal_list = []
    #convert time to minutes (from seconds)
    #convert distance to miles (from meters)
    for i in elapsed:
        minutes = i/60
        minutes_list.append(minutes)
    for i in distance:
        miles = i * 0.00062137
        miles_list.append(miles)
    for min,mile in zip(minutes_list,miles_list):
        pace = min/mile
        pace_decimal_list.append(pace)
    return pace_decimal_list

def convert_dec_time(dec):
    #converts decimal time to readable time format
    Minutes = dec
    Seconds = 60 * (Minutes % 1)
    result = ("%d:%02d" % (Minutes, Seconds))
    return result

def convert_unix_time(var):
    x = datetime.datetime.fromtimestamp(var).strftime('%Y-%m-%d %H:%M:%S')
    y = datetime.datetime.fromtimestamp(var).strftime('%Y-%m-%d')
    return y

def meters_to_miles(meters):
    meters_int = int(meters)
    miles1 = meters_int * 0.000621371
    miles2 = ("{0:.2f}".format(miles1))
    return miles2

def merge_lists(keys,values):
    dictionary = dict(zip(keys, values))
    return dictionary

def activity_count(dictionary):
    #counts amount of keys in dictionary
    amount = len(dictionary.keys())
    amount_str = str(amount)
    return amount_str

def purge_dictionary_miles(dictionary,time):
    #compares strava dict to time to remove unwanted activities
    #returns miles for time
    for key in list(dictionary):
        if key < time:
            del dictionary[key]
    value_list = (dictionary.values())
    meters = sum(value_list)
    miles = meters_to_miles(meters)
    miles_str = str(miles)
    return miles

def purge_dictionary_pace(dictionary,time):
        #returns average pace of the average paces of each runs
        #does NOT return average of all of the miles individually
    for key in list(dictionary):
        if key < time:
            del dictionary[key]
    value_list = (dictionary.values())
    #creates a list of average times based on input date
    total_pace = sum(value_list)
    list_length = len(value_list)
    if list_length != 0:
        average_pace_dec = total_pace/list_length
        average_pace_time = convert_dec_time(average_pace_dec)
        average_pace_time_str = str(average_pace_time)
        return average_pace_time_str
    elif list_length == 0:
        result = str(0)
        return result

def purge_dictionary_pace_double(dictionary,time1,time2):
    if time1 > time2:
        newer_time = time1
        older_time = time2
    if time2 > time1:
        older_time = time1
        newer_time = time2
    for key in list(dictionary):
        if key < older_time:
            del dictionary[key]
    for key in list(dictionary):
        if key > newer_time:
            del dictionary[key]
    value_list = (dictionary.values())
    #creates a list of average times based on input date
    total_pace = sum(value_list)
    list_length = len(value_list)
    if list_length != 0:
        average_pace_dec = total_pace/list_length
        average_pace_time = convert_dec_time(average_pace_dec)
        average_pace_time_str = str(average_pace_time)
        return average_pace_time_str
    elif list_length == 0:
        result = str(0)
        return result

def purge_dictionary_miles_double(dictionary,time1,time2):
    #compares an older time and newer time to dictionary to remove values
        #used for calculating yesterdays week or month etc
    if time1 > time2:
        newer_time = time1
        older_time = time2
    if time2 > time1:
        older_time = time1
        newer_time = time2
    for key in list(dictionary):
        if key < older_time:
            del dictionary[key]
    for key in list(dictionary):
        if key > newer_time:
            del dictionary[key]
    value_list = (dictionary.values())
    meters = sum(value_list)
    miles = meters_to_miles(meters)
    return miles

###
def convert_unix_time_day(var):
    x = datetime.datetime.fromtimestamp(var).strftime('%Y-%m-%d %H:%M:%S')
    y = datetime.datetime.fromtimestamp(var).strftime('%Y-%m-%d')
    z = datetime.datetime.fromtimestamp(var).strftime('%d')
    return z

def convert_unix_time_year_month_day(var):
    x = datetime.datetime.fromtimestamp(var).strftime('%Y-%m-%d %H:%M:%S')
    y = datetime.datetime.fromtimestamp(var).strftime('%Y-%m-%d')
    z = datetime.datetime.fromtimestamp(var).strftime('%d')
    return y

def year_month_day(var):
    #takes datetime object and returns string formatted
    x = str((var.year))+"."+str((var.month))+"."+str((var.day))
    return x

def month_day(var):
    #takes datetime object and returns string formatted
    x = str((var.month))+"."+str((var.day))
    return x

#####
def running_totals_single(dictionary1,days,date):
    calculation_range_time = []
    final_list = []

    dictionary = dictionary1.copy()
    x = days

    #time functions
    now = datetime.datetime.now()
    start_of_today = datetime.datetime(now.year, now.month, now.day, hour=0, minute=0, second=0)
    end_of_today = datetime.datetime(now.year, now.month, now.day, hour=23, minute=59, second=59)
    difference = start_of_today - date

    calculation_range = list(range(0,(difference.days +1))) #creates list from past date(given) to current date
    calculation_range_rev = list(reversed(calculation_range))
    calculation_range_time = [end_of_today - datetime.timedelta(days=x) for x in range(0,(difference.days +1))]

    for i,f in zip(calculation_range_time,calculation_range): #for every calculation day ex 1,2,3,4,5 back
        dictionary_1 = dictionary.copy() #create a new dictionary
        oldest_time = end_of_today - (datetime.timedelta(days=(x+f)))
        for key in list(dictionary_1):
            if key > i:
                del dictionary_1[key] #delete keys newer than calculation day
        for key in list(dictionary_1):
            if key < oldest_time: #delete keys older than oldest time
                 del dictionary_1[key]

        value_list = (dictionary_1.values()) #grabs x values from list
        meters = sum(value_list)
        miles = meters_to_miles(meters)
        final_list.append(miles)

    new_dict = dict(zip(calculation_range_rev, final_list))
    return new_dict

def running_totals_double(dictionary1,days,date1,date2):
    calculation_range_time = []
    final_list = []

    dictionary = dictionary1.copy()
    x = days

    if date1 > date2:
        newer_time = date1
        older_time = date2
    if date2 > date1:
        older_time = date1
        newer_time = date2

    #time functions
    now = datetime.datetime.now()
    start_of_today = datetime.datetime(now.year, now.month, now.day, hour=0, minute=0, second=0)
    end_of_today = datetime.datetime(now.year, now.month, now.day, hour=23, minute=59, second=59)
    difference_newer = now - newer_time
    difference_older = now - older_time

    calculation_range = list(range(difference_newer.days +1,difference_older.days +1)) #creates list from past date(given) to current date
    calculation_range_rev = list(reversed(calculation_range))
    calculation_range_time = [end_of_today - datetime.timedelta(days=x) for x in range(difference_newer.days +1,difference_older.days +1)]
    print(calculation_range_time)


    for i,f in zip(calculation_range_time,calculation_range): #for every calculation day ex 1,2,3,4,5 back
        dictionary_1 = dictionary.copy() #create a new dictionary
        oldest_time = end_of_today - (datetime.timedelta(days=(x+f)))
        for key in list(dictionary_1):
            if key > i:
                del dictionary_1[key] #delete keys newer than calculation day
        for key in list(dictionary_1):
            if key < oldest_time: #delete keys older than oldest time
                 del dictionary_1[key]
        value_list = (dictionary_1.values()) #grabs x values from list
        meters = sum(value_list)
        miles = meters_to_miles(meters)
        final_list.append(miles)

    new_dict = dict(zip(calculation_range_rev, final_list)) #creates new dictionary
    return new_dict

def var_calc_loop_single(time_function,sub_dataset):

    keys = ['miles','count','pace','solo_miles','solo_count','solo_pace','partner_miles','partner_count','partner_pace','date']
    values = []

    dict_time_distance,dict_time_pace,dict_time_elapsed,dict_time_elevation,dict_time_av_heartrate,dict_time_mx_heartrate = filter(sub_dataset)
    #filters my_dataset to create two dictionaries as above, but only containes solo runs
    dict_time_distance_solo,dict_time_pace_solo = solo_filter(sub_dataset)
    #same as above but only runs containing 2 or more people running
    dict_time_distance_partner,dict_time_pace_partner = partner_filter(sub_dataset)

    name_miles = purge_dictionary_miles(dict_time_distance,time_function)
    values.append(name_miles)
    name_count = activity_count(dict_time_distance)
    values.append(name_count)
    name_pace = purge_dictionary_pace(dict_time_pace,time_function)
    values.append(name_pace)

    name_solo_miles = purge_dictionary_miles(dict_time_distance_solo,time_function)
    values.append(name_solo_miles)
    name_solo_count = activity_count(dict_time_distance_solo)
    values.append(name_solo_count)
    name_solo_pace = purge_dictionary_pace(dict_time_pace_solo,time_function)
    values.append(name_solo_pace)

    name_partner_miles = purge_dictionary_miles(dict_time_distance_partner,time_function)
    values.append(name_partner_miles)
    name_partner_count = activity_count(dict_time_distance_partner)
    values.append(name_partner_count)
    name_partner_pace = purge_dictionary_pace(dict_time_pace_partner,time_function)
    values.append(name_partner_pace)

    st1 = str(time_function.month)
    st2 = str(time_function.day)
    st3 = str(time_function.year)

    date = (st1+"."+st2+"."+st3)

    values.append(date)

    new_dictionary = merge_lists(keys,values)
    #print(new_dictionary)
    return(new_dictionary)
    #return name_miles,name_count,name_pace,name_solo_miles,name_solo_count,name_solo_pace,name_partner_miles,name_partner_count,name_partner_pace

def var_calc_loop_double(time_function1,time_function2,sub_dataset):

    keys = ['miles','count','pace','solo_miles','solo_count','solo_pace','partner_miles','partner_count','partner_pace','date']
    values = []

    dict_time_distance,dict_time_pace = filter(sub_dataset)
    #filters my_dataset to create two dictionaries as above, but only containes solo runs
    dict_time_distance_solo,dict_time_pace_solo = solo_filter(sub_dataset)
    #same as above but only runs containing 2 or more people running
    dict_time_distance_partner,dict_time_pace_partner = partner_filter(sub_dataset)

    name_miles = purge_dictionary_miles_double(dict_time_distance,time_function1,time_function2)
    values.append(name_miles)
    name_count = activity_count(dict_time_distance)
    values.append(name_count)
    name_pace = purge_dictionary_pace_double(dict_time_pace,time_function1,time_function2)
    values.append(name_pace)

    name_solo_miles = purge_dictionary_miles_double(dict_time_distance_solo,time_function1,time_function2)
    values.append(name_solo_miles)
    name_solo_count = activity_count(dict_time_distance_solo)
    values.append(name_solo_count)
    name_solo_pace = purge_dictionary_pace_double(dict_time_pace_solo,time_function1,time_function2)
    values.append(name_solo_pace)

    name_partner_miles = purge_dictionary_miles_double(dict_time_distance_partner,time_function1,time_function2)
    values.append(name_partner_miles)
    name_partner_count = activity_count(dict_time_distance_partner)
    values.append(name_partner_count)
    name_partner_pace = purge_dictionary_pace_double(dict_time_pace_partner,time_function1,time_function2)
    values.append(name_partner_pace)

    if time_function1 > time_function2:
        newer_time = time_function1
        older_time = time_function2
    if time_function2 > time_function1:
        older_time = time_function1
        newer_time = time_function2

    st1 = str(older_time.month)
    st2 = str(older_time.day)
    st3 = str(newer_time.month)
    st4 = str(newer_time.day)
    st5 = str(older_time.year)
    st6 = str(newer_time.year)

    date = (st1+"."+st2+"."+st5+" - "+st3+"."+st4+"."+st6)
    values.append(date)

    new_dictionary = merge_lists(keys,values)
    print(new_dictionary)
    return(new_dictionary)

    #return name_miles,name_count,name_pace,name_solo_miles,name_solo_count,name_solo_pace,name_partner_miles,name_partner_count,name_partner_pace

###
#NEWEST FUNCTIONS HERE
def all_running_totals(dictionary1,days):
    #used by Noteables2 to get dictionary of running totals and datetime for keys
    calculation_range_time = []
    final_list = []

    dictionary = dictionary1.copy()
    x = days

    #time functions
    now = datetime.datetime.now()
    start_of_today = datetime.datetime(now.year, now.month, now.day, hour=0, minute=0, second=0)
    end_of_today = datetime.datetime(now.year, now.month, now.day, hour=23, minute=59, second=59)
    difference = start_of_today - get_time.FOY()

    calculation_range = list(range(0,(difference.days +1))) #creates list from past date(given) to current date
    calculation_range_rev = list(reversed(calculation_range))
    calculation_range_time = [end_of_today - datetime.timedelta(days=x) for x in range(0,(difference.days +1))]

    for i,f in zip(calculation_range_time,calculation_range): #for every calculation day ex 1,2,3,4,5 back
        dictionary_1 = dictionary.copy() #create a new dictionary
        oldest_time = end_of_today - (datetime.timedelta(days=(x+f)))
        for key in list(dictionary_1):
            if key > i:
                del dictionary_1[key] #delete keys newer than calculation day
        for key in list(dictionary_1):
            if key < oldest_time: #delete keys older than oldest time
                 del dictionary_1[key]

        value_list = (dictionary_1.values()) #grabs x values from list
        meters = sum(value_list)
        miles = meters_to_miles(meters)
        final_list.append(float(miles))
    #new_dict = dict(zip(calculation_range_rev, final_list))
    new_date_list = []
    for i in calculation_range: #create list of days going backwards from today
        new_day = get_time.day(i)
        new_date_list.append(new_day)
    #print(final_list)
    new_dict = dict(zip(new_date_list, final_list))
    return new_dict

####

def format(i):
    return float(("{0:.2f}".format(i)))
