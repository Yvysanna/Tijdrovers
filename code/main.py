# ==================================================================================
# main.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Usage: python3 main.py
#
# - Creates schedule
# ==================================================================================

import time
from statistics import mean

# Main class for course planning, holds all information about schedule
from algorithms.planner import Planner

# Algorithm functions
from algorithms.semirandom import semirandom
from algorithms.random import random_method
from algorithms.hill_climber import HillClimber

# Loader function to load all necessary information from dataset
from loader import load_all

# Evaluation function
from checker import checker

# Functions to create visualisations and store schedule results in csv
from visualisations import store, distribution, plot


def main():
    """
    ARGS:
        None
    USAGE:
        Main function for this programm
        * loads and uses source information in hill climber 
        * evaluates hill climber results 
        * stores results and plotting

    RETURNS:
        Maluspoints
    """

    # Load classrooms, students and courses
    classrooms_list, students_set, course_set = load_all()

    # Create planner object
    points = 0

    # Fill planner with semirandom method
    while points == False or points == 0:
        planner = Planner(classrooms_list)
        random_method(course_set, classrooms_list, planner, planner.days, planner.times)
        student_dict = planner.create_student_dict(students_set)
        points = checker(planner.slots, student_dict)


    # Create object of class hill climber
    hill = HillClimber(planner, course_set, students_set, streak_limit=100, iteration_limit=500, point_limit=200, temperature_multiplier=0.02)
    # Run hill climber method and evaluate its results
    i = hill.run('climber')
    student_dict = planner.create_student_dict(students_set)
    points = checker(planner.slots, student_dict)

    # Create visualisation and csv dataset from results
    plot(hill.plotx, hill.ploty, hill.streak_limit)
    store(students_set, planner, points)

    return points, i


if __name__ == '__main__':
    start = time.time()
    n_runs = 0

    points = []
    iterations = []

    # while time.time() - start < 3600:
    new_points, i = main()
    points.append(new_points)
    iterations.append(i)
    print(n_runs, i, points[n_runs])
    n_runs += 1

    print("\n Average: " + str(mean(points)))
    print("\n Average iterations: " + str(mean(iterations)))

    # Create probability distribution from all runs
    distribution(points, n_runs)


