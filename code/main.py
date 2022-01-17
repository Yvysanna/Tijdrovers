# ==================================================================================
# main.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Usage: python3 main.py
#
# - Creates schedule
# ==================================================================================

from numpy import NaN
import pandas as pd
from algorithms.planner import Planner

import loader


days = ['ma', 'di', 'wo', 'do', 'vr']
timeslots = ['9-11', '11-13', '13-15', '15-17']

pd.set_option("display.max_rows", None, "display.max_columns", None)

# Load classrooms and courses
classrooms_list = loader.load_classrooms()
(students_list, course_count) = loader.load_students()
course_list = loader.load_courses(classrooms_list, course_count)
loader.load_activities(classrooms_list, students_list,course_list)

# Create schedule for every classroom
schedule_dict = {}
for classroom in classrooms_list:
    schedule_dict[classroom.name] = pd.DataFrame(columns=days, index=timeslots)


planner = Planner(classrooms_list)
for course in course_list:
    for activity in course._activities:
        planner.plan_activity(classrooms_list[classrooms_list.index(activity._room):], activity)


df_dict = {'student': [],'vak': [],'activiteit': [],'zaal': [],'dag': [],'tijdslot': []}
for student in students_list:
    for course in student.courses:
        activities = [activity for activity in course._activities if activity.confirm_registration(student)]
        for activity in activities:
            room, day, time = planner.get_info(activity)
            df_dict['student'].append(student._last_name + ' ' + student._first_name)
            df_dict['vak'].append(activity._name)
            df_dict['activiteit'].append(activity._type)
            df_dict['zaal'].append(activity._room.name)
            df_dict['dag'].append(day or 'tba')
            df_dict['tijdslot'].append(time or 'tba') 
            if (room):
                #pass
                print(f"{activity._name} ({activity._type}) - {room.name}/ ('{day}', '{time}')")
            else:
                #pass
                print(f"{activity._name} ({activity._type}) - {activity._room.name}/ ('{day}', '{time}') - not planned")

#print(df_dict['student'])
print('\n\n')
print (planner.get_capacity_info())


c = ['student','vak','activiteit','zaal','dag','tijdslot']
results_df = pd.DataFrame.from_dict(df_dict, orient='columns', dtype=None, columns=None)
print(results_df)
with open('data/results/results.csv', 'w'):
    pass


results_df.to_csv('data/results/results.csv', sep = ';', index=False)

