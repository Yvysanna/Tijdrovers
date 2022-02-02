import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from random import randrange, choice, random
import matplotlib.pyplot as plt
from checker import checker
import time

sys.setrecursionlimit(10000)


class HillClimber:

    def __init__(self, planner, course_set, students_set):
        self.planner = planner
        self._courses = tuple(course_set)
        self._students = tuple(students_set)
        self.plotx = []
        self.ploty = []


    def activity_switch(self):
        # Pick two random activities, making sure they are not the same activity
        index_activity_1 = randrange(0, len(self.planner.slots))
        random_activity_1 = self.planner.slots[index_activity_1]
        while True:
            index_activity_2 = randrange(0, len(self.planner.slots))
            random_activity_2 = self.planner.slots[index_activity_2]
            if random_activity_1 != random_activity_2:
                break
        
        # Switch the position of the activities in the schedule
        self.planner.slots[index_activity_1] = random_activity_2
        self.planner.slots[index_activity_2] = random_activity_1

        return(index_activity_1, index_activity_2)


    def undo_activity_switch(self, index_activity_1, index_activity_2):
        # Switch activities back to previous state
        previous_activity_2 = self.planner.slots[index_activity_1]
        previous_activity_1 = self.planner.slots[index_activity_2]

        self.planner.slots[index_activity_1] = previous_activity_1
        self.planner.slots[index_activity_2] = previous_activity_2


    def reassign(self):
        # Pick a random tutorial or lab
        possible_activities = []
        possible_tutorials = []
        possible_labs = []
        while len(possible_activities) == 0:
            random_course = choice(self._courses)
            # Only take activities with multiple groups
            if len(random_course._tutorials) > 1:
                possible_tutorials.extend(random_course._tutorials)
                possible_activities.extend(random_course._tutorials)

            if len(random_course._labs) > 1:
                possible_labs.extend(random_course._labs)
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

        self.student_switch(random_student_1, random_group_1, random_group_2)

        # If group 2 was already full, move a random student from group 2 to group 1
        if random_group_2._max_capacity <= len(random_group_2._students_list):
            random_student_2 = choice(random_group_2._students_list)

            self.student_switch(random_student_2, random_group_2, random_group_1)

        assert len(random_group_1._students_list) <= random_group_1._max_capacity, f"Too many students in {random_group_1}: {len(random_group_1._students_list)}"
        assert len(random_group_2._students_list) <= random_group_2._max_capacity, f"Too many students in {random_group_2}: {len(random_group_2._students_list)}"

        return random_group_1, random_group_2, random_student_1, random_student_2


    def undo_reassign(self, random_group_1, random_group_2, random_student_1, random_student_2):
        # Undo reassignment
        self.student_switch(random_student_1, random_group_2, random_group_1)
        if random_student_2 != None:
            self.student_switch(random_student_2, random_group_1, random_group_2)

        assert len(random_group_1._students_list) <= random_group_1._max_capacity, f"Too many students in {random_group_1}: {len(random_group_1._students_list)}"
        assert len(random_group_2._students_list) <= random_group_2._max_capacity, f"Too many students in {random_group_2}: {len(random_group_2._students_list)}"


    def student_switch(self, student, current_group, new_group):

        current_group._students_list.remove(student)
        new_group._students_list.append(student)

        student.activities.remove(current_group)
        student.activities.add(new_group)


    def run(self):
        # start = time.time()
        streak = 0
        i = 0
        # Count current maluspoints
        student_dict = self.planner.create_student_dict(self._students)
        old_points = checker(self.planner.slots, student_dict)

        while streak < 3000:
            # if i % 100000 == 0:
            #     print(time.time() - start, i, streak, old_points)

            index_activity_1, index_activity_2 = self.activity_switch()
            student_dict = self.planner.create_student_dict(self._students)
            new_points = checker(self.planner.slots, student_dict)

            if new_points == False or new_points > old_points:
                self.undo_activity_switch(index_activity_1, index_activity_2)
                streak += 1
            else:
                if new_points < old_points:
                    streak = 0
                old_points = new_points

            i += 1
            # self.plotx.append(i)
            # self.ploty.append(old_points)

            random_group_1, random_group_2, random_student_1, random_student_2 = self.reassign()
            student_dict = self.planner.create_student_dict(self._students)
            new_points = checker(self.planner.slots, student_dict)

            if new_points == False or new_points > old_points:
                self.undo_reassign(random_group_1, random_group_2, random_student_1, random_student_2)
                streak += 1
            else:
                if new_points < old_points:
                    streak = 0
                old_points = new_points

            i += 1
            # self.plotx.append(i)
            # self.ploty.append(old_points)

        return i


    def run_annealing_climber(self):
        streak = 0
        i = 0
        # Count current maluspoints
        student_dict = self.planner.create_student_dict(self._students)
        old_points = checker(self.planner.slots, student_dict)

        while old_points > 150:
            print(i, streak, old_points)

            index_activity_1, index_activity_2 = self.activity_switch()
            student_dict = self.planner.create_student_dict(self._students)
            new_points = checker(self.planner.slots, student_dict)

            if new_points == False or new_points > old_points:
                self.undo_activity_switch(index_activity_1, index_activity_2)
                streak += 1
            else:
                if new_points < old_points:
                    streak = 0
                old_points = new_points

            i += 1
            # self.plotx.append(i)
            # self.ploty.append(old_points)

            random_group_1, random_group_2, random_student_1, random_student_2 = self.reassign()
            student_dict = self.planner.create_student_dict(self._students)
            new_points = checker(self.planner.slots, student_dict)

            if new_points == False or new_points > old_points:
                self.undo_reassign(random_group_1, random_group_2, random_student_1, random_student_2)
                streak += 1
            else:
                if new_points < old_points:
                    streak = 0
                old_points = new_points

            i += 1
            # self.plotx.append(i)
            # self.ploty.append(old_points)

        x = 1
        Tstart = old_points

        while streak < 100 or x < 20000:
            print(i, streak, old_points)

            index_activity_1, index_activity_2 = self.activity_switch()
            student_dict = self.planner.create_student_dict(self._students)
            new_points = checker(self.planner.slots, student_dict)

            T = Tstart * (0.9997**x)
            print(T, Tstart, x)
            chance = 2**((old_points - new_points)/(0.02*T))
            r = random()

            if r > chance:
                self.undo_activity_switch(index_activity_1, index_activity_2)
                streak += 1
            else:
                if new_points < old_points:
                    streak = 0
                old_points = new_points

            x += 1
            i += 1
            # self.plotx.append(i)
            # self.ploty.append(new_points)

            random_group_1, random_group_2, random_student_1, random_student_2 = self.reassign()
            student_dict = self.planner.create_student_dict(self._students)
            new_points = checker(self.planner.slots, student_dict)

            T = Tstart * (0.9997**x)
            print(T, Tstart, x)
            chance = 2**((old_points - new_points)/(0.02*T))
            r = random()

            if r > chance:
                self.undo_reassign(random_group_1, random_group_2, random_student_1, random_student_2)
                streak += 1
            else:
                streak = 0
                old_points = new_points

            x += 1
            i += 1
            # self.plotx.append(i)
            # self.ploty.append(new_points)

        while streak < 100:
            print(i, streak, old_points)

            index_activity_1, index_activity_2 = self.activity_switch()
            student_dict = self.planner.create_student_dict(self._students)
            new_points = checker(self.planner.slots, student_dict)

            if new_points == False or new_points > old_points:
                self.undo_activity_switch(index_activity_1, index_activity_2)
                streak += 1
            else:
                if new_points < old_points:
                    streak = 0
                old_points = new_points

            i += 1
            # self.plotx.append(i)
            # self.ploty.append(old_points)

            random_group_1, random_group_2, random_student_1, random_student_2 = self.reassign()
            student_dict = self.planner.create_student_dict(self._students)
            new_points = checker(self.planner.slots, student_dict)

            if new_points == False or new_points > old_points:
                self.undo_reassign(random_group_1, random_group_2, random_student_1, random_student_2)
                streak += 1
            else:
                if new_points < old_points:
                    streak = 0
                old_points = new_points

            i += 1

        return i



    def run_annealing(self):
        streak = 0
        # Count current maluspoints
        student_dict = self.planner.create_student_dict(self._students)
        old_points = checker(self.planner.slots, student_dict)

        Tstart = old_points
        for x in range(35000):

            index_activity_1, index_activity_2 = self.activity_switch()
            student_dict = self.planner.create_student_dict(self._students)
            new_points = checker(self.planner.slots, student_dict)

            T = Tstart * (0.9997**x)
            chance = 2**((old_points - new_points)/T)
            r = random()

            if r > chance:
                self.undo_activity_switch(index_activity_1, index_activity_2)
                streak += 1
            else:
                if new_points < old_points:
                    streak = 0
                old_points = new_points

            # self.plotx.append(x)
            # self.ploty.append(new_points)

            random_group_1, random_group_2, random_student_1, random_student_2 = self.reassign()
            student_dict = self.planner.create_student_dict(self._students)
            new_points = checker(self.planner.slots, student_dict)

            if new_points == False or new_points > old_points:
                self.undo_reassign(random_group_1, random_group_2, random_student_1, random_student_2)
                streak += 1
            else:
                if new_points < old_points:
                    streak = 0
                old_points = new_points
                

        return x

            # self.plotx.append(x)
            # self.ploty.append(new_points)

    def run_annealing_exp(self):
        # Count current maluspoints
        i = 0
        student_dict = self.planner.create_student_dict(self._students)
        old_points = checker(self.planner.slots, student_dict)
        Tstart = old_points
        for x in range(20000):

            index_activity_1, index_activity_2 = self.activity_switch()
            student_dict = self.planner.create_student_dict(self._students)
            new_points = checker(self.planner.slots, student_dict)

            T = Tstart * (0.9997**i)
            if new_points == False:
                chance = 0
            else:
                chance = 2**((old_points - new_points)/T)
            print(i, old_points, T, new_points, chance)
            r = random()

            if new_points == False or r > chance:
                self.undo_activity_switch(index_activity_1, index_activity_2)
                streak += 1
            else:
                if new_points < old_points:
                    streak = 0
                old_points = new_points

            i += 1
            self.plotx.append(i)
            self.ploty.append(old_points)

            random_group_1, random_group_2, random_student_1, random_student_2 = self.reassign()
            student_dict = self.planner.create_student_dict(self._students)
            new_points = checker(self.planner.slots, student_dict)

            T = Tstart * (0.9997**i)
            if new_points == False:
                chance = 0
            else:
                chance = 2**((old_points - new_points)/T)
            print(i, old_points, T, new_points, chance)
            r = random()

            if new_points == False or r > chance:
                self.undo_reassign(random_group_1, random_group_2,
                                   random_student_1, random_student_2)
                streak += 1
            else:
                if new_points < old_points:
                    streak = 0
                old_points = new_points

            i += 1
            self.plotx.append(i)
            self.ploty.append(old_points)

    def run_annealing_lin(self):
        # Count current maluspoints
        i = 0
        student_dict = self.planner.create_student_dict(self._students)
        old_points = checker(self.planner.slots, student_dict)
        Tstart = old_points
        for x in range(20000):

            index_activity_1, index_activity_2 = self.activity_switch()
            student_dict = self.planner.create_student_dict(self._students)
            new_points = checker(self.planner.slots, student_dict)

            T = Tstart - (Tstart/40000) * i
            if new_points == False:
                chance = 0
            else:
                chance = 2**((old_points - new_points)/T)
            print(i, old_points, T, new_points, chance)
            r = random()

            if new_points == False or r > chance:
                self.undo_activity_switch(index_activity_1, index_activity_2)
            else:
                if new_points < old_points:
                    streak = 0
                old_points = new_points

            i += 1
            self.plotx.append(i)
            self.ploty.append(old_points)

            random_group_1, random_group_2, random_student_1, random_student_2 = self.reassign()
            student_dict = self.planner.create_student_dict(self._students)
            new_points = checker(self.planner.slots, student_dict)

            T = Tstart - (Tstart/40000) * i
            if new_points == False:
                chance = 0
            else:
                chance = 2**((old_points - new_points)/T)
            print(i, old_points, T, new_points, chance)
            r = random()

            if new_points == False or r > chance:
                self.undo_reassign(random_group_1, random_group_2,
                                   random_student_1, random_student_2)
                streak += 1
            else:
                if new_points < old_points:
                    streak = 0
                old_points = new_points

            i += 1
            self.plotx.append(i)
            self.ploty.append(old_points)


    def plot(self):
        plt.plot(self.plotx, self.ploty)
        plt.ylim(0)
        plt.xlabel("Iterations")
        plt.ylabel("Maluspoints")
        plt.title("Points during hill climber which stops after 1000 non-improvements")
        plt.grid()
        plt.savefig('code/algorithms/plots/climber1000.png', dpi=1000)


    def add_value(self, i, new_points):
        i += 1
        self.plotx.append(i)
        self.ploty.append(new_points)
