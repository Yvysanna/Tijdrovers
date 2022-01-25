from copy import deepcopy
from random import randrange, choice
from tokenize import group
import matplotlib.pyplot as plt

import checker


class Register_climber:

    def __init__(self, course_set, planner):
        self._courses = deepcopy(course_set)
        self._students = set()
        for course in self._courses:
            for student in course._students_set:
                self._students.add(student)

        self._planner = planner
        self.plotx = []
        self.ploty = []
        self.students_schedule = self._planner.create_student_dict(self._students)


    def random_change(self):
        # Pick a random tutorial or lab
        possible_activities = []
        possible_tutorials = []
        possible_labs = []
        while len(possible_activities) == 0:
            random_course = choice(self._courses)
            # Only take activities with multiple groups
            if len(random_course._tutorials) > 1:
                possible_tutorials = random_course._tutorials
                possible_activities.extend(random_course._tutorials)

            if len(random_course._labs) > 1:
                possible_labs = random_course._labs
                possible_activities.extend(random_course._labs)

        random_group_1 = choice(possible_activities)
        if random_group_1._type == 'Tutorial':
            possible_activities = possible_tutorials
        elif random_group_1._type == 'Lab':
            possible_activities = possible_labs
        else:
            raise Exception("Group typing incorrect or could not copy activities")

        # Remove group 1 from possible groups to switch with and pick group 2
        possible_activities.remove(random_group_1)
        random_group_2 = choice(possible_activities)

        # Pick a random student from each group and switch them
        random_student_1 = choice(random_group_1._students_list)
        random_student_2 = choice(random_group_2._students_list)

        random_group_1._students_list.remove(random_student_1)
        random_group_2._students_list.remove(random_student_2)
        random_group_1._students_list.append(random_student_2)
        random_group_2._students_list.append(random_student_1)

        random_student_1.activities.remove(random_group_1)
        random_student_2.activities.remove(random_group_2)
        random_student_1.activities.add(random_group_2)
        random_student_2.activities.add(random_group_1)

        return random_group_1, random_group_2, random_student_1, random_student_2


    def undo_change(self, random_group_1, random_group_2, random_student_1, random_student_2):
        # Undo student reassignment
        random_group_1._students_list.remove(random_student_2)
        random_group_2._students_list.remove(random_student_1)
        random_group_1._students_list.append(random_student_1)
        random_group_2._students_list.append(random_student_2)

        random_student_1.activities.remove(random_group_2)
        random_student_2.activities.remove(random_group_1)
        random_student_1.activities.add(random_group_1)
        random_student_2.activities.add(random_group_2)


    def run(self):
        # Check points of first grouping
        streak = 0
        old_points = checker.checker(self._courses, self.students_schedule)
        i = 0
        while streak < 35000:
            if streak % 5000 == 0 and streak > 0:
                print(streak)
            # Randomly switch students and check the score
            random_group_1, random_group_2, random_student_1, random_student_2 = self.random_change()
            self.students_schedule = self._planner.create_student_dict(self._students)
            new_points = checker.checker(self._courses, self.students_schedule)

            if new_points > old_points:
                self.undo_change(random_group_1, random_group_2, random_student_1, random_student_2)
                streak += 1
            else:
                if new_points < old_points:
                    streak = 0
                old_points = new_points
            i += 1
            self.plotx.append(i)
            self.ploty.append(new_points)


    def plot(self):
        plt.plot(self.plotx, self.ploty)
        plt.grid()
        plt.savefig('code/algorithms/plots/climber.png', dpi=1000)
