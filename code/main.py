# ==================================================================================
# main.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Usage: python3 main.py
#
# - Creates schedule
# ==================================================================================

import random
import pandas as pd
from algorithms.planner import Planner
from conflicts import find_course_conflicts, find_activity_conflicts, find_conflict_free_activities, book_rooms_for_parallel_activities
import loader
import ugly_checker as ugly_checker

def main():
    days = ['ma', 'di', 'wo', 'do', 'vr']
    timeslots = ['9-11', '11-13', '13-15', '15-17']

    pd.set_option("display.max_rows", None, "display.max_columns", None)

    # Load classrooms and courses
    classrooms_list = loader.load_classrooms()
    (students_set, course_students) = loader.load_students()
    course_set = loader.load_courses(classrooms_list, course_students)
    loader.connect_courses(students_set, course_set)

    course_dict, ordered_courses = find_course_conflicts(students_set, course_set)

    loader.load_activities(classrooms_list, students_set, course_set)

    # Create schedule for every classroom
    schedule_dict = {}
    for classroom in classrooms_list:
        schedule_dict[classroom.name] = pd.DataFrame(columns=days, index=timeslots)

    #print(find_activity_conflicts(course_set, students_set))

    planner = Planner(classrooms_list)

    # TEMPORARY FIX FOR SCHEDULING EVERY LEFTOVER ACTIVITY RANDOMLY
    result = find_conflict_free_activities(course_set)
    not_scheduled = set()
    for activities in result:
        for activity in activities:
            planner.plan_activity(classrooms_list[classrooms_list.index(activity._room):], activity)
            
            # Check if activity can be scheduled
            room, day, time = planner.get_info(activity)

    #---- SEMI RANDOM METHOD FIX FROM HERE ----- #
            if not room:
                not_scheduled.add(activity)

    #print("NOT SCHEDULED", len(not_scheduled))
    for activity in not_scheduled:

        # Loop until activity could be planned for each activity
        while planner.get_info(activity) == (None, None, None):
            room = random.choice(classrooms_list)
            day = random.choice(days)
            time = random.choice (timeslots)

            # Just try to insert activity with random data there and see if it works
            planner.insert_activity(activity, room, day, time)
        activity._room = room # Connect room when broken out of while loop
        room, day, time = planner.get_info(activity) # Final checkup

        if planner.get_info(activity) == (None, None, None):
            print("NOT FIXED")

    # ----- SEMI RANDOM METHOD END ----- #

    # ------ COMPLETELY RANDOM METHOD ------ ADDS EVERY ACTIVITY TO RANDOM TIMESLOT -------- #
    # all_activities_global = []
    # for course in course_set:
    #     all_activities = course._lectures + course._tutorials + course._labs
        
    #     for activity in all_activities:
    #         all_activities_global.append(activity)

    # random.shuffle(all_activities_global)

    # for activity in all_activities_global:

    #     while planner.get_info(activity) == (None, None, None):
    #         room = random.choice(classrooms_list)
    #         day = random.choice(days)
    #         time = random.choice (timeslots)
    #         planner.insert_activity(activity, room, day, time)
    #         #planner.plan_activity(classrooms_list[classrooms_list.index(activity._room):], activity)
    #         activity._room = room
        #print(activity._name)

            #planner.plan_activity(classrooms_list[classrooms_list.index(activity._room):], activity)


    df_dict = {'student': [],'vak': [],'activiteit': [],'zaal': [],'dag': [],'tijdslot': []}
    for student in students_set:
        for course in student.courses:
            all_activities = course._lectures + course._tutorials + course._labs
            activities = [activity for activity in all_activities if activity.confirm_registration(student)]
            for activity in activities:
                room, day, time = planner.get_info(activity)
                df_dict['student'].append(student._last_name + ' ' + student._first_name)
                df_dict['vak'].append(activity._name)
                df_dict['activiteit'].append(activity._type)
                df_dict['zaal'].append(activity._room.name)
                df_dict['dag'].append(day or 'tba')
                df_dict['tijdslot'].append(time or 'tba') 
                # if (room):
                #     #pass
                #     print(f"{activity._name} ({activity._type}) - {room.name}/ ('{day}', '{time}')")
                # else:
                #     #pass
                #     print(f"{activity._name} ({activity._type}) - {activity._room.name}/ ('{day}', '{time}') - not planned")


    results_df = pd.DataFrame.from_dict(df_dict, orient='columns', dtype=None, columns=None)

    results_df.to_csv('data/results/results.csv', sep = ';', index=False)

    print(ugly_checker.count_points(classrooms_list, course_set))

    


    df_dict = {'student': [],'vak': [],'activiteit': [],'zaal': [],'dag': [],'tijdslot': []}
    for student in students_set:
        for course in student.courses:
            all_activities = course._lectures + course._tutorials + course._labs
            activities = [activity for activity in all_activities if activity.confirm_registration(student)]
            for activity in activities:
                room, day, time = planner.get_info(activity)
                df_dict['student'].append(student._last_name + ' ' + student._first_name)
                df_dict['vak'].append(activity._name)
                df_dict['activiteit'].append(activity._type)
                df_dict['zaal'].append(activity._room.name)
                df_dict['dag'].append(day or 'tba')
                df_dict['tijdslot'].append(time or 'tba') 
                # if (room):
                #     #pass
                #     print(f"{activity._name} ({activity._type}) - {room.name}/ ('{day}', '{time}')")
                # else:
                #     #pass
                #     print(f"{activity._name} ({activity._type}) - {activity._room.name}/ ('{day}', '{time}') - not planned")


    results_df = pd.DataFrame.from_dict(df_dict, orient='columns', dtype=None, columns=None)

    results_df.to_csv('data/results/results.csv', sep = ';', index=False)

    print(ugly_checker.count_points(classrooms_list, course_set))

    return classrooms_list, course_set

if __name__ == '__main__':
    main()