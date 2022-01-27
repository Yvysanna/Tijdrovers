from conflicts import find_conflict_free_activities
import random


def semirandom(course_set, classrooms_list, planner, days, timeslots):
    # TEMPORARY FIX FOR SCHEDULING EVERY LEFTOVER ACTIVITY RANDOMLY
    not_scheduled = set()
    result = find_conflict_free_activities(course_set)
    for activities in result:
        for activity in activities:

            # Give planner all classrooms from the smallest possible to the biggest available
            planner.plan_activity(classrooms_list[classrooms_list.index(activity._room):], activity)

            # Check if activity can be scheduled
            room, day, time = planner.get_info(activity)

    #---- SEMI RANDOM METHOD FIX FROM HERE ----- #
            if not room:
                not_scheduled.add(activity)

    #print("NOT SCHEDULED", len(not_scheduled))
    for activity in not_scheduled:

        # Loop until activity could be planned for each activity
        while planner.get_info(activity) == (None, None, None):
            room = random.choice(classrooms_list)
            day = random.choice(days)
            time = random.choice (timeslots)
            #print(room, day, time)

            # Just try to insert activity with random data there and see if it works
            planner.insert_activity(activity, room, day, time)
        #print(activity, "planning succeeded")
        room, day, time = planner.get_info(activity) # Final checkup
        activity._room = room # Connect room when broken out of while loop
        activity._timeslot = (day, time)

        if planner.get_info(activity) == (None, None, None):
            print("NOT FIXED")
    # ----- SEMI RANDOM METHOD END ----- #
