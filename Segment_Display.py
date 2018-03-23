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

my_athlete_id = "19826138"
dad_athlete_id = "1140693"

dictionary_file = Path('./History.dict')

if dictionary_file.is_file():
    pickle_in = open(dictionary_file,"rb")
    old_dict = pickle.load(pickle_in)
else:
    f=open(dictionary_file,"w+") #create file
    f.close()
    old_dict = {}

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

#set labels for pythonista?
#set_labels.set_100_series()
#get_seg_data.print_stats(old_dict)

#save to the history file - use OLD_DICT
with open(dictionary_file, 'w') as outfile:
    #json.dump(history_dict, outfile)
    pickle_out = open(dictionary_file,"wb")
    pickle.dump(old_dict, pickle_out)
    pickle_out.close()

#display information down ehre

def button_action_1(sender):
    button2.title = "this"
    button3.title = "Is"
    button4.title = "a"
    button5.title = "Public"
    button6.title = "Service"
    button7.title = "Annoucement"
    button8.title = "Test"
    set_labels.set_100_series(v)
    set_labels.set_200_series(v)

#setup variables
v = ui.load_view()

button1 = v['button1']
button2 = v['button2']
button3 = v['button3']
button4 = v['button4']
button5 = v['button5']
button6 = v['button6']
button7 = v['button7']
button8 = v['button8']

label100= v['label100']
label101= v['label101']
label102= v['label102']
label103= v['label103']
label104= v['label104']
label105= v['label105']
label106= v['label106']

set_labels.setup_widgets(v)

button1.action = button_action_1
button1.title = "Test" #this works

v.present(style='sheet', hide_title_bar=True)
