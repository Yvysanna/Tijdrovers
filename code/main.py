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

# Create activity objects in course
for course in course_list:
    course.create_activities(classrooms_list)
    
    # The only important line from randomize !!!!! RANDOMIZE NO LONGER NEEDED :D
    course.schedule(classrooms_list) # Creates schedule; might needs to be put further down in code

# Create schedule for every classroom
schedule_dict = {}
for classroom in classrooms_list:
    schedule_dict[classroom.name] = pd.DataFrame(columns=days, index=timeslots)

    
# Connect student objects with according course objects
for student in students_list:
    for i, course in enumerate(student.courses):
        course_object = list(filter(lambda subj: subj.name == course, course_list))[0]
        student.courses[i] = course_object

        # Add students to courses
        student.courses[i].register(student)
        # course_object.students_list.append(student)

#print(course_list[0].smallest_classroom())

# Randomize course activities and fill in schedule
#randomize(course_list, schedule_dict)
# print([l for l in classrooms_list])
print(classrooms_list)
