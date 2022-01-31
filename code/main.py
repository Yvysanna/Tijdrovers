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
from conflicts import find_course_conflicts
from algorithms.semirandom import semirandom
from algorithms.randommethod import random_method
from algorithms.hill_climber import HillClimber
from store import store
import loader
import checker



def main():
    days = ['ma', 'di', 'wo', 'do', 'vr']
    timeslots = ['9-11', '11-13', '13-15', '15-17', '17-19']

    pd.set_option("display.max_rows", None, "display.max_columns", None)

    # Load classrooms and courses
    classrooms_list = loader.load_classrooms()
    (students_set, course_students) = loader.load_students()
    course_set = loader.load_courses(classrooms_list, course_students)
    loader.connect_courses(students_set, course_set)

    loader.load_activities(classrooms_list, students_set, course_set)

    min_planner = None


    calls = 1; min_points = 10000000000000
    while calls > 0 or min_planner == None:
        
        planner = Planner(classrooms_list)
        semirandom(course_set, classrooms_list, planner, days, timeslots)
        student_dict = planner.create_student_dict(students_set)
        points = checker.checker(planner.slots, student_dict)
        if points < min_points and points != False:
            min_points = points
            print(min_points)
            min_planner = planner
        calls -= 1

    hill = HillClimber(min_planner, course_set, students_set)
    hill.run_annealing()
    hill.plot()
    student_dict = min_planner.create_student_dict(students_set)
    points = checker.checker(min_planner.slots, student_dict)
    print(points)
    store(students_set, planner, points)


    #store(students_set, planner)

    #print(checker.checker(course_set))


    return planner.slots, student_dict

if __name__ == '__main__':
    main()
