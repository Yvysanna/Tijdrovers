# ==================================================================================
# main.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Usage: python3 main.py -s streak_limit (int) -p point_limit (int)
#          -i iteration_limit (int) -t temperature_multiplier (float)
#          -c constraint (bool) -r semirandom_begin (bool) -d distribution (bool)
#          -g graph (bool) -n runs (int) -a algorithm (str)
#
# - Creates class schedule using the provided data using a hill climber
# - Reduces the number of maluspoints as much as possible, which are given for
#   schedule gaps, activity conflicts, exceeding classroom capacity and using
#   late timeslots
# - The specific hill climber can be chosen using the algorithm argument,
#   and the streak limit, point limit, the number of iterations, and the temperature
#   multiplier in the argument can be provided with their respective arguments
# - It is recommended to use a number of 10000 or lower for number of iterations to
#   prevent out of range errors
# - A hard constraint for the third break term can be set by setting constraint
#   to True
# - The semirandom algorithm can be used instead of random_method for the begin state
#   by setting semirandom_begin to True
# - A line graph may be created with the graph argument which plots the number of
#   maluspoints against the iterations
# - A distribution graph may be created with the distribution argument which makes
#   a histogram of maluspoints across n runs, which can be set with the runs
#   argument
# - Do not create a line graph and distribution graph at the same time, as it
#   may cause bugs
# ==================================================================================

from statistics import mean
import argparse

from code.algorithms.planner import Planner

from code.algorithms.semirandom import semirandom
from code.algorithms.randommethod import random_method
from code.algorithms.hill_climber import HillClimber

from code.loader import load_all
from code.checker import checker
from code.visualisations import store, distribution, plot


def main(graph, algorithm, streak_limit, iteration_limit, point_limit, temperature_multiplier, constraint, semirandom_begin):
    """
    Main function for this programm
        * Loads and uses source information in hill climber
        * Evaluates hill climber results
        * Stores results and plotting

    ARGS:
    graph : bool
        Whether or not a graph will be made for the hill climber
    algorithm : str
        The algorithm that will be used to create the schedule
    streak_limit : int
        Hill climber non-improvements limit
    iteration_limit : int
        Annealing total iterations
    point_limit : int
        Switching point from climber to annealing
    temperature_multiplier : float
        Annealing temperature multiplier
    constraint : bool
        Whether or not to use a hard-constraint for third break term
    semirandom_begin : bool
        Whether or not to use semirandom for begin state
    RETURNS:
        points : Number of maluspoints
        iterations : Number of i
    """

    # Load classrooms, students and courses
    classrooms_list, students_set, course_set = load_all()
    points = 0

    # Fill planner with semirandom method
    while not points:
        planner = Planner(classrooms_list)
        if semirandom_begin:
            semirandom(course_set, classrooms_list, planner, planner.days, planner.times)
        else:
            random_method(course_set, classrooms_list, planner, planner.days, planner.times)
        student_dict = planner.create_student_dict(students_set)
        points = checker(planner.slots, student_dict, constraint)

    # Create object of class hill climber
    hill = HillClimber(
        planner, course_set, students_set, streak_limit, iteration_limit, point_limit, temperature_multiplier, constraint)

    # Run hill climber method and evaluate its results
    iterations = hill.run(algorithm)
    student_dict = planner.create_student_dict(students_set)
    points = checker(planner.slots, student_dict, constraint)

    # Create visualisation and csv dataset from results
    if graph:
        plot(hill.plotx, hill.ploty, algorithm)

    # Save to csv
    store(students_set, planner, points)
    return points, iterations


if __name__ == '__main__':
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description='create a class schedule')

    # Adding arguments
    parser.add_argument('-s', '--streak_limit', type=int, default=1000,
                        help='hill climber non-improvements (default: 1000)')
    parser.add_argument('-p', '--point_limit', type=int, default=200,
                        help='switching point from climber to annealing (default: 200)')
    parser.add_argument('-i', '--iteration_limit', type=int, default=10000,
                        help='annealing iterations (default: 10000)')
    parser.add_argument('-t', '--temperature_multiplier', type=float, default=1,
                        help='annealing temperature multiplier (default: 1)')
    parser.add_argument('-c', '--constraint', type=bool, default=False,
                        help='use hard-constraint for third break term (default: False)')
    parser.add_argument('-r', '--semirandom_begin', type=bool, default=False,
                        help='use semirandom for begin state (default: False)')
    parser.add_argument('-d', '--distribution', type=bool, default=False,
                        help='create distribution histogram (default: False)')
    parser.add_argument('-g', '--graph',   type=bool, default=False,
                        help='create lines graph for single run, do not use together with distribution! (default: False)')
    parser.add_argument('-n', '--runs', type=int, default=1,
                        help='number of runs (default: 1)')
    parser.add_argument('-a', '--algorithm', type=str, default='climber',
                        help='select algorithm: climber, annealing or annealing_climber (default: climber)')

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    points, iterations = [], []
    for _ in range(args.runs):
        new_points, i = main(args.graph, args.algorithm, args.streak_limit, args.iteration_limit, args.point_limit, args.temperature_multiplier, args.constraint, args.semirandom_begin)
        points.append(new_points)
        iterations.append(i)

    print("\n Average: " + str(mean(points)))
    print("\n Average iterations: " + str(mean(iterations)))

    # Create probability distribution from all runs
    if args.distribution:
        distribution(points, args.runs)
