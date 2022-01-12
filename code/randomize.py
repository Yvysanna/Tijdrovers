import pandas as pd
import random

days = ['ma', 'di', 'wo', 'do', 'vr']
timeslots = ['9-11', '11-13', '13-15', '15-17']


def randomize(subjects_list, schedule_dict):
    # create full list of activities
    activities_list = []
    activities_dict = {}

    # for every activity of every subject, add activity to list
    for subject in subjects_list:
        for n in range(int(subject._min_timeslots)):
            activities_list.append(subject._name)
            # activities_dict[activity] = subject._name

    # shuffle list of activities
    random.shuffle(activities_list)
    print(activities_list)

    # add every activity to schedule
    #  for i in schedule_dict:
    #     for j in days:
    #         for k in timeslots:
    #             if len(activities_list) > 0:
    #                 schedule_dict[i].at[k, j] = activities_list.pop(0)
