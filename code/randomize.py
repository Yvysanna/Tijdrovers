days = ['ma', 'di', 'wo', 'do', 'vr']
timeslots = ['9-11', '11-13', '13-15', '15-17']


def randomize(course_list, schedule_dict):
    """
    ARGS: list of objects, (dict{str:pd.dataframe})
    calls class method to schedule courses
    RETURNS list of course objects
    """

    # for every activity of every course, add activity to list
    for course in course_list:
        course.schedule()

    return course_list

