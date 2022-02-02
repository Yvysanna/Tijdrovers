# ==================================================================================
# semirandom.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Semirandom algorithm to create a class schedule
# - Finds every activity that does not form a conflict for any students
# - Plans the conflict free activities into the smallest available classroom
# - Plans every other activity randomly
# ==================================================================================

import random


def semirandom(course_set, classrooms_list, planner, days, timeslots):
    """
    Creates a schedule after certain constrains
    random schedules everything that cannot be planned under constrains
    ARGS:
        course_set: set containing all course objects
        classrooms_list: list with all classroom objects 
        planner: planner object holding the whole schedule
        days: list with all possible days to schedule
        timeslots: list with all possible timeslots to schedule
    RETURNS:
        None
    """
    
    # Find every pair of activities that can be taught in the same timeslot
    not_scheduled = set()
    result = find_conflict_free_activities(course_set)

    for activities in result:
        for activity in activities:
            # Give planner all classrooms from the smallest possible to the biggest available
            planner.plan_activity(
                classrooms_list[classrooms_list.index(activity.room):], activity)

            # Check if activity can be scheduled
            room, day, time = planner.get_info(activity)

            # Add all non scheduled activities to a list for random procedure
            if not room:
                not_scheduled.add(activity)

    # Randomly schedule all remaining activities
    for activity in not_scheduled:

        # Loop until activity could be planned for each activity
        while planner.get_info(activity) == (None, None, None):
            room = random.choice(classrooms_list)
            day = random.choice(days)
            time = random.choice(timeslots)
            planner.insert_activity(activity, room, day, time)

        # If succesful, add room and timeslot
        room, day, time = planner.get_info(activity)
        activity.set_day_time(day, time)


def find_conflict_free_activities(course_set):
    """
    Checks which activities can be held parallel without students facing overlap

    ARGS:
        course_set : set(Course objects) 
        All the courses which contain activities
    RETURNS:
        List of lists of all activities that can be held parallel to eachother, only having each activity appear once
    """

    conflict_free = []

    # Create list of activities through looping through each course
    activities = [activity for course in course_set for activity in course.lectures +
                  course.tutorials + course.labs]
    # Avoid duplicates
    queue = [activity for activity in activities]

    # Sort list so that lecture activities are on top
    activities.sort(key=lambda act: act.type == 'Hoorcollege', reverse=True)

    for activity_a in activities:
        if activity_a in queue:
            activity_group = [activity_a]
            conflict_free.append(activity_group)

            # Only find unique matching pairs
            queue.pop(queue.index(activity_a))

            for activity_b in queue:
                students_list = set([student for activity in activity_group for student in activity.student_list])

                # Check for overlap in registered students
                if students_list.isdisjoint(activity_b.student_list):
                    queue.pop(queue.index(activity_b))
                    activity_group.append(activity_b)

    # Sort list of lists with activities that can be planned parallel; list of most activities at the same time on top
    conflict_free.sort(key=lambda acts: len(acts), reverse=True)
    return conflict_free
