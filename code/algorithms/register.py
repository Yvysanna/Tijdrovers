import random


class Register:

    def __init__(self, course):

        self._course = course

    def register(self, student):

        possible_tutorials = {}
        possible_labs = {}

        # Add every lecture to student activity list
        for lecture in self._course._lectures:
            student.activities.add(lecture)

        if len(self._course._tutorials) > 0:
            # Check for every tutorial group with available spots the total of shared classes with current students in group
            for tutorial in self._course._tutorials:
                if len(tutorial._students_list) < self._course._tutorials_max:
                    shared_classes = 0
                    for classmate in tutorial._students_list:
                        shared_classes += student.classmates[classmate]

                    possible_tutorials[tutorial] = shared_classes

            # If all groups have the same number of existing classmates, put student in random group
            # https://stackoverflow.com/questions/35253971/how-to-check-if-all-values-of-a-dictionary-are-0
            if all(value == list(possible_tutorials.values())[0] for value in possible_tutorials.values()):
                assigned_tutorial = random.choice(list(possible_tutorials.keys()))
            else:
                # Put the student in the tutorial group that has the most students with shared classes
                assigned_tutorial = max(possible_tutorials, key=possible_tutorials.get)

            # Add another shared group with every classmate in tutorial
            for classmate in assigned_tutorial._students_list:
                classmate.classmates[student] += 1
                student.classmates[classmate] += 1

            # Create connection between tutorial group and student
            assigned_tutorial._students_list.append(student)
            student.activities.add(assigned_tutorial)

        if len(self._course._labs) > 0:
            # Repeat for labs
            for lab in self._course._labs:
                if len(lab._students_list) < self._course._lab_max:
                    shared_classes = 0
                    for classmate in lab._students_list:
                        shared_classes += student.classmates[classmate]

                    possible_labs[lab] = shared_classes

            if all(value == list(possible_labs.values())[0] for value in possible_labs.values()):
                assigned_lab = random.choice(list(possible_labs.keys()))
            else:
                assigned_lab = max(possible_labs, key=possible_labs.get)

            for classmate in assigned_lab._students_list:
                classmate.classmates[student] += 1
                student.classmates[classmate] += 1

            assigned_lab._students_list.append(student)
            student.activities.add(assigned_lab)


    def random_register(self, student):

        possible_tutorials = []
        possible_labs = []

        # Add student to every lecture and add every lecture to student activity list
        for lecture in self._course._lectures:
            student.activities.add(lecture)

        if len(self._course._tutorials) > 0:
            # Check for every tutorial group with available spots
            for tutorial in self._course._tutorials:
                if len(tutorial._students_list) < self._course._tutorials_max:
                    possible_tutorials.append(tutorial)

            assigned_tutorial = random.choice(possible_tutorials)

            assigned_tutorial._students_list.append(student)
            student.activities.add(assigned_tutorial)

        if len(self._course._labs) > 0:
            # Repeat for labs
            for lab in self._course._labs:
                if len(lab._students_list) < self._course._lab_max:
                    possible_labs.append(lab)

            assigned_lab = random.choice(possible_labs)

            assigned_lab._students_list.append(student)
            student.activities.add(assigned_lab)



    def register_helper(self, student, activities):
        pass