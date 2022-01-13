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
            for course in subjects_list:
                if subject == course._name:
                    classroom._possible_subjects.append(course)
                    course._possible_classrooms.append(classroom)

for student in students_list:
    for i, course in enumerate(student._courses):
        #print(i, course, subjects_list)
        student._courses[i] = list(filter(lambda subj: subj._name == course, subjects_list))[0]
#print(subjects_list[0].smallest_classroom())

# randomize subject activities and fill in schedule
randomize(subjects_list, schedule_dict)
print([l for l in classrooms_list])

# Write all dataframes for schedule in csv files
#for key, val in schedule_dict.items():
#    val.to_csv(f'data/results/schedule_{key}.csv',)
#print(schedule_dict)
#print(students_list)