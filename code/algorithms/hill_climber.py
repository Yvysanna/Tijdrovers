import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from random import choice, random, sample

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
        """
        ARGS: 
            self 
        USAGE:
            Switching the timeslots for two activities with each other
        RETURNS: 
            index_activity_1, index_activity_2: indices of the two switched activity objects
        """
        # Pick two random activities, making sure they are not the same activity        
        # https://stackoverflow.com/questions/22842289/generate-n-unique-random-numbers-within-a-range
        index_activity_1, index_activity_2 = sample(range(0, len(self.planner.slots)),2)
        #print(f'old activity: {self.planner.slots[index_activity_1]}')
        # Switch the position of the activities in the planner
        self.planner.swap_activities(index_activity_1, index_activity_2)
        #print(f'new activity: {self.planner.slots[index_activity_1]}')
        return(index_activity_1, index_activity_2)


    def undo_activity_switch(self, index_activity_1, index_activity_2):
        """
        ARGS: 
            self
            index_activity_1: int
            index_activity_2  
        USAGE:
            Switching the timeslots for two activities with each other
        RETURNS: 
            index_activity_1, index_activity_2: the indices of the switched activities
        """
        # Switch activities back to previous state
        #print(f'switched indexe 1:{index_activity_1}')
        self.planner.swap_activities(index_activity_1, index_activity_2)
        #print(f'back to old:{self.planner.slots[index_activity_1]}')

    def reassign(self):
        """
        ARGS: 
            self
        USAGE:
            Switching a random student from a random course activity group with 
            another random student from the same course activity but different group
        RETURNS: 
            random_group_1, random_group_2: activity objects for the groups from the switched students
            random_student_1, random_student_2: student objects of the switched students
        """
        # Pick a random tutorial or lab
        possible_activities = []
        possible_tutorials = []
        possible_labs = []
        while len(possible_activities) == 0:
            random_course = choice(self._courses)
            # Only take activities with multiple groups
            if len(random_course.tutorials) > 1:
                possible_tutorials.extend(random_course.tutorials)
                possible_activities.extend(random_course.tutorials)

            if len(random_course.labs) > 1:
                possible_labs.extend(random_course.labs)
                possible_activities.extend(random_course.labs)

        # Pick a random group and determine which type of activity the next group needs to be
        random_group_1 = choice(possible_activities)
        if random_group_1.type == 'Werkcollege':
            possible_activities = possible_tutorials
        elif random_group_1.type == 'Practica':
            possible_activities = possible_labs
        else:
            raise Exception("Group typing incorrect or could not copy activities")

        # Remove group 1 from possible groups to switch with
        possible_activities.remove(random_group_1)

        # Pick group 2 and a student from group 1 and move the student to group 2
        random_group_2 = choice(possible_activities)
        random_student_1 = choice(random_group_1.student_list)
        random_student_2 = None

        self.student_switch(random_student_1, random_group_1, random_group_2)

        # If group 2 was already full, move a random student from group 2 to group 1
        if random_group_2.max_students <= len(random_group_2.student_list):
            random_student_2 = choice(random_group_2.student_list)

            self.student_switch(random_student_2, random_group_2, random_group_1)

        assert len(random_group_1.student_list) <= random_group_1.max_students, f"Too many students in {random_group_1}: {len(random_group_1.student_list)}"
        assert len(random_group_2.student_list) <= random_group_2.max_students, f"Too many students in {random_group_2}: {len(random_group_2.student_list)}"

        return random_group_1, random_group_2, random_student_1, random_student_2


    def undo_reassign(self, random_group_1, random_group_2, random_student_1, random_student_2):
        """
        ARGS: 
            self
            random_group_1, random_group_2: activity objects for the groups from the switched students
            random_student_1, random_student_2: student objects of the switched students
        USAGE:
            Switching the previously switched students back into their previous activity groups
        RETURNS: 
            None
        """
        # Undo reassignment
        self.student_switch(random_student_1, random_group_2, random_group_1)
        if random_student_2 != None:
            self.student_switch(random_student_2, random_group_1, random_group_2)

        assert len(random_group_1.student_list) <= random_group_1.max_students, f"Too many students in {random_group_1}: {len(random_group_1.student_list)}"
        assert len(random_group_2.student_list) <= random_group_2.max_students, f"Too many students in {random_group_2}: {len(random_group_2.student_list)}"


    def student_switch(self, student, current_group, new_group):

        current_group.student_list.remove(student)
        new_group.student_list.append(student)

        student.remove_activity(current_group)
        student.add_activity(new_group)


    def run(self, n):
        # start = time.time()
        """
        ARGS:
            self
        USAGE:
            Improves a given schedule by:
            * switching two activities in day and or time,
            * evaluating improvement and undoing it if unsuccessful
            * switching two students from the same activity but different groups
            * evaluating improvement again and undoing it if unsuccessful

        RETURNS:
            i: the total count of iterations made
        """
        streak = 0
        i = 0

        # Count current maluspoints
        student_dict = self.planner.create_student_dict(self._students)
        old_points = checker(self.planner.slots, student_dict)

        while streak < n:
            # if i % 100000 == 0:
            #     print(time.time() - start, i, streak, old_points)

            # Activity climber
            index_activity_1, index_activity_2 = self.activity_switch()
            student_dict = self.planner.create_student_dict(self._students)
            new_points = checker(self.planner.slots, student_dict)

            # Check if improvement was made, allows hard constraints
            if new_points == False or new_points > old_points:
                self.undo_activity_switch(index_activity_1, index_activity_2)
                streak += 1

            else:
                # Only reset streak if improvement is made
                if new_points < old_points:
                    streak = 0
                old_points = new_points

            i += 1
            # self.plotx.append(i)
            # self.ploty.append(old_points)

            # Student switch climber
            random_group_1, random_group_2, random_student_1, random_student_2 = self.reassign()
            student_dict = self.planner.create_student_dict(self._students)
            new_points = checker(self.planner.slots, student_dict)
            print(i, streak, old_points)

            # Check if improvement was made, allows hard constraints
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


    def run_annealing_climber(self, n):
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
            self.plotx.append(i)
            self.ploty.append(old_points)

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
            self.plotx.append(i)
            self.ploty.append(old_points)

        x = 1
        Tstart = old_points

        while streak < n or x < 20000:
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

        while streak < n:
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


    def run_annealing(self, n):
        streak = 0
        # Count current maluspoints
        student_dict = self.planner.create_student_dict(self._students)
        old_points = checker(self.planner.slots, student_dict)

        Tstart = old_points
        for x in range(n):

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
        for x in range(10):

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
