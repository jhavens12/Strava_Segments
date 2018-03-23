import get_time
import calc
from io import BytesIO
from pprint import pprint
import credentials
import requests
import datetime

#my_athlete_id = "19826138"
my_athlete_name = 'Jonathan H.'
dad_athlete_id = "1140693"
dan_athlete_name = 'Danielle C.'
test_id = '15600558'

friend_list = ['Danielle C.']

# starred_dict = get_starred_segments(my_athlete_id)
# final_dict = create_segment_dictionary(starred_dict)
# print_stats(final_dict)

def get_starred_segments(athlete_id):
    url = 'https://www.strava.com/api/v3/athletes/'+athlete_id+'/segments/starred'
    header = {'Authorization': 'Bearer '+credentials.api_key}
    param = {'per_page':200, 'page':1}
    dataset = requests.get(url, headers=header, params=param).json()
    dict_1 = {}
    list_1 = []
    for n,x in enumerate(dataset):
        s = n+1
        dict_1[s] = {}
        dict_1[s]['id'] = x['id']
        dict_1[s]['name'] = x['name']
        dict_1[s]['city'] = x['city']
        list_1.append(x['id'])
    return dict_1

def get_segment_info(seg_id):
    url = 'https://www.strava.com/api/v3/segments/'+seg_id
    header = {'Authorization': 'Bearer '+credentials.api_key}
    param = {'per_page':200, 'page':1}
    dataset = requests.get(url, headers=header, params=param).json()
    return dataset

def leaderboard(seg_id):
    url = 'https://www.strava.com/api/v3/segments/'+seg_id+'/leaderboard'
    header = {'Authorization': 'Bearer '+credentials.api_key}
    param = {'per_page':200, 'page':1}
    dataset = requests.get(url, headers=header, params=param).json()
    count = len(dataset['entries'])
    if dataset['entry_count'] < 200:
        return dataset
    else:
        page = 1
        while count < dataset['entry_count']:
            page = page + 1
            param = {'per_page':200, 'page':page}
            dataset_part = requests.get(url, headers=header, params=param).json()
            if dataset_part:
                dataset['entries'] = dataset['entries'] + dataset_part['entries']
            count = len(dataset['entries'])
        return dataset

def segment_efforts(athlete_id):
    url = 'https://www.strava.com/api/v3/segment_efforts/'+athlete_id
    header = {'Authorization': 'Bearer '+credentials.api_key}
    param = {'per_page':200, 'page':1}
    dataset = requests.get(url, headers=header, params=param).json()
    print("SEGMENT EFFORTS")
    pprint(dataset)

def my_friends(athlete_id):
    url = 'https://www.strava.com/api/v3/athletes/'+athlete_id+'/friends'
    header = {'Authorization': 'Bearer '+credentials.api_key}
    param = {'per_page':200, 'page':1}
    dataset = requests.get(url, headers=header, params=param).json()
    dict_1 = {}
    list = []
    pprint(dataset)
    for n,x in enumerate(dataset):
        s = n+1
        dict_1[s] = {}
        dict_1[s]['id'] = x['id']
        dict_1[s]['name'] = str(x['firstname'])+" "+str(x['lastname'])
        list.append(x['id'])
    #pprint(dict_1)
    return dict_1

def seconds_format(elapsed):
    return datetime.timedelta(seconds=elapsed)

def convert_timestamp(i):
    return datetime.datetime.strptime(i, "%Y-%m-%dT%H:%M:%SZ")

def create_segment_dictionary(starred_dict):
    final_dict = {}
    for seg in starred_dict: #for each segment in my starred list

        seg_data = leaderboard(str(starred_dict[seg]['id'])) #find learderboard information

        final_dict[starred_dict[seg]['id']] = {}
        final_dict[starred_dict[seg]['id']]['information'] = get_segment_info(str(starred_dict[seg]['id']))
        final_dict[starred_dict[seg]['id']]['name'] = starred_dict[seg]['name']
        final_dict[starred_dict[seg]['id']]['entries'] = seg_data['entry_count']
        try:
            final_dict[starred_dict[seg]['id']]['cr'] = seg_data['entries'][0] #set up course record dict
        except Exception:
            print("Segment does not have any data yet loaded")
            final_dict[starred_dict[seg]['id']]['cr'] = {}
            final_dict[starred_dict[seg]['id']]['cr']['elapsed_time'] = 0
            final_dict[starred_dict[seg]['id']]['cr']['start_date_local'] = "1990-1-1T12:00:00Z"

        final_dict[starred_dict[seg]['id']]['cr']['hms'] = \
            seconds_format(final_dict[starred_dict[seg]['id']]['cr']['elapsed_time'])
        final_dict[starred_dict[seg]['id']]['cr']['start_time'] = \
            convert_timestamp(final_dict[starred_dict[seg]['id']]['cr']['start_date_local'])

        #set up Jonathan dictionary
        for x in seg_data['entries']:
            if str(my_athlete_name) == str(x['athlete_name']):
                final_dict[starred_dict[seg]['id']]['Jonathan'] = x
        try:
            final_dict[starred_dict[seg]['id']]['Jonathan']['hms'] = \
                    seconds_format(final_dict[starred_dict[seg]['id']]['Jonathan']['elapsed_time']) #nice format time
            final_dict[starred_dict[seg]['id']]['Jonathan']['start_time'] = \
                    convert_timestamp(final_dict[starred_dict[seg]['id']]['Jonathan']['start_date_local'])
        except Exception:
            print("Segment does not have Jonathan data")
            final_dict[starred_dict[seg]['id']]['Jonathan`'] = {}
            final_dict[starred_dict[seg]['id']]['Jonathan']['elapsed_time'] = 0
            final_dict[starred_dict[seg]['id']]['Jonathan']['rank'] = 0
            final_dict[starred_dict[seg]['id']]['Jonathan']['start_date_local'] = "1990-1-1T12:00:00Z"

        for friend in friend_list: #set up to loop through to add information for each friend
            #print("search for friend name, create nested dictionary for each")
            pass

    return final_dict

def print_stats(final_dict):
    for segment in final_dict:
        print()
        print("Segment: "+str(final_dict[segment]['information']['name']))
        print("My Time: "+str(final_dict[segment]['Jonathan']['hms']))
        print("CR: "+str(final_dict[segment]['cr']['hms']))
        print("Set On: "+str(final_dict[segment]['cr']['start_time']))
        print("Behind by: "+str(final_dict[segment]['Jonathan']['hms'] - final_dict[segment]['cr']['hms']))
        print("My Rank: "+str(final_dict[segment]['Jonathan']['rank'])+" Out of "+str(final_dict[segment]['entries']))
        print("Set On: "+str(final_dict[segment]['Jonathan']['start_time']))
        print(str(final_dict[segment]['information']['athlete_segment_stats']['effort_count'])+ " Attempts")
