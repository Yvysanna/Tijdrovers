import datetime
import pandas as pd

def store(students_set, planner, min_points):
    """
    Function to write everything after correct format in csv file
    RETURNS: None
    """

    df_dict = {'student': [],'vak': [],'activiteit': [],'zaal': [],'dag': [],'tijdslot': []}
    for student in students_set:
        for course in student.courses:
            all_activities = course._lectures + course._tutorials + course._labs
            activities = [activity for activity in all_activities if activity.confirm_registration(student)]
            for activity in activities:
                room, day, time = planner.get_info(activity)
                df_dict['student'].append(student._last_name + ' ' + student._first_name)
                df_dict['vak'].append(activity._name)
                df_dict['activiteit'].append(activity._type)
                df_dict['zaal'].append(room.name)
                df_dict['dag'].append(day or 'tba')
                df_dict['tijdslot'].append(time or 'tba')


    results_df = pd.DataFrame.from_dict(df_dict, orient='columns', dtype=None, columns=None)
    # with open(f'data/climber{min_points}.csv', 'w+'):
    #     pass
    # results_df.to_csv(f'data/climber{min_points}.csv', sep = ';', index=False)
    results_df.to_csv(f'data/results/climber{min_points}_{datetime.now().strftime("%Y%m%d%H%M")}.csv', mode = 'w+', sep = ';', index=False)
