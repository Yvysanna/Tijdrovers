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
from algorithms.planner import Planner
from algorithms.randommethod import random_method
from conflicts import find_course_conflicts
from algorithms.semirandom import semirandom
from store import store
import loader
import checker



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

    loader.load_activities(classrooms_list, students_set, ordered_courses)

    # Create schedule for every classroom
    schedule_dict = {}
    for classroom in classrooms_list:
        schedule_dict[classroom.name] = pd.DataFrame(columns=days, index=timeslots)

    #print(find_activity_conflicts(course_set, students_set))

    #planner = Planner(classrooms_list)

    calls = 1; min_points = 100000
    while calls > 0:
        planner = Planner(classrooms_list)
        #semirandom(course_set, classrooms_list, planner, days, timeslots)
        random_method(course_set, classrooms_list, planner, days, timeslots)
        student_dict = planner.create_student_dict(students_set)
        points = checker.checker(course_set, student_dict)
        if points < min_points:
            min_points = points
            print(min_points)
            store(students_set, planner)
        calls -= 1

    #planner = Planner(classrooms_list)
    #random_method(course_set, planner, classrooms_list, days, timeslots)

    #store(students_set, planner)

    #print(checker.checker(course_set))


    return course_set, student_dict

if __name__ == '__main__':
    main()