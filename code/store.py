from datetime import datetime
from itertools import chain
import pandas as pd

def store(students_set, planner, points):
    """
    ARGS:
        students_set: Set of all student objects
        planner: Planner object
        points: Int total malus points
    USAGE:
        Writes results after correct format into csv file
    RETURNS:
        None
    """

    df_dict = {'student': [],'vak': [],'activiteit': [],'zaal': [],'dag': [],'tijdslot': []}
    for student in students_set:
        for activity in student.activities:
            room, day, time = planner.get_info(activity)
            df_dict['student'].append(f'{student._last_name} {student._first_name}')
            df_dict['vak'].append(activity.name)
            df_dict['activiteit'].append(activity.type)
            df_dict['zaal'].append(room.name)
            df_dict['dag'].append(day or 'tba')
            df_dict['tijdslot'].append(time or 'tba')

    # Create dataframe and write into csv
    results_df = pd.DataFrame.from_dict(df_dict, orient='columns', dtype=None, columns=None)
    results_df.to_csv(f'code/results/schedule{points}_{datetime.now().strftime("%Y%m%d%H%M")}.csv', mode = 'w+', sep = ';', index=False)
