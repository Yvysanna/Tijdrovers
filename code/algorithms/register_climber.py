from copy import deepcopy
from random import randrange, choice
import matplotlib.pyplot as plt
from statistics import mean


import checker
from planner import Planner
from semirandom import semirandom
from register import Register

class Register_climber:

    def __init__(self, course_set, students_set, planner, classroom_list, days, timeslots):
        self._courses = course_set
        self._students = students_set
        self._planner_original = planner
        self._classrooms = classroom_list
        self._days = days
        self._timeslots = timeslots
        self.plotx = []
        self.ploty = []
        self.students_schedule = self._planner_original.create_student_dict(self._students)


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

        # Pick a random group and determine which type of activity the next group needs to be
        random_group_1 = choice(possible_activities)
        if random_group_1._type == 'Tutorial':
            possible_activities = possible_tutorials
        elif random_group_1._type == 'Lab':
            possible_activities = possible_labs
        else:
            raise Exception("Group typing incorrect or could not copy activities")

        # Remove group 1 from possible groups to switch with
        possible_activities.remove(random_group_1)

        # Pick group 2 and a student from group 1 and move the student to group 2
        random_group_2 = choice(possible_activities)
        random_student_1 = choice(random_group_1._students_list)
        random_student_2 = None

        self.reassign(random_student_1, random_group_1, random_group_2)

        # If group 2 was already full, move a random student from group 2 to group 1
        if random_group_2._max_capacity <= len(random_group_2._students_list):
            random_student_2 = choice(random_group_2._students_list)

            self.reassign(random_student_1, random_group_1, random_group_2)
            self.reassign(random_student_2, random_group_2, random_group_1)

        assert len(random_group_1) < random_group_1._max_capacity, f"Too many students in {random_group_1}"
        assert len(random_group_2) < random_group_2._max_capacity, f"Too many students in {random_group_2}"

        return random_group_1, random_group_2, random_student_1, random_student_2


    def undo_change(self, random_group_1, random_group_2, random_student_1, random_student_2):
        # Undo reassignment
        self.reassign(random_student_1, random_group_2, random_group_1)
        if random_student_2 != None:
            self.reassign(random_student_2, random_group_1, random_group_2)

        assert len(random_group_1) < random_group_1._max_capacity, f"Too many students in {random_group_1}"
        assert len(random_group_2) < random_group_2._max_capacity, f"Too many students in {random_group_2}"


    def reassign(self, student, current_group, new_group):
        
        current_group._students_list.remove(student)
        new_group._students_list.append(student)

        student.activities.remove(current_group)
        student.activities.add(new_group)

    # def randomize_assignment(self):
    #     # Clear connections between students and tutorials/labs
    #     for course in self._courses:
    #         for tutorial in course._tutorials:
    #             tutorial._students_list.clear()
    #         for lab in course._labs:
    #             lab._students_list.clear()

    #         register_course = Register(course)

    #         for student in self._students:
    #             student.activities.clear()
    #             if course in student.courses:
    #                 # Create new random activity groups
    #                 register_course.random_register(student)


    # def run(self):
    #     # Create N new schedules
    #     schedules_number = 500
    #     schedule_set = {}

    #     for i in range(schedules_number):
    #         self.randomize_assignment()
    #         planner = Planner(self._classrooms)
    #         semirandom(self._courses, self._classrooms, planner, self._days, self._timeslots)
    #         schedule_set.add(planner)


    #     streak = 200
    #     old_points = 1000000
    #     i = 0
    #     while streak < 35000:
    #         if streak % 5000 == 0 and streak > 0:
    #             print(streak)

    #         # Randomly switch students and check the mean score over the new schedules
    #         random_group_1, random_group_2, random_student_1, random_student_2 = self.random_change()

    #         points = []
    #         for schedule in schedule_set:
    #             student_dict = schedule.create_student_dict(self._students)
    #             points.append(checker.checker(self._courses, student_dict))

    #         new_points = mean(points)
            
    #         # If new mean score is higher than old score, undo change. Else, keep change
    #         if new_points > old_points:
    #             self.undo_change(random_group_1, random_group_2, random_student_1, random_student_2)
    #             streak += 1
    #         else:
    #             if new_points < old_points:
    #                 streak = 0
    #             old_points = deepcopy(new_points)
    #         i += 1
    #         self.plotx.append(i)
    #         self.ploty.append(new_points)
    #         print(old_points)

    #     print("\n Average: " + str(old_points))


    # def plot(self):
    #     plt.plot(self.plotx, self.ploty)
    #     plt.grid()
    #     plt.savefig('code/algorithms/plots/climber.png', dpi=1000)
