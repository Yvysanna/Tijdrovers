# ==================================================================================
# checker.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Checks the amount of maluspoints for a schedule
# ==================================================================================

from itertools import chain
from collections import Counter

def checker(course_set, student_dict):
    """
    ARGS:
        Course set: set of course objects,
        Student dict: format {Student : [{Day : [Timeslot]}]}
    USAGE:
        Checker function calculating maluspoints for schedule for each student
    RETURNS:
        False if invalid result,
        Malus points if valid result
    """
    malus = 0

    # Compare classroom capacity and students per activity
    for course in course_set:
        for activity in chain(course._lectures, course._tutorials, course._labs):
            # Add maluspoint if number of students exceed capacity
                if len(activity._students_list) > activity._room.capacity:
                    malus += len(activity._students_list) - activity._room.capacity
                    # mal_dict['lack_capacity'] +=1


    points = [0,1,3,100] # Maluspoint values
    # Check for timeslots in each day for each student
    for student in student_dict.values():
        for day in student:
            for timeslots in day.values():
                
                # Min points for late timeslot
                for t in timeslots:
                    if t == '17-19':
                        malus += 5

                # For conflict comparison        
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
                            if idx > 3:
                                return False # If more than 2 breaks, invalid result, thus return early and stop

                            #mal_dict[f'free_period{idx}'] += 1
                            malus += points[idx]

    # print('checker', mal_dict)
    return malus
