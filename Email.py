#Set up to email daily any changes in segment positionsimport get_time
import get_seg_data
import calc
from io import BytesIO
from pprint import pprint
import credentials
import requests
import datetime
from pathlib import Path
import pickle
import yagmail

def convert_pace(distance,elapsed):
    minutes = elapsed/60
    miles = distance * 0.00062137
    pace = minutes/miles
    return pace

def convert_dec_time(dec):
    #converts decimal time to readable time format
    Minutes = dec
    Seconds = 60 * (Minutes % 1)
    result = ("%d:%02d" % (Minutes, Seconds))
    return result

gmail_user = credentials.gmail_user
gmail_password = credentials.gmail_password
yag = yagmail.SMTP( gmail_user, gmail_password)

my_athlete_id = credentials.my_athlete_id

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

improve_list = []
decrease_list = []

for new_seg in new_dict:
    for old_seg in old_dict:
        if new_seg == old_seg: #id matches
            if new_dict[new_seg]['Jonathan']['rank'] != old_dict[old_seg]['Jonathan']['rank']:#rank no longer matches

                if new_dict[new_seg]['Jonathan']['rank'] > old_dict[old_seg]['Jonathan']['rank']:
                    decrease_list.append("<b><font size='+1'>"+str(old_dict[old_seg]['information']['name'])+str('</font></b>'))
                    decrease_list.append("ID: https://www.strava.com/segments/"+str(new_seg))
                    decrease_list.append("App: strava://segments/"+str(new_seg))
                    decrease_list.append('')
                    decrease_list.append("Time: "+str(old_dict[old_seg]['Jonathan']['hms']))
                    decrease_list.append("Pace: "+convert_dec_time(convert_pace(new_dict[new_seg]['information']['distance'],new_dict[new_seg]['Jonathan']['elapsed_time'])))
                    decrease_list.append('')
                    decrease_list.append("Old Rank: "+str(old_dict[old_seg]['Jonathan']['rank'])+"/"+str(old_dict[old_seg]['entries']))
                    decrease_list.append("New Rank: "+str(new_dict[new_seg]['Jonathan']['rank'])+"/"+str(new_dict[new_seg]['entries']))
                    decrease_list.append('')
                    decrease_list.append("Old Date: "+str(old_dict[old_seg]['Jonathan']['start_time']))
                    #decrease_list.append("New Time: "+str(new_dict[new_seg]['Jonathan']['hms']))
                    decrease_list.append("New Date: "+str(new_dict[new_seg]['Jonathan']['start_time']))
                    decrease_list.append('')
                    decrease_list.append("CR: "+str(new_dict[new_seg]['cr']['athlete_name']))
                    decrease_list.append("Time: "+str(new_dict[new_seg]['cr']['hms']))
                    decrease_list.append("Date: "+str(new_dict[new_seg]['cr']['start_time']))

                    seg_distance = float(new_dict[new_seg]['information']['distance'])
                    cr_seconds = float(new_dict[new_seg]['cr']['elapsed_time'])
                    meters_per_second = seg_distance/cr_seconds
                    miles_per_hour = meters_per_second * 2.2369
                    if miles_per_hour > 11.5:
                        decrease_list.append('')
                        decrease_list.append("<font size='+1'>SUSPECT SPEED DETECTED!</font>")
                        decrease_list.append('')

                    decrease_list.append("Speed (Mph): "+str("{0:.2f}".format(miles_per_hour)))
                    decrease_list.append("Pace: "+convert_dec_time(convert_pace(new_dict[new_seg]['information']['distance'],new_dict[new_seg]['cr']['elapsed_time'])))
                    decrease_list.append('')
                    decrease_list.append("CR Difference: "+str(new_dict[new_seg]['Jonathan']['hms'] - new_dict[new_seg]['cr']['hms']))
                    decrease_list.append("************************")
                    decrease_list.append('')

                if new_dict[new_seg]['Jonathan']['rank'] < old_dict[old_seg]['Jonathan']['rank']:
                    improve_list.append("<b><font size='+1'>"+str(old_dict[old_seg]['information']['name'])+str('</font></b>'))
                    improve_list.append("ID: https://www.strava.com/segments/"+str(new_seg))
                    improve_list.append("App: strava://segments/"+str(new_seg))
                    improve_list.append('')
                    improve_list.append("Improved by: "+str( old_dict[old_seg]['Jonathan']['hms'] - new_dict[new_seg]['Jonathan']['hms'] ))
                    improve_list.append("Old Time: "+str(old_dict[old_seg]['Jonathan']['hms']))
                    improve_list.append("New Time: "+str(new_dict[new_seg]['Jonathan']['hms']))
                    improve_list.append("New Pace: "+convert_dec_time(convert_pace(new_dict[new_seg]['information']['distance'],new_dict[new_seg]['Jonathan']['elapsed_time'])))
                    improve_list.append('')
                    improve_list.append("Old Rank: "+str(old_dict[old_seg]['Jonathan']['rank'])+"/"+str(old_dict[old_seg]['entries']))
                    improve_list.append("New Rank: "+str(new_dict[new_seg]['Jonathan']['rank'])+"/"+str(new_dict[new_seg]['entries']))
                    improve_list.append('')
                    improve_list.append("New Date: "+str(new_dict[new_seg]['Jonathan']['start_time']))
                    improve_list.append("Old Date: "+str(old_dict[old_seg]['Jonathan']['start_time']))
                    improve_list.append('')
                    improve_list.append("CR: "+str(new_dict[new_seg]['cr']['athlete_name']))
                    improve_list.append("Time: "+str(new_dict[new_seg]['cr']['hms']))
                    improve_list.append("Date: "+str(new_dict[new_seg]['cr']['start_time']))

                    seg_distance = float(new_dict[new_seg]['information']['distance'])
                    cr_seconds = float(new_dict[new_seg]['cr']['elapsed_time'])
                    meters_per_second = seg_distance/cr_seconds
                    miles_per_hour = meters_per_second * 2.2369
                    if miles_per_hour > 11.5:
                        improve_list.append('')
                        improve_list.append("<font size='+1'>SUSPECT SPEED DETECTED!</font>")
                        improve_list.append('')

                    improve_list.append("Speed (Mph): "+str("{0:.2f}".format(miles_per_hour)))
                    improve_list.append("Pace: "+convert_dec_time(convert_pace(new_dict[new_seg]['information']['distance'],new_dict[new_seg]['cr']['elapsed_time'])))
                    improve_list.append('')
                    improve_list.append("CR Difference: "+str(new_dict[new_seg]['Jonathan']['hms'] - new_dict[new_seg]['cr']['hms']))
                    improve_list.append("************************")
                    improve_list.append('')


                old_dict[old_seg]['Jonathan_old'] = old_dict[old_seg]['Jonathan'] #store old jonathan as jonathan_old
                old_dict[old_seg]['Jonathan_old']['change_occurred'] = datetime.datetime.now() #timestamp it
    if new_seg not in old_dict: #what about if we star a new segment? need to save it to old_dict
        #print("We have a new starred segment: "+str(new_dict[new_seg]['information']['name']))
        old_dict[new_seg] = new_dict[new_seg] #save new segment in old dict

#improve_list.append("<b><font size='+2'>IMPROVED Segments:</font></b>\n\n")
#decrease_list.append("<b><font size='+2'>DECREASED Segments:</font></b>\n\n")

if improve_list or decrease_list:
    print("We have updated data to share")
    if improve_list:
        improve_list = ["<b><font size='+2'>IMPROVED Segments:</font></b>\n\n"] + improve_list #add header
    if decrease_list:
        decrease_list = ["<b><font size='+2'>DECREASED Segments:</font></b>\n\n"] + decrease_list #add header

    email_body = improve_list + decrease_list
    real_send = "\n".join(email_body)
    yag.send('jhavens12@gmail.com', 'Strava Segment Update', [real_send])

else:
    print("There are no updates at this time")

#save to the history file - use OLD_DICT
with open(dictionary_file, 'w') as outfile:
    #json.dump(history_dict, outfile)
    pickle_out = open(dictionary_file,"wb")
    pickle.dump(old_dict, pickle_out)
    pickle_out.close()
