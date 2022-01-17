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
from objects.planner import Planner

import loader


days = ['ma', 'di', 'wo', 'do', 'vr']
timeslots = ['9-11', '11-13', '13-15', '15-17']

pd.set_option("display.max_rows", None, "display.max_columns", None)

# Load classrooms and courses
classrooms_list = loader.load_classrooms()
(students_list, course_count) = loader.load_students()
course_list = loader.load_courses(classrooms_list, students_list, course_count)

# Create activity objects in course
for course in course_list:
    course.create_activities(classrooms_list)

    # The only important line from randomize !!!!! RANDOMIZE NO LONGER NEEDED :D
    course.schedule(classrooms_list) # Creates schedule; might needs to be put further down in code

# Create schedule for every classroom
schedule_dict = {}
for classroom in classrooms_list:
    schedule_dict[classroom.name] = pd.DataFrame(columns=days, index=timeslots)


planner = Planner(classrooms_list)
for course in course_list:
    for activity in course._activities:
        planner.plan_activity(classrooms_list[classrooms_list.index(activity._room):], activity)


for student in students_list:
    print('\n',student._last_name)
    for course in student.courses:
        activities = [activity for activity in course._activities if activity.confirm_registration(student)]
        for activity in activities:
            room, day, time = planner.get_info(activity)
            if (room):
                print(f"{activity._name} ({activity._type}) - {room.name}/ ('{day}', '{time}')")
            else:
                print(f"{activity._name} ({activity._type}) - {activity._room.name}/ ('{day}', '{time}') - not planned")


print('\n\n')
print (planner.get_capacity_info())

