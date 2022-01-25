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


# Load classrooms and courses
classrooms_list = loader.load_classrooms()
(students_set, course_students) = loader.load_students()
course_set = loader.load_courses(classrooms_list, course_students)
loader.connect_courses(students_set, course_set)
loader.load_activities(classrooms_list, students_set, course_set)
course_dict = find_activity_conflicts(
    course_set, students_set)


class Annealing:

    def __init__(self, course_set):
        self.timeslots = []
        for _ in range(20):
            self.timeslots.append([])
        for course in course_set:
            for activity in chain(course._lectures, course._tutorials, course._labs):
                scheduled = False
                while not scheduled:
                    index = randrange(0, 20)
                    if len(self.timeslots[index]) != 7:
                        self.timeslots[index].append(activity._name)
                        scheduled = True
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
        scheduled = False
        while not scheduled:
            new_index = randrange(0, 20)
            if len(self.timeslots[new_index]) != 7:
                self.timeslots[new_index].append(random_pick)
                scheduled = True

        self.points = self.count_conflicts()
        return self.timeslots

    def count_conflicts(self):
        malus = 0
        for slot in self.timeslots:
            if len(slot) > 1:
                combs = list(combinations(slot, 2))
                for conflict in combs:
                    for activity1 in course_dict.items():
                        if conflict[0] == activity1[0]._name:
                            for activity2 in activity1[1]:
                                if conflict[1] == activity2._name:
                                    malus += len(course_dict[activity1[0]]
                                                 [activity2])
        return malus

    def run(self):
        streak = 0
        old_slots = self.timeslots
        old_points = self.count_conflicts()
        i = 0
        while streak < 5000:
            print(streak, self.points)
            self.timeslots = deepcopy(old_slots)
            self.timeslots = self.random_change()

            if self.points > old_points:
                self.timeslots = old_slots
                self.points = old_points
                streak += 1
            else:
                if self.points < old_points:
                    streak = 0
                old_slots = self.timeslots
                old_points = self.points
            i += 1
            self.plotx.append(i)
            self.ploty.append(self.points)

        self.print_conflicts()

        return self.timeslots

    def plot(self):
        plt.plot(self.plotx, self.ploty)
        plt.grid()
        plt.savefig('code/algorithms/plots/climber2.png', dpi=1000)

    def print_conflicts(self):
        malus = 0
        for slot in self.timeslots:
            if len(slot) > 1:
                combs = list(combinations(slot, 2))
                for conflict in combs:
                    for course in course_set:
                        for activity1 in chain(course._lectures, course._tutorials, course._labs):
                            if activity1._name == conflict[0]:
                                for course in course_set:
                                    for activity2 in chain(course._lectures, course._tutorials, course._labs):
                                        if activity2._name == conflict[1]:
                                            for student in activity1._students_list:
                                                if student in activity2._students_list:
                                                    malus += 1
                                                    print(activity1, activity2)
                                                    print(student)
                                                    print(
                                                        "Points: " + str(malus))
                                                    print()
        return malus

    def __str__(self):
        string = ""
        a = 0
        for x in self.timeslots:
            a += len(x)
            string += str(x) + str(len(x))+'\n'
        string += str(self.count_conflicts())
        return string


hill = Annealing(course_set)
print(hill)
hill.run()
print(hill)
hill.plot()
