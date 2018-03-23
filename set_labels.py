import ui #used for pythonista
import console #used for pythonista

def set_100_series(v):

    v['label100'].text = str("100")
    v['label101'].text = str("series")
    v['label102'].text = str("labels")
    v['label103'].text = str()
    v['label104'].text = str()
    v['label105'].text = str()
    v['label106'].text = str()


def set_200_series(v,old_dict,segment):
    if 'Jonathan_old' in old_dict[segment]:
        print("There is an old record for "+str(old_dict[segment]['information']['name']))
        #v['label300'].text = str(old_dict[segment]['Jonathan_old']['hms'])
        v['label300'].text = str("UPDATED")
        v['label301'].text = str(old_dict[segment]['Jonathan_old']['start_time'])
        v['label302'].text = str(old_dict[segment]['Jonathan_old']['rank'])
        v['label305'].text = str(old_dict[segment]['Jonathan_old']['hms'] - old_dict[segment]['cr']['hms'])


    v['label100'].text = str("My Time:")
    v['label200'].text = str(old_dict[segment]['Jonathan']['hms']) #my time

    v['label101'].text = str("Set On:")
    v['label201'].text = str(old_dict[segment]['Jonathan']['start_time']) #my set date

    v['label102'].text = str("My Rank:")
    v['label202'].text = str(old_dict[segment]['Jonathan']['rank']) #rank

    v['label103'].text = str("My Attempts:")
    v['label203'].text = str(old_dict[segment]['information']['athlete_segment_stats']['effort_count']) #my attempts

    v['label104'].text = str("Course Record:")
    v['label204'].text = str(old_dict[segment]['cr']['hms']) #record time

    v['label105'].text = str("Difference:")
    v['label205'].text = str(old_dict[segment]['Jonathan']['hms'] - old_dict[segment]['cr']['hms']) #behind b

    v['label106'].text = str("CR Set By:")
    v['label206'].text = str(old_dict[segment]['cr']['athlete_name'])

    v['label107'].text = str("Date:")
    v['label207'].text = str(old_dict[segment]['cr']['start_date'])
