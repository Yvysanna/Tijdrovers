# ==================================================================================
# distribution.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Creates a histogram of total number of maluspoints across N runs
# ==================================================================================

import matplotlib.pyplot as plt
from datetime import datetime
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


def distribution(points, n_runs):
    """
    ARGS:
        points: list of maluspoints on each iteration
        n_runs: number of times main() has been run
    USAGE:
        Creates a histogram of total number of maluspoints across N runs
    RETURNS:
        None
    """

    plt.hist(points, range=(60, 150), color='midnightblue', edgecolor='mediumblue', density=True, bins=1)
    plt.xlim(60, 150)
    plt.title(f"Probability distribution of maluspoints across {n_runs} runs")
    plt.xlabel("Maluspoints")
    plt.ylabel("Probability")
    plt.tight_layout()
    plt.savefig('data/distribution.png', dpi=1000)


def plot(plotx, ploty, streak):
    """
    ARGS:
        plotx: list of iteration numbers
        ploty: list of scores of every iteration
    USAGE:
        Creates a line graph from the amount of points over the iterations within the algorithm
    RETURNS:
        None
    """

    plt.plot(plotx, ploty)
    plt.ylim(0)
    plt.xlabel("Iterations")
    plt.ylabel("Maluspoints")
    plt.title(f"Points during hill climber which stops after {streak} non-improvements")
    plt.grid()
    plt.savefig(f'code/algorithms/plots/climber{streak}.png', dpi=1000)



