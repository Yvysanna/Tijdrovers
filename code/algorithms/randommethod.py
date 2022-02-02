import random

def random_method(course_set, classrooms_list, planner, days, timeslots):
    """
    Completely random method / method to begin from
    Adds every activity to a random timeslot in a random room
    RETURNS: None
    """
    all_activities_global = []
    for course in course_set:
        all_activities = course._lectures + course._tutorials + course._labs

        for activity in all_activities:
            all_activities_global.append(activity)

    random.shuffle(all_activities_global)


    for activity in all_activities_global:
        while planner.get_info(activity) == (None, None, None):
            room = random.choice(classrooms_list)
            day = random.choice(days)
            time = random.choice (timeslots)
            planner.insert_activity(activity, room, day, time)
            activity.room = room
