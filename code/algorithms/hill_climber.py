import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from conflicts import find_activity_conflicts
import loader
from random import randrange, choice, random
from itertools import combinations, chain
from copy import deepcopy
import matplotlib.pyplot as plt

sys.setrecursionlimit(10000)


class HillClimber:

    def __init__(self, planner, course_set, students_set):
        self.planner = planner
        self._courses = course_set
        self._students = students_set
        self.plotx = []
        self.ploty = []


    def activity_switch(self):
        # Pick a random activity
        