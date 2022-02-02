# ==================================================================================
# random.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Random algorithm to create a class schedule
# - Adds every activity to a random timeslot in a random classroom
# ==================================================================================

from itertools import chain
from random import shuffle, choice

def random_method(course_set, classrooms_list, planner, days, timeslots):
    """
    Creates a random schedule

    ARGS:
    course_set: set(Course objects)
        set containing all course objects
    classrooms_list: [Classroom objects]
        list with all classroom objects
    planner: Planner object
        planner object holding the whole schedule
    days: [str]
        list with all possible days to schedule
    timeslots: [str]
        list with all possible timeslots to schedule
    """

    # Add activities to list and randomly shuffle
    activity_list = []
    for course in course_set:
        for activity in chain(course.lectures,course.tutorials,course.labs):
            activity_list.append(activity)
    shuffle(activity_list)

    # Plan activity in schedule for a random classroom in a random timeslot on a random day if not occupied
    for activity in activity_list:
        while planner.get_info(activity) == (None, None, None):
            room = choice(classrooms_list)
            day = choice(days)
            time = choice (timeslots)
            planner.insert_activity(activity, room, day, time)
            activity.room = room
