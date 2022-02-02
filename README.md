# Lectures & Lesroosters

This project aims to optimally create a class schedule for the Science Park Campus at UvA. This project has been made in the scope of the course 'Programmeertheorie / Heuristiek' from the Minor Programming at the University of Amsterdam.

## Problem summary

All the data used in this project is found in the `data` directory. This problem in this project involves a list of
609 students that each follows up to 5 courses found in `students.csv`, and a list of classrooms, each with a maximum capacity found in `classrooms.csv`.<br>
There are 29 courses, each of which has a certain amount of lectures, tutorials and lab lessons per week. Each tutorial
and lab session has a maximum number of students that can participate in it, meaning there will be multiple groups
for each of these activities. All students are assigned to every lecture, so no groups are made for lectures.
Each classroom is suitable for any of the three types of activities. The number of activities and maximum amount of students is found in `courses.csv`.<br>

Each classroom has either 4 or 5 timeslots, at 9-11, 11-13, 13-15, 15-17, and only the largest classroom having a timeslot
at 17-19. Given this data it is our goal to create the most optimal class schedule by giving each activity their own
timeslot in a classroom, where we are free to assign students to any activity group.
How optimal the schedule is, is measured my maluspoints. Maluspoints are given for each of the following:<br>

- 1 point for each student that exceeds the capacity limit for a classroom
- 1 point for each time a student has two activities planned in the same timeslot
- 1 point for every time a student has a gap in their schedule
- 3 points for every time a student has two consecutive gaps in their schedule
- 5 points for every use of the timeslot at 17-19

With these soft constraints also come a few hard constraints:<br>

- Each student must have every activity that they signed up for in the schedule
- No activities can be given in the same classroom in the same timeslot
- No student may have three consecutive gaps in their schedule

## Solution summary

For this problem we have experimented with hill climbers, simulated annealing and a combination of the two algorithms. All of these algorithms alternate between two functions that randomly switch activities between time slots and randomly switch students between activity groups.

For the begin position, we create a begin position with either random_method or semirandom. Random_method creates a completely random schedule, while semirandomtries to create a schedule with the least amount of conflicts.

The hill climber keeps track of how many non-improvements are made after each state change. The algorithm keeps changing the state randomly with the aforementioned switch functions and only keeps the state if an improvement is made. After the maximum number of non-improvements or 'streak' has been reached, the algorithm stops and a schedule is created from the last state. The schedule will be saved as a csv in the code/results folder.

Simulated annealing keeps changing the state randomly and decides based on a calculated chance if a state with a worse score will be accepted. States with a better score will always be accepted. The algorithm will stop after a determined number of iterations.

The climber_annealing is a combination of the aforementioned algorithms. This algorithm starts like a hill climber until a certain number of points is reached. After that the algorithm changes into a simulated annealing until the iteration limit has been reached. Finally, the algorithm runs like a climber again until the streak limit has been reached.

## Run Locally

Clone the project

```bash
  git clone https://github.com/Yvysanna/Tijdrovers
```

Install dependencies<br>
*This code is written in Python 3.8.10 and 3.10.1. To run this code, the required packages are noted down in requirements.txt and can be installed easily via pip with this command:*

```bash
  pip3 install -r requirements.txt
```

Run the program

```bash
  python3 main.py [-s STREAK_LIMIT] [-p POINT_LIMIT] [-i ITERATION_LIMIT] [-t TEMPERATURE_MULTIPLIER] [-c CONSTRAINT] [-d DISTRIBUTION] [-g GRAPH] [-n RUNS] [-a ALGORITHM]
```

* The streak limit is an integer that determines for the hill climber after how many non-improvements the program should stop.
* The point limit is an integer that determines for the climber-annealing program after how many iterations it should switch from climbing to annealing
* The iteration limit is an integer that determines for the annealing program after how many interations the program should stop
* The temperature multiplier is a float that determines the effect of the current temperature on the chance to accept a state
* The constraint is a boolean value that determines whether a hard or a soft constraint will be used for the third break term
* The distribution is a boolean value that determines whether or not a histogram should be plotted of the points across N runs
* The graph is a boolean value that determines whether or not a line graph should be made of the maluspoints plotted against the iterations for one run
* The number of runs is an integer that determines how often the main program should run
* The algorithm is a string that determines whether the hill climber ('climber'), simulated annealing ('annealing'), or a combination ('annealing_climber') should run.

## Acknowledgements

* StackOverflow
* Minor Programmeren, Programming Lab, Faculty of Science, University of Amsterdam

## Authors

* [Karel Nijhuis](https://github.com/5inu)
* [Yvette Schröder](https://github.com/Yvysanna)
* [Julia Liem](https://github.com/julialfk)
