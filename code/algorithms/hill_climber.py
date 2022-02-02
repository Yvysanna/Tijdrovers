import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from random import choice, random, sample

from checker import checker

sys.setrecursionlimit(10000)


class HillClimber:

    def __init__(self, planner, course_set, students_set, streak_limit, iteration_limit, point_limit, temperature_multiplier):
        self.planner = planner
        self._courses = tuple(course_set)
        self._students = tuple(students_set)
        self._algorithms = ['climber', 'annealing', 'climber_annealing']
        self.streak_limit = streak_limit
        self.iteration_limit = iteration_limit
        self.point_limit = point_limit
        self.temperature_multiplier = temperature_multiplier
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

        # Switch the position of the activities in the planner
        self.planner.swap_activities(index_activity_1, index_activity_2)
        return(index_activity_1, index_activity_2)


    def undo_activity_switch(self, index_activity_1, index_activity_2):
        """
        ARGS: 
            self
            index_activity_1, index_activity_2: index number of switched activities
        USAGE:
            Switching the timeslots for two activities with each other
        RETURNS: 
            None
        """
        # Switch activities back to previous state
        self.planner.swap_activities(index_activity_1, index_activity_2)

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
        """
        ARGS: 
            self
            student: student object
            current_group, new_group: activity objects for the groups from the switched student
        USAGE:
            Switching the activity group for student
        RETURNS: 
            None
        """
        # Switch student object from old to new group
        current_group.student_list.remove(student)
        new_group.student_list.append(student)

        student.remove_activity(current_group)
        student.add_activity(new_group)

    
    def activity_climber(self, current_streak, old_points, X=None, Tstart=None):
        """
        ARGS: 
            self
            current_streak: current number of consecutive non-improvements
            old_points: number of points
            X: current iteration in simulated annealing
            Tstart: start temperature in simulated annealing
        USAGE:
            Generating the next activity switch and determining if change will be kept
        RETURNS: 
            current_streak, old_points: updated values
        """
        # Change slot of activity randomly
        index_activity_1, index_activity_2 = self.activity_switch()
        student_dict = self.planner.create_student_dict(self._students)
        new_points = checker(self.planner.slots, student_dict)

        # Determine if climber or annealer comparison is needed
        if Tstart == None:
            comparison_value = new_points
            comparison_base = old_points
        else:
            T = Tstart * (0.9997**X)
            chance = 2**((old_points - new_points)/(self.temperature_multiplier*T))
            r = random()

            comparison_value = r
            comparison_base = chance

        # Check if improvement was made, allows hard constraints
        if new_points == False or comparison_value > comparison_base:
            self.undo_activity_switch(index_activity_1, index_activity_2)
            current_streak += 1
        else:
            # Only reset streak if improvement is made
            if new_points < old_points:
                current_streak = 0
            old_points = new_points

        return current_streak, old_points


    def student_climber(self, current_streak, old_points, X=None, Tstart=None):
        """
        ARGS: 
            self
            current_streak: current number of consecutive non-improvements
            old_points: number of points
            X: current iteration in simulated annealing
            Tstart: start temperature in simulated annealing
        USAGE:
            Generating the next student switch and determining if change will be kept
        RETURNS: 
            current_streak, old_points: updated values
        """
        # Change a random activity group for a random student
        random_group_1, random_group_2, random_student_1, random_student_2 = self.reassign()
        student_dict = self.planner.create_student_dict(self._students)
        new_points = checker(self.planner.slots, student_dict)

        # Determine if climber or annealer comparison is needed
        if Tstart == None:
            comparison_value = new_points
            comparison_base = old_points
        else:
            T = Tstart * (0.9997**X)
            chance = 2**((old_points - new_points)/(self.temperature_multiplier*T))
            r = random()

            comparison_value = r
            comparison_base = chance
            
        # Check if improvement was made, allows hard constraints
        if new_points == False or comparison_value > comparison_base:
            self.undo_reassign(random_group_1, random_group_2, random_student_1, random_student_2)
            current_streak += 1
        else:
            if new_points < old_points:
                current_streak = 0
            old_points = new_points

        return current_streak, old_points


    def add_value(self, iteration, old_points):
        """
        ARGS: 
            self
            i: current iteration
            old_points: number of points
        USAGE:
            Saves data point for graph
        RETURNS: 
            None
        """
        self.plotx.append(iteration)
        self.ploty.append(old_points)


    def run(self, algorithm):
        """
        ARGS:
            self
            algorithm: algorithm type to run
        USAGE:
            Improves a given schedule by:
            * switching two activities in day and or time,
            * evaluating improvement and undoing it if unsuccessful
            * switching two students from the same activity but different groups
            * evaluating improvement again and undoing it if unsuccessful

        RETURNS:
            iteration: the total count of iterations made
        """
        if algorithm not in self._algorithms:
            raise Exception("Algorithm is invalid")

        current_streak = 0
        iteration = 0

        # Count current maluspoints
        student_dict = self.planner.create_student_dict(self._students)
        old_points = checker(self.planner.slots, student_dict)

        # Check which algorithm is used and run appropriate loops
        if algorithm == 'climber-annealing':
            while old_points > self.point_limit:
                current_streak, old_points = self.activity_climber(current_streak, old_points)
                iteration += 1
                self.add_value(iteration, old_points)
                
                current_streak, old_points = self.student_climber(current_streak, old_points)
                iteration += 1
                self.add_value(iteration, old_points)

        tstart = old_points

        if algorithm == 'annealing' or algorithm == 'climber-annealing':
            for x in range(self.iteration_limit):

                current_streak, old_points = self.activity_climber(current_streak, old_points, X=x, Tstart=tstart)
                iteration += 1
                self.add_value(iteration, old_points)

                current_streak, old_points = self.student_climber(current_streak, old_points, X=x, Tstart=tstart)
                iteration += 1
                self.add_value(iteration, old_points)

        if algorithm == 'climber' or algorithm == 'climber-annealing':
            while current_streak < self.streak_limit:
                current_streak, old_points = self.activity_climber(current_streak, old_points)
                iteration += 1
                self.add_value(iteration, old_points)
                
                current_streak, old_points = self.student_climber(current_streak, old_points)
                iteration += 1
                self.add_value(iteration, old_points)

        return iteration


