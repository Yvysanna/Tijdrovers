import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import matplotlib.pyplot as plt
from copy import deepcopy
from itertools import combinations
from random import randrange, choice, random
import loader
from conflicts import find_course_conflicts


# Load classrooms and courses
classrooms_list = loader.load_classrooms()
(students_set, course_students) = loader.load_students()
course_set = loader.load_courses(classrooms_list, course_students)
loader.connect_courses(students_set, course_set)
course_dict, conflicting_pairs = find_course_conflicts(
    students_set, course_set)
loader.load_activities(classrooms_list, students_set, course_set)


class Annealing:

    def __init__(self, course_set):
        self.timeslots = []
        for _ in range(20):
            self.timeslots.append([])
        for course in course_set:
            for _ in course._lectures:
                index = randrange(0, 20)
                self.timeslots[index].append(course.name)
        self.plotx = []
        self.ploty = []
        self.points = self.count_conflicts()

    def random_change(self):
        # Pick a random lecture
        random_slot = []
        while len(random_slot) == 0:
            index1 = choice(range(len(self.timeslots)))
            random_slot = self.timeslots[index1]
        index2 = choice(range(len(random_slot)))
        random_pick = self.timeslots[index1][index2]

        # Randomly move lecture elsewhere
        self.timeslots[index1].remove(random_pick)
        new_index = randrange(0, 20)
        self.timeslots[new_index].append(random_pick)

        self.points = self.count_conflicts()
        return self.timeslots

    def count_conflicts(self):
        malus = 0
        for slot in self.timeslots:
            if len(slot) > 1:
                combs = list(combinations(slot, 2))
                for conflict in combs:
                    for course1 in course_dict.items():
                        if course1[0].name == conflict[0]:
                            for course2 in course_dict.items():
                                if course2[0].name == conflict[1]:
                                    malus += len(course_dict[course1[0]]
                                                 [course2[0]])
                                    if conflict[0] == conflict[1]:
                                        malus += course1[0].students_number
        return malus

    def run(self):
        streak = 0
        old_slots = self.timeslots
        old_points = self.count_conflicts()
        Tstart = old_points
        for x in range(35000):
            if x % 1000 == 0:
                print(x, self.points)
            self.timeslots = deepcopy(old_slots)
            self.timeslots = self.random_change()
            self.points = self.count_conflicts()
            T = Tstart * (0.9997**x)
            chance = 2**((old_points - self.points)/T)
            r = random()

            if r > chance:
                self.timeslots = old_slots
                self.points = old_points
                streak += 1
            else:
                if self.points < old_points:
                    streak = 0
                old_slots = self.timeslots
                old_points = self.points
            self.plotx.append(x)
            self.ploty.append(self.points)

        return self.timeslots

    def plot(self):
        plt.plot(self.plotx, self.ploty)
        plt.grid()
        plt.savefig('code/algorithms/plots/annealing.png', dpi=1000)

    def __str__(self):
        string = ""
        for x in self.timeslots:
            string += str(x) + '\n'
        string += str(self.count_conflicts())
        return string


hill = Annealing(course_set)
print(hill)
print()
hill.run()
print(hill)
hill.plot()
