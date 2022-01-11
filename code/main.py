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


classrooms_df = pd.DataFrame(pd.read_csv('data/classrooms.csv', sep=';'))
subjects_df = pd.DataFrame(pd.read_csv('data/subjects.csv', sep=';'))
schedule_df = pd.DataFrame(columns=['9-11', '11-13', '13-15', '15-17', '17-19'], index=['ma', 'di', 'wo', 'do', 'vr'])
print(classrooms_df, "\n", subjects_df, "\n", schedule_df)
