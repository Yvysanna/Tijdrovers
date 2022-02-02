# ==================================================================================
# conflicts.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - For every course, finds the number of overlapping students with every
# - other course in order to prevent conflicting courses in the schedule
# ==================================================================================

def find_conflict_free_activities(course_set):
    """
    ARGS: course_set, set of course objects
    Checks which activities can be held parallel without students facing overlap
    RETURNS list of lists of all activities that can be held parallel, only having each activity appear once 
    PROBLEM: List is longer than possible timeslots, some lists shorter or longer than 7; 7 would mean activity found for each room at the same timeslot
    """
    result = []
    counter = 0

    # Create list of activities through looping through each course; may be updated with chain method?!
    activities = [activity for course in course_set for activity in course.lectures + course.tutorials + course.labs]
    queue = [activity for activity in activities] # just to avoid duplicates, can't be type(set) bc of indexing

    # Sort list so that Lecture activities are on top
    activities.sort(key=lambda act: act.type == 'Lecture', reverse = True)

    for activity_a in activities:
        if activity_a in queue:
            array = [activity_a]
            result.append(array)
            queue.pop(queue.index(activity_a)) # To only find unique matching pairs and not the same course connected to several courses

            for activity_b in queue:
                students_list = set([student for activity in array for student in activity.student_list])
                
                # Check for overlap in registered students
                if students_list.isdisjoint(activity_b.student_list):
                    queue.pop(queue.index(activity_b))
                    activity_b._counter = counter # just for counting total of groups
                    array.append(activity_b)

        counter += 1 # Just for checking

    # Sort list of lists with activities that can be planned parallel; list of most activities at the same time on top
    result.sort(key=lambda acts: len(acts), reverse=True)

    return result
