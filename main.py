from io import BytesIO
from pprint import pprint
import credentials
import requests
import pickle
from pathlib import Path

my_athlete_id = "19826138"
dad_athlete_id = "1140693"

def get_starred_segments(athlete_id): #get user starred segments
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

def leaderboard(seg_id): #return dictionary of leaderboard for segment
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

def my_friends(athlete_id): #return dictionary of friends
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

def leaderboard_matches(seg_data,friend_dict):
    #return a dictionary with a single segment data with friend and user data
    seg_dict = {}
    seg_dict['athletes'] = {}
    for x in seg_data['entries']: #for user listed in leaderboard for segment
        if str(my_athlete_id) == str(x['athlete_id']):
            seg_dict['athletes'][str(my_athlete_id)] = {}
            seg_dict['athletes'][my_athlete_id]['rank'] = x['rank']
            seg_dict['athletes'][my_athlete_id]['elapsed_time'] = x['elapsed_time']

        for user in friend_dict:
            if friend_dict[user]['id'] == x['athlete_id']:
                seg_dict['athletes'][friend_dict[user]['id']] = {}
                seg_dict['athletes'][friend_dict[user]['id']]['rank'] = x['rank']
                seg_dict['athletes'][friend_dict[user]['id']]['elapsed_time'] = x['elapsed_time']
    return seg_dict

def compare_record(record_dict,new_record_dict):
    print("NA")
    #remove any entries (segments) that aren't in one another
    #for each segments
    #if my user id exists
    for segment in record_dict:
        if len(record_dict[segment]['athletes']) > 1:
            for athlete1 in record_dict[segment]['athletes']:
                for athlete2 in new_record_dict[segment]['athletes']:

                    print(record_dict[segment]['athletes'][athlete1])
                    print(new_record_dict[segment]['athletes'][athlete2])




new_record_dict = {}
friend_dict = my_friends(my_athlete_id)
starred_dict = get_starred_segments(my_athlete_id)

for n,seg in enumerate(starred_dict): #for each segment in my starred list
    seg_count = n+1
    new_record_dict[starred_dict[seg]['id']] = {} #create new dictionary to store data with seg ID as key

    seg_data = leaderboard(str(starred_dict[seg]['id'])) #find learderboard information from single segment
    seg_dict = leaderboard_matches(seg_data,friend_dict) #create dict based on your id and friends list

    new_record_dict[starred_dict[seg]['id']] = seg_dict #adds segment dict to main dictionary as segment id as key
    new_record_dict[starred_dict[seg]['id']]['name'] = starred_dict[seg]['name'] #set segment name in new dictionary

#pprint(new_record_dict)
#####
record_file = Path("./record.dict")
if record_file.is_file():
#pricing import
    pickle_in = open("record.dict","rb")
    record_dict = pickle.load(pickle_in)

    compare_record(record_dict,new_record_dict)

    record_dict = new_record_dict

    pickle_out = open("record.dict","wb")
    pickle.dump(record_dict, pickle_out)
    pickle_out.close()

else:
    f=open("record.dict","w+") #create file
    f.close()

    record_dict = new_record_dict #create limits dict and variables

    pickle_out = open("record.dict","wb") #open file
    pickle.dump(record_dict, pickle_out) #save limits dict to file
    pickle_out.close()
#####
