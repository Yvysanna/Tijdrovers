days = ['ma', 'di', 'wo', 'do', 'vr']
timeslots = ['9-11', '11-13', '13-15', '15-17']


def randomize(subjects_list, schedule_dict):
    """
    ARGS: list of objects, (dict{str:pd.dataframe})
    calls class method to schedule subjects
    RETURNS list of subject objects
    """

    # for every activity of every subject, add activity to list
    for subject in subjects_list:
        subject.schedule()

    return subjects_list

