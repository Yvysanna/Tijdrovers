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


def count_points(course_set):
    malus = 0
    # mal_dict = dict()
    # mal_dict['free_period0'] = 0
    # mal_dict['free_period1'] = 0
    # mal_dict['free_period2'] = 0
    # mal_dict['lack_capacity'] = 0
    # mal_dict['conflicts'] = 0

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
                    for day in student_dict[row[0]]:
                        if row[4] in day:
                            day[row[4]].append(row[5])

        # Compare classroom capacity and students per activity
        for course in course_set:
            for activity in chain(course._lectures, course._tutorials, course._labs):
                # Add maluspoint if number of students exceed capacity
                    if len(activity._students_list) > activity._room.capacity:
                        malus += len(activity._students_list) - activity._room.capacity
                        # mal_dict['lack_capacity'] +=1

        
        points = [0,1,3] # Maluspoint values
        # Check for timeslots in each day for each student
        for student in student_dict.values():
            for day in student:
                for timeslots in day.values():
                    if len(timeslots) > 1:

                        # Add maluspoint for every conflict
                        conflicts = Counter(timeslots)
                        for x in conflicts.values():
                            if x > 1:
                                malus += (x - 1)
                                # mal_dict['conflicts'] += 1


                        # Calculate maluspoints for free periods
                        check = [int(x.split('-')[0]) for x in conflicts.keys()]
                        check.sort()
                        #print(student, conflicts, '   ------   ',  check)

                        # Check that more than one activity per day
                        if len(check) > 1:
                            l1 = check[:-1]
                            l2 = check[1:]

                            # Two times equal list but with shifted values to subtract one from the other
                            zlip = zip(l1, l2)

                            # Iterate over both lists to find difference between times
                            for l1, l2 in zlip:
                                idx = int(((l2 - l1) / 2) - 1) # Idx just because one break gives -1 and two give -3 (not 2)
                                if idx > 2:
                                    return False # If more than 2 breaks, invalid result, thus return early and stop

                                #mal_dict[f'free_period{idx}'] += 1
                                malus += points[idx]   

    # print('checker', mal_dict)
    return malus
