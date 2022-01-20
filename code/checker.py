# ==================================================================================
# checker.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Checks the amount of maluspoints for a schedule
# ==================================================================================

import csv
from itertools import chain
from collections import Counter


def count_points(classroom_list, course_set):
    malus = 0

    # Open schedule
    with open('data/results/results.csv', 'r', encoding="ISO-8859-1") as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)

        # Desired datatype: {Student : [{Day : [Timeslot]}]}
        student_dict = {}
        for row in reader:
            # Add entry if student not in dictionary
            if row[0] not in student_dict:
                student_dict[row[0]] = [{row[4]: [row[5]]}]
            else:
                # Add entry if day not in dictionary for this student
                if not any(row[4] in d for d in student_dict[row[0]]):
                    student_dict[row[0]].append({row[4]: [row[5]]})
                # Add entry if student and day are both in dictionary
                else:
                    for x in student_dict[row[0]]:
                        if row[4] in x:
                            x[row[4]].append(row[5])

            # Compare classroom capacity and students per activity
        for course in course_set:
            for activity in chain(course._lectures, course._tutorials, course._labs):
                # if row[1] == activity._name:

                # Add maluspoint if number of students exceed capacity
                    if len(activity._students_list) > activity._room.capacity:
                        malus += len(activity._students_list) - activity._room.capacity
                        # malus += 1
        # Check for timeslots in each day for each student
        for student in student_dict.values():
            for day in student:
                for timeslots in day.values():
                    if len(timeslots) > 1:

                        # Add maluspoint for every conflict
                        conflicts = Counter(timeslots)
                        for x in conflicts.values():
                            malus += (x - 1)

                        # Add maluspoints for free periods
                        if '9-11' in timeslots and '11-13' not in timeslots:
                            if '13-15' in timeslots:
                                # print(student)
                                malus += 1
                            else:
                                print(student)
                                malus += 3
                        elif '15-17' in timeslots and '13-15' not in timeslots:
                            # print(student)
                            malus += 1

    return malus
