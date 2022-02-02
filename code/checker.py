# ==================================================================================
# checker.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Checks the amount of maluspoints for a schedule
# ==================================================================================

from collections import Counter

def checker(activities, student_dict, constraint):
    """
    ARGS:
        Activities: Array of activity objects either from planner.timeslots or read and created out of csv
        Student dict: format {Student : [{Day : [Timeslot]}]}
    USAGE:
        Checker function calculating maluspoints for schedule for each student
    RETURNS:
        False if invalid result,
        Malus points if valid result
    """
    malus = 0

    if constraint == True:
        terms = 2
    elif constraint == False:
        terms = 3

    for activity in activities:
        if activity:
            # Calculate maluspoints for room capacity and late timeslot
            malus += activity.maluspoints()

    points = [0,1,3,1000] # Maluspoint values
    # Check for timeslots in each day for each student
    for student in student_dict.values():
        for day in student:
            for timeslots in day.values():

                # For conflict comparison        
                if len(timeslots) > 1:

                    # Add maluspoint for every conflict
                    conflicts = Counter(timeslots)
                    for x in conflicts.values():
                        if x > 1:
                            malus += (x - 1)

                    # Calculate maluspoints for free periods
                    check = [int(x.split('-')[0]) for x in conflicts.keys()]
                    check.sort()

                    # Check that more than one activity per day
                    if len(check) > 1:
                        l1 = check[:-1]
                        l2 = check[1:]

                        # Two times equal list but with shifted values to subtract one from the other
                        zlip = zip(l1, l2)

                        # Iterate over both lists to find difference between times
                        for l1, l2 in zlip:
                            idx = int(((l2 - l1) / 2) - 1) # Idx just because one break gives -1 and two give -3 (not 2)
                            if idx > 2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  :
                                return False # If more than 2 breaks, invalid result, thus return early and stop

                            malus += points[idx]

    # print('checker', mal_dict)
    return malus
