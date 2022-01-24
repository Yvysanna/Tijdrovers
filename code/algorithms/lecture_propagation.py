import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from conflicts import find_course_conflicts
from lecture_climber import HillClimber
import loader
from copy import deepcopy

# Load classrooms and courses
classrooms_list = loader.load_classrooms()
(students_set, course_students) = loader.load_students()
course_set = loader.load_courses(classrooms_list, course_students)
loader.connect_courses(students_set, course_set)
course_dict, conflicting_pairs = find_course_conflicts(
    students_set, course_set)
loader.load_activities(classrooms_list, students_set, course_set)

class Propagation:
    def __init__(self):
        self.climbers = []
        for x in range(6):
            self.climbers.append(HillClimber(course_set))
        self.children = [3,3,2,2,1,1]
        self.change = [1,1,2,3,5,8]

    def propagate(self):
        for _ in range(30000):
            self.climbers.sort(key = lambda climber: climber.points)
            climbers_copy = deepcopy(self.climbers)
            for i in range(len(climbers_copy)):
                for _ in range(self.children[i]):
                    child = deepcopy(climbers_copy[i])
                    for _ in range(self.change[i]):
                        child.random_change()
                    self.climbers.append(child)
            self.climbers.sort(key=lambda climber: climber.points)
            self.climbers = self.climbers[:6]
            print(self.climbers[0])

    def __str__(self):
        string = ""
        for x in self.climbers:
            string += str(x)
        return string

p = Propagation()
print(p)
p.propagate()
