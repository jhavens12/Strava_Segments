import ui #used for pythonista
import console #used for pythonista
import webbrowser

def set_100_series(v):

    v['label100'].text = str("100")
    v['label101'].text = str("series")
    v['label102'].text = str("labels")
    v['label103'].text = str()
    v['label104'].text = str()
    v['label105'].text = str()
    v['label106'].text = str()


def set_200_series(v,old_dict,segment):
    if 'historical_data' in old_dict[segment]:
        print("There is an old record for "+str(old_dict[segment]['information']['name']))
        print()
        v['label300'].text = str(old_dict[segment]['historical_data']['Jonathan']['hms'])
        v['label301'].text = str(old_dict[segment]['historical_data']['Jonathan']['start_time'])
        v['label302'].text = str(old_dict[segment]['historical_data']['Jonathan']['rank'])+"/"+str(old_dict[segment]['historical_data']['entries'])
        v['label303'].text = str(old_dict[segment]['historical_data']['information']['athlete_segment_stats']['effort_count'])
        v['label304'].text = str(old_dict[segment]['historical_data']['cr']['hms'])
        v['label305'].text = str(old_dict[segment]['historical_data']['Jonathan']['hms'] - old_dict[segment]['cr']['hms'])
        v['label306'].text = str(old_dict[segment]['historical_data']['cr']['athlete_name'])
        v['label307'].text = str(old_dict[segment]['historical_data']['cr']['start_time'])
    else:
        v['label300'].text = str()
        v['label301'].text = str()
        v['label302'].text = str()
        v['label303'].text = str()
        v['label304'].text = str()
        v['label305'].text = str()
        v['label306'].text = str()
        v['label307'].text = str()

    v['label100'].text = str("My Time:")
    v['label200'].text = str(old_dict[segment]['Jonathan']['hms']) #my time

    v['label101'].text = str("Set On:")
    v['label201'].text = str(old_dict[segment]['Jonathan']['start_time']) #my set date

    v['label102'].text = str("My Rank:")
    v['label202'].text = str(old_dict[segment]['Jonathan']['rank'])+"/"+str(old_dict[segment]['entries']) #rank

    v['label103'].text = str("My Attempts:")
    v['label203'].text = str(old_dict[segment]['information']['athlete_segment_stats']['effort_count']) #my attempts

    v['label104'].text = str("Record:")
    v['label204'].text = str(old_dict[segment]['cr']['hms']) #record time

    v['label105'].text = str("Difference:")
    v['label205'].text = str(old_dict[segment]['Jonathan']['hms'] - old_dict[segment]['cr']['hms']) #behind b

    v['label106'].text = str("CR Set By:")
    v['label206'].text = str(old_dict[segment]['cr']['athlete_name'])

    v['label107'].text = str("Set On:")
    v['label207'].text = str(old_dict[segment]['cr']['start_time'])
