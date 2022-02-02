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
    activities: [Activity objects]
        Array of activity objects either from planner.timeslots or read and created out of csv
    student_dict: {Student : [{Day : [Timeslot]}]}
        A dictionary containing every timeslot for every student
    constraint : bool
        True if three consecutive gaps in schedule should be considered a hard constraint, False otherwise

    RETURNS:
        False if invalid result,
        Maluspoints if valid result
    """

    malus = 0

    # Hard or soft constraint
    if constraint == True:
        terms = 2
    else:
        terms = 3

    for activity in activities:
        if activity:

            # Calculate maluspoints for room capacity and late timeslot
            malus += activity.maluspoints()

    # 0 maluspoints for 0 consecutive gaps, 1 maluspoint for 1 consecutive gap, etc.
    points = [0,1,3,1000]

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

                    # Calculate maluspoints for gaps in the schedule
                    check = [int(x.split('-')[0]) for x in conflicts.keys()]
                    check.sort()

                    # Check for more than one activity per day
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
