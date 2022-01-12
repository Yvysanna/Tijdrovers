import pandas as pd
import random

days = ['ma', 'di', 'wo', 'do', 'vr']
timeslots = ['9-11', '11-13', '13-15', '15-17']


def randomize(subjects_list, schedule_dict):
    """
    ARGS: list of objects, dict{str:pd.dataframe}
    randomizes the order of list containing all courses (n amount of times depending on min_timeslots)
    RETURNS: dict 
    KEY: room name
    VALUE: pd.dataframe of full-week schedule of courses according to room capacity depending on amount of enrollments
    """
    # create full list of activities
    activities_list = []

    # for every activity of every subject, add activity to list
    for subject in subjects_list:
        for n in range(int(subject._min_timeslots)):
            activities_list.append(subject)

    # shuffle list of activities
    random.shuffle(activities_list)

    for j in days:
        for k in timeslots:       
            # add every activity to schedule
            if len(activities_list) > 0:
                subj = activities_list.pop(0)
                schedule_dict[subj.smallest_classroom()._classroom].at[k, j] = subj._name

    return schedule_dict

