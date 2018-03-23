import ui #used for pythonista
import console #used for pythonista

def set_100_series(v,old_dict,segment):

    v['label100'].text = str("100")
    v['label101'].text = str("series")
    v['label102'].text = str("labels")
    v['label103'].text = str()
    v['label104'].text = str()
    v['label105'].text = str()
    v['label106'].text = str()


def set_200_series(v,old_dict,segment):

    v['label200'].text = str(old_dict[segment]['Jonathan']['hms']) #my time
    v['label201'].text = str(old_dict[segment]['Jonathan']['start_time']) #my set date
    v['label202'].text = str(old_dict[segment]['Jonathan']['rank']) #rank
    v['label203'].text = str(old_dict[segment]['information']['athlete_segment_stats']['effort_count']) #my attempts
    v['label204'].text = str(old_dict[segment]['cr']['hms'])) #record time
    v['label205'].text = str(old_dict[segment]['Jonathan']['hms'] - old_dict[segment]['cr']['hms']) #behind by
    v['label206'].text = str()
