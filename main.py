import get_time
import get_data
import calc
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates
import pylab
from io import BytesIO
from pprint import pprint
import credentials
import requests

my_athlete_id = "19826138"
dad_athlete_id = "1140693"

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
    for n,x in enumerate(dataset):
        s = n+1
        dict_1[s] = {}
        dict_1[s]['id'] = x['id']
        dict_1[s]['name'] = str(x['firstname'])+" "+str(x['lastname'])
        list.append(x['id'])
    pprint(dict_1)
    return dict_1

friend_dict = my_friends(my_athlete_id)
starred_dict = get_starred_segments(my_athlete_id)

for seg in starred_dict: #for each segment in my starred list
    print(starred_dict[seg]['name'])
    seg_data = leaderboard(str(starred_dict[seg]['id'])) #find learderboard information
    print("ENTRY COUNT: "+str(seg_data['entry_count']))
    for x in seg_data['entries']:
        if str(my_athlete_id) == str(x['athlete_id']):
            print("YOUR RANK: "+str(x['rank']))
        for user in friend_dict:
            if friend_dict[user]['id'] == x['athlete_id']:
                print ("FRIEND "+str(friend_dict[user]['name'])+" RANK: "+str(x['rank']))
    print()
