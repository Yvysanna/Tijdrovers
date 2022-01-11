import pandas as pd
import random

days = ['ma', 'di', 'wo', 'do', 'vr']
timeslots = ['9-11', '11-13', '13-15', '15-17']


def randomize(subjects_df, schedule_dict):
    # create full list of activities
    activities_list = []

    index_subjects = range(len(subjects_df.index) - 1)

    # for every activity of every subject, add activity to list
    for i in index_subjects:
        for j in range(subjects_df.at[i, "min aantal tijdslots"]):
            activities_list.append(subjects_df.at[i, "Vakken"] + "_" + str(j))

    #print(activities_list)

    # shuffle list of activities
    random.shuffle(activities_list)

    #print(activities_list)

    # add every activity to schedule
    for i in schedule_dict:
        for j in days:
            for k in timeslots:
                if len(activities_list) > 0:
                    schedule_dict[i].at[k, j] = activities_list.pop(0)

    return schedule_dict