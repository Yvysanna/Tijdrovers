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
    Checker function calculating maluspoints for schedule for each student

    ARGS:
        Activities: Iterable
            Array of activity objects either from planner.timeslots or read and created out of csv
        Student dict: Dictionary
            format {Student : [{Day : [Timeslot]}]}
        Constraint: Bool
            Defines, whether too many breaks cause False result or result with more malus points
    RETURNS:
        False if invalid result,
        Malus points if valid result
    """
    malus = 0

    # Hard or soft constraint
    if constraint == True:
        terms = 2
    elif constraint == False:
        terms = 3

    for activity in activities:
        if activity:

            # Calculate maluspoints for room capacity and late timeslot
            malus += activity.maluspoints()

     # Maluspoint values
    points = [0,1,3,1000]

    # Iterate over student's individual schedule
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

                    # Check if several activities planned for one day
                    if len(check) > 1:
                        l1 = check[:-1]
                        l2 = check[1:]

                        # Two times equal list but with shifted values to subtract one from the other
                        zlip = zip(l1, l2)

                        # Iterate over both lists to find difference between times
                        for l1, l2 in zlip:
                            idx = int(((l2 - l1) / 2) - 1) 
                            
                            # Depending on hard or soft constraint, return early
                            if idx > terms:
                                return False 

                            malus += points[idx]

    return malus