# ==================================================================================
# main.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Usage: python3 main.py
#
# - Creates schedule
# ==================================================================================

# Main class for course planning, holds all information about schedule
from algorithms.planner import Planner

# Algorithm functions
from algorithms.semirandom import semirandom
from algorithms.randommethod import random_method
from algorithms.hill_climber import HillClimber

# Loader function to load all necessary information from dataset
from loader import loadall

# Function to store results in csv
from store import store

# Evaluation function
from checker import checker


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
    classrooms_list, students_set, course_set = loadall()

    # Create planner object
    planner = Planner(classrooms_list)

    # Fill planner with semirandom method
    semirandom(course_set, classrooms_list, planner, planner.days, planner.times)

    # Create object of class hill climber
    hill = HillClimber(planner, course_set, students_set)

    # Run hill climber method and evaluate its results
    hill.run()
    student_dict = planner.create_student_dict(students_set)
    points = checker(planner.slots, student_dict)

    # Create visualtization and csv dataset from results
    hill.plot()
    store(students_set, planner, points)

    return planner.slots, student_dict

if __name__ == '__main__':
    main()
