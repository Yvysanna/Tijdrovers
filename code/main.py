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

import loader
from randomize import randomize


days = ['ma', 'di', 'wo', 'do', 'vr']
timeslots = ['9-11', '11-13', '13-15', '15-17']

# load classrooms and subjects
classrooms_list = loader.load_classrooms()
subjects_list = loader.load_subjects()

# create schedule for every classroom
schedule_dict = {}
for classroom in classrooms_list:
    schedule_dict[classroom._classroom] = pd.DataFrame(columns=days, index=timeslots)

# randomize subject activities and fill in schedule
randomize(subjects_list, schedule_dict)
print(schedule_dict)
