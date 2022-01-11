# ==================================================================================
# main.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Usage: python3 main.py
#
# - Creates schedule
# ==================================================================================

import pandas as pd
import random

from randomize import randomize


days = ['ma', 'di', 'wo', 'do', 'vr']
timeslots = ['9-11', '11-13', '13-15', '15-17']


classrooms_df = pd.DataFrame(pd.read_csv('data/classrooms.csv', sep=';'))
subjects_df = pd.DataFrame(pd.read_csv('data/subjects.csv', sep=';'))
schedule_dict = {}
for classroom in classrooms_df['Zaalnummber']:
    schedule_dict[classroom] = pd.DataFrame(columns=days, index=timeslots)

schedule_output = randomize(subjects_df, schedule_dict)
print(schedule_output)

#print(classrooms_df, "\n", subjects_df, "\n", schedule_dict)



#schedule_df.at['ma', '9-11'] = "Advanced Heuristics"

#print(schedule_df)
