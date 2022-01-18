import random


class Register:

    def __init__(self, course):

        self._course = course
        self.possible_tutorials = {}
        self.possible_labs = {}

    def register(self, student):

        # Add student to every lecture and add every lecture to student activity list
        for lecture in self._course._lectures:
            student.activities.add(lecture)

            # Add this student as classmate to everyone already in this lecture
            for classmate in lecture._students_list:
                classmate.classmates.add(student)

            # Add students in this lecture to current student's classmates
            student.classmates.update(lecture._students_list)

        if len(self._course._tutorials) > 0:
            # Check for every tutorial group with available spots how many other students this student is already classmates with
            for tutorial in self._course._tutorials:
                if len(tutorial._students_list) < self._course._tutorials_max:
                    self.possible_tutorials[tutorial] = set(tutorial._students_list).intersection(student.classmates)

            # If all groups have the same number of existing classmates, put student in random group
            # https://stackoverflow.com/questions/35253971/how-to-check-if-all-values-of-a-dictionary-are-0
            if all(value == list(self.possible_tutorials.values())[0] for value in self.possible_tutorials.values()):
                assigned_tutorial = random.choice(list(self.possible_tutorials.keys()))
            else:
                # Put the student in the tutorial group that has the most students with shared classes
                assigned_tutorial = max(self.possible_tutorials, key=self.possible_tutorials.get)

            # Add this student as classmate to everyone already in this tutorial
            for classmate in assigned_tutorial._students_list:
                classmate.classmates.add(student)

            # Add students in this group to current student's classmates
            student.classmates.update(assigned_tutorial._students_list)

            assigned_tutorial._students_list.append(student)
            student.activities.add(assigned_tutorial)

        if len(self._course._labs) > 0:
            # Repeat for labs
            for lab in self._course._labs:
                if len(lab._students_list) < self._course._lab_max:
                    self.possible_labs[lab] = set(lab._students_list).intersection(student.classmates)

            if all(value == list(self.possible_labs.values())[0] for value in self.possible_labs.values()):
                assigned_lab = random.choice(list(self.possible_labs.keys()))
            else:
                assigned_lab = max(self.possible_labs, key=self.possible_labs.get)

            for classmate in assigned_lab._students_list:
                classmate.classmates.add(student)

            student.classmates.update(assigned_lab._students_list)

            assigned_lab._students_list.append(student)
            student.activities.add(assigned_lab)


    def register_helper(self, student, activities):
        pass