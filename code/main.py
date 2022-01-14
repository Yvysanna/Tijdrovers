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

# Load classrooms and courses
classrooms_list = loader.load_classrooms()
(students_list, course_count) = loader.load_students()
course_list = loader.load_courses(course_count)

# Create schedule for every classroom
schedule_dict = {}
for classroom in classrooms_list:
    schedule_dict[classroom.name] = pd.DataFrame(columns=days, index=timeslots)

    # Connect room and course objects with eachother
    for course in course_list:
        if classroom.capacity >= course.students_number:
            classroom.possible_courses.append(course)
            course.possible_classrooms.append(classroom)

# Connect student object with according course objects
for student in students_list:
    for i, course in enumerate(student.courses):
        #print(i, course, course_list)
        student.courses[i] = list(filter(lambda subj: subj.name == course, course_list))[0]
#print(course_list[0].smallest_classroom())

# Randomize course activities and fill in schedule
randomize(course_list, schedule_dict)
# print([l for l in classrooms_list])

# Write all dataframes for schedule to csv files
#for key, val in schedule_dict.items():
#    val.to_csv(f'data/results/schedule_{key}.csv',)
#print(schedule_dict)
#print(students_list)
