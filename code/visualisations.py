# ==================================================================================
# distribution.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Visualizes results from running mainprogram
# - Creates a csv file containing the schedule of every student
# - Creates a histogram of total number of maluspoints across N runs
# - Creates a line graph showing the maluspoints with every iteration for 1 run
# ==================================================================================

import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd


def store(students_set, planner, points):
    """
    Writes schedule for every student into csv file

    ARGS:
    students_set : set(Student object)
        A set of every student
    planner : Planner object
        Contains the schedule of every student
    points : int
        The total number of maluspoints

    RETURNS:
    None
    """

    df_dict = {'student': [], 'vak': [], 'activiteit': [],
               'zaal': [], 'dag': [], 'tijdslot': []}
    for student in students_set:
        for activity in student.activities:
            room, day, time = planner.get_info(activity)
            df_dict['student'].append(
                f'{student.last_name} {student.first_name}')
            df_dict['vak'].append(activity.name)
            df_dict['activiteit'].append(activity.type)
            df_dict['zaal'].append(room.name)
            df_dict['dag'].append(day or 'tba')
            df_dict['tijdslot'].append(time or 'tba')

    # Create dataframe and write into csv
    results_df = pd.DataFrame.from_dict(
        df_dict, orient='columns', dtype=None, columns=None)
    results_df.to_csv(
        f'code/results/schedule{points}_{datetime.now().strftime("%Y%m%d%H%M")}.csv', mode='w+', sep=';', index=False)


def distribution(points, n):
    """
    Creates a histogram of total number of maluspoints across N runs

    ARGS:
    points : [int]
        List of maluspoints on each iteration
    n : int
        Number of iterations

    RETURNS:
    None
    """

    minimum = min(points) // 10 * 10 - 50
    maximum = max(points) // 10 * 10 + 50
    plt.hist(points, range=(minimum, maximum), color='midnightblue', edgecolor='mediumblue', density=True, bins=(maximum - minimum) // 10 + 1)
    plt.xlim(minimum, maximum)
    plt.title(f"Probability distribution of maluspoints across {n} runs")
    plt.xlabel("Maluspoints")
    plt.ylabel("Probability")
    plt.tight_layout()
    plt.savefig('code/algorithms/plots/distribution.png', dpi=1000)


def plot(plotx, ploty, streak):
    """
    Creates a line graph from the amount of points over the iterations within the algorithm

    ARGS:
    plotx : [int]
        List of iteration numbers
    ploty : [int]
        List of points on every iteration

    RETURNS:
    None
    """

    plt.plot(plotx, ploty)
    plt.ylim(0)
    plt.xlabel("Iterations")
    plt.ylabel("Maluspoints")
    plt.title(f"Points during hill climber after {len(ploty)} iterations")
    plt.grid()
    plt.savefig(f'code/algorithms/plots/climber{streak}.png', dpi=1000)
