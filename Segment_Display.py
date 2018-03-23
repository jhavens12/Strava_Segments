import get_time
import get_seg_data
import calc
import set_labels
from io import BytesIO
from pprint import pprint
import credentials
import requests
import datetime
from pathlib import Path
import pickle

import ui #used for pythonista
import console #used for pythonista

my_athlete_id = '19826138'
v = ui.load_view()
v.background_color = "#FC4C02" #strava orange
v.present(style='sheet', hide_title_bar=True)
v['Refresh'].title = "Loading..." #this works

dictionary_file = Path('./History.dict')

global old_dict

if dictionary_file.is_file():
    pickle_in = open(dictionary_file,"rb")
    old_dict = pickle.load(pickle_in)
else:
    f=open(dictionary_file,"w+") #create file
    f.close()
    old_dict = {}

def download_data():
    v['Refresh'].title = "Loading..."
    #gather new dictionary information
    starred_dict = get_seg_data.get_starred_segments(my_athlete_id)
    new_dict = get_seg_data.create_segment_dictionary(starred_dict)

    for new_seg in new_dict:
        for old_seg in old_dict:
            if new_seg == old_seg: #id matches
                if new_dict[new_seg]['Jonathan']['rank'] != old_dict[old_seg]['Jonathan']['rank']:#rank no longer matches
                    print("Rank has changed for: "+str(old_dict[old_seg]['information']['name'])) #print that it has changed
                    old_dict[old_seg]['Jonathan_old'] = old_dict[old_seg]['Jonathan'] #store old jonathan as jonathan_old
                    old_dict[old_seg]['Jonathan_old']['change_occurred'] = datetime.datetime.now() #timestamp it
        if new_seg not in old_dict: #what about if we star a new segment? need to save it to old_dict
            print("We have a new starred segment: "+str(new_dict[new_seg]['information']['name']))
            old_dict[new_seg] = new_dict[new_seg] #save new segment in old dict

    #do stuff in here for pythonista, set up the labels
    for seg in old_dict:
        if 'Jonathan_old' in old_dict[seg]:
            print("There is an old record for "+str(old_dict[old_seg]['information']['name']))

    #save to the history file - use OLD_DICT
    with open(dictionary_file, 'w') as outfile:
        #json.dump(history_dict, outfile)
        pickle_out = open(dictionary_file,"wb")
        pickle.dump(old_dict, pickle_out)
        pickle_out.close()

#display information down ehre

def refresh(sender):
    download_data()
    global button_dict #make global on each refresh
    button_dict = set_button_titles(v,old_dict)
    #button dict is buttonid as key and segid as value
    v['Refresh'].action = refresh #do refresh function
    v['Refresh'].title = "Refresh" #this works

def seg_button_pressed(sender):
    #takes sender.title (name) and sets labels based on that
    set_labels.set_200_series(v,old_dict,button_dict[sender.title])

def set_button_titles(v,old_dict):
    button_dict = {}
    #need button dict of name of segment and ID of segment
    for n,segment in enumerate(old_dict): #limit to number of labels somehow
        button_name = 'button'+str(n)
        label_title = str(old_dict[segment]['information']['name'])
        button_dict[label_title] = segment #save button with segment id
        v[button_name].title = label_title #set titles for buttons
        v[button_name].action = seg_button_pressed
    return button_dict

#setup variables

refresh("nothing") #runs initial setup
