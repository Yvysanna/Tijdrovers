# ==================================================================================
# main.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Usage: python3 main.py -i iterations (int) -d distribution (bool)
#          -g graph (bool) -a algorithm (str) -n runs (int)
#
# - Creates class schedule using the provided data using a hill climber
# - Reduces the number of maluspoints as much as possible, which are given for
#   schedule gaps, activity conflicts, exceeding classroom capacity and using
#   late timeslots
# - The specific hill climber can be chosen using the algorithm argument,
#   and the number of iterations in the argument can be provided with the
#   iterations argument
# - A line graph may be created with the graph argument which plots the number of
#   maluspoints against the iterations
# - A distribution graph may be created with the distribution argument which makes
#   a histogram of maluspoints across n runs, which can be set with the runs
#   argument
# - Do not create a line graph and distribution graph at the same time, as it
#   may cause bugs
# ==================================================================================

import time
from statistics import mean
import argparse

from code.algorithms.planner import Planner

from code.algorithms.semirandom import semirandom
from code.algorithms.randommethod import random_method
from code.algorithms.hill_climber import HillClimber

from code.loader import load_all
from code.checker import checker
from code.visualisations import store, distribution, plot

class InvalidAlgorithm(Exception):
    pass


def main(iterations, graph, algorithm):
    """
    Main function for this programm
        * Loads and uses source information in hill climber
        * Evaluates hill climber results
        * Stores results and plotting

    ARGS:
    iterations : int
        Number of iterations the algorithm will go through
    graph : bool
        Wether or not a graph will be made for the hill climber
    algorithm : str
        The algorithm that will be used to create the schedule

    RETURNS:
        Number of maluspoints
    """

    # Load classrooms, students and courses
    classrooms_list, students_set, course_set = load_all()
    points = 0

    # Fill planner with semirandom method
    while points == False or points == 0:
        planner = Planner(classrooms_list)
        semirandom(course_set, classrooms_list, planner, planner.days, planner.times)
        student_dict = planner.create_student_dict(students_set)
        points = checker(planner.slots, student_dict)

    # Create object of class hill climber
    hill = HillClimber(planner, course_set, students_set)
    # Run hill climber method and evaluate its results
    if algorithm == 'climber':
        i = hill.run(iterations)
    elif algorithm == 'annealing':
        i = hill.run_annealing(iterations)
    elif algorithm == 'annealing_climber':
        i = hill.run_annealing_climber(iterations)
    else:
        raise InvalidAlgorithm("This algorithm is invalid")
    student_dict = planner.create_student_dict(students_set)
    points = checker(planner.slots, student_dict)

    # Create visualisation and csv dataset from results
    if graph:
        plot(hill.plotx, hill.ploty, hill.streak)

    # Save to csv
    store(students_set, planner, points)
    return points, i


if __name__ == '__main__':
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description='create a class schedule')

    # Adding arguments
    parser.add_argument('-i', '--iterations', type=int, default=10000,help='hill climber iterations (default: 10000)')
    parser.add_argument('-d', '--distribution', type=bool,default=False, help='create distribution histogram (default: False)')
    parser.add_argument('-g', '--graph',   type=bool,default=False,
                        help='create lines graph for single run, do not use together with distribution! (default: False)')
    parser.add_argument('-n', '--runs', type=int, default=1, help='number of runs (default: 1)')
    parser.add_argument('-a', '--algorithm', type=str, default='climber', help='select algorithm: climber, annealing or annealing_climber (default: climber)')

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    points, iterations = [], []
    for _ in range(args.runs):
        new_points, i = main(args.iterations, args.graph, args.algorithm)
        points.append(new_points)
        iterations.append(i)

    print("\n Average: " + str(mean(points)))
    print("\n Average iterations: " + str(mean(iterations)))

    # Create probability distribution from all runs
    if args.distribution:
        distribution(points, args.runs)
