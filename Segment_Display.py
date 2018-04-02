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
import webbrowser
import sys

import ui #used for pythonista
import console #used for pythonista

my_athlete_id = '19826138'

w,h = ui.get_screen_size()

bh = 32 #button height
bw = w/2 #button width
sp = 15 #spacing
smg = 5 #side margin
tmg = 20 #top_margin

v = ui.load_view()
v = ui.View(frame = (0,0,w,h))
v.background_color = "#FC4C02" #strava orange

label_view =  ui.ScrollView(frame=(smg, tmg, w/2, h), background_color='white')

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

    #new_dict is the freshly pulled information
    #old_dict is the imported information from file

    for new_seg in new_dict:
        for old_seg in old_dict:
            if new_seg == old_seg: #segment id matches each other
                if new_dict[new_seg]['Jonathan']['rank'] != old_dict[old_seg]['Jonathan']['rank']:#rank no longer matches
                    print("Rank has changed for: "+str(old_dict[old_seg]['information']['name'])) #print that it has changed
                    #need to wipe out previous historical_data if exists so it doesn't create a big chain
                    historical_data = old_dict[old_seg]
                    old_dict[old_seg] = new_dict[new_seg]
                    old_dict[old_seg]['historical_data'] = historical_data
                    old_dict[old_seg]['historical_data']['timestamp'] = datetime.datetime.now()

        if new_seg not in old_dict: #what about if we star a new segment? need to save it to old_dict
            print("We have a new starred segment: "+str(new_dict[new_seg]['information']['name']))
            old_dict[new_seg] = new_dict[new_seg] #save new segment in old dict

    display_dict = {} #use this to filter out anything thats not in "Starred" - keeping it below still updates all segments
    for seg in old_dict:
        for starred_seg in starred_dict:
            if seg == starred_dict[starred_seg]['id']: #check if segment in old dict is in current starred dictionary
                display_dict[seg] = old_dict[seg] #take entry from old dict and put in to display

    #do stuff in here for pythonista, set up the labels
    for seg in old_dict:
        if 'historical_data' in old_dict[seg]:
            print("There is an old record for "+str(old_dict[old_seg]['information']['name']))

    #save to the history file - use OLD_DICT
    with open(dictionary_file, 'w') as outfile:
        #json.dump(history_dict, outfile)
        pickle_out = open(dictionary_file,"wb")
        pickle.dump(old_dict, pickle_out) #save old_dict as it has all of the data
        pickle_out.close()

    #checks to see if there are more entries than labels
    if len(display_dict) > 14:
        v.close() #close view
        print("You have too many starred segments, unstar some and try again")
        sys.exit()

    return display_dict
#display information down ehre

def refresh(sender):
    v['Refresh'].title = "Loading..."
    global display_dict
    display_dict = download_data()
    global button_dict #make global on each refresh
    button_dict = set_button_titles(v,display_dict)
    #button dict is buttonid as key and segid as value
    v['Refresh'].action = refresh #do refresh function
    v['Refresh'].title = "Refresh" #this works

def seg_button_pressed(sender):
    #takes sender.title (name) and sets labels based on that
    set_labels.set_200_series(v,display_dict,button_dict[sender.title])
    #when this button is pressed
    global url_id
    url_id = str(button_dict[sender.title])

def set_button_titles(v,old_dict): #this is passed display dict not old dict
    button_dict = {}
    for n,segment in enumerate(old_dict):
        button_name = 'button'+str(n)
        label_title = str(old_dict[segment]['information']['name']) + " ("+str(old_dict[segment]['Jonathan']['rank'])+")"
        button_dict[label_title] = segment #save button with segment id

        btn_tmg = (tmg+sp)*n #determine y position
        button_name = ui.Button(name = button_name, bg_color ='white', frame = (0, btn_tmg, bw, bh))
        button_name.border_width = 1
        button_name.tint_color = 'black'#"RGBA(1.000000,0.285714,0.000000,1.000000)"
        button_name.border_color = 'white'#"RGBA(1.000000,0.767857,0.458333,1.000000)"
        button_name.corner_radius = 1
        button_name.background_color = "#01B2FC" #"RGBA(1.000000,1.000000,1.000000,1.000000)"
        button_name.title = label_title #set titles for buttons
        button_name.action = seg_button_pressed
        if 'historical_data' in old_dict[segment]:
            if old_dict[segment]['historical_data']['timestamp'] > (datetime.datetime.now() - datetime.timedelta(days=7)):
                button_name.background_color = '#0135FC'
                button_name.tint_color = 'white'
        label_view.add_subview(button_name)

    label_view.content_size = (w/2,(tmg+sp)*len(button_dict)+bh+sp)

    return button_dict

def open_url(sender):
    #sender is not used as label is static
    callback = "strava://segments/"+url_id
    webbrowser.open_new(callback)

v['button400'].action = open_url #set to open url
v['button400'].border_width = 1
v['button400'].tint_color = 'black'
v['button400'].border_color = 'white'
v['button400'].background_color = "#01B2FC"
v['button400'].title = "Open In Strava"


#setup variables

refresh("nothing") #runs initial setup
