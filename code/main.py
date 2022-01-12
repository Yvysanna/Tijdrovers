# ==================================================================================
# main.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Usage: python3 main.py
#
# - Creates schedule
# ==================================================================================

import pandas as pd

import loader
from randomize import randomize


days = ['ma', 'di', 'wo', 'do', 'vr']
timeslots = ['9-11', '11-13', '13-15', '15-17']

# load classrooms and subjects
classrooms_list = loader.load_classrooms()
subjects_list = loader.load_subjects()
(students_list, subjects_count) = loader.load_students()

# create schedule for every classroom
schedule_dict = {}
for classroom in classrooms_list:
    schedule_dict[classroom._classroom] = pd.DataFrame(columns=days, index=timeslots)

    for subject, count in subjects_count.items():
        if classroom._capacity >= count:
            classroom._possible_subjects.append(subject)
            for course in subjects_list:
                if subject == course._name:
                    course._possible_classrooms.append(classroom._classroom)

for subject in subjects_list:
    print(subject._name,subject._possible_classrooms)

# randomize subject activities and fill in schedule
# randomize(subjects_list, schedule_dict)
# print(schedule_dict)