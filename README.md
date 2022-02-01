# Lectures & Lesroosters

This project aims to optimally create a class schedule for the Science Park Campus at UvA. This project has been made in the scope of the course 'Programmeertheorie / Heuristiek' from the Minor Programming at the University of Amsterdam.

## Summary

To create the schedule, we used a pandas Dataframe object.

## Run Locally

Clone the project

```bash
  git clone https://github.com/Yvysanna/Tijdrovers
```

Install dependencies
*This code is written in Python 3.8.10 and 3.10.1. To run this code, the required packages are noted down in requirements.txt and can be installed easily via pip with this command:*

```bash
  pip install -r requirements.txt
```

Run the program

```bash
  python3 code/main.py
```

#### Instructions for experiments
Run the program multiple times for testing:
* Determine the time you want to run the program in line 28 of distribution.py by changing `start < {time}`
* Change the file name in line 51 to save distribution histogram
* The main algorithm used can be changed in main.py in line 56. Usable algorithm functions can be found in algorithms/hill_climber.py.
* Algorithm for determining starting position for the main algorithm can be changed to random_method or semirandom in line 50 of main.py
* In line 62 of checker.py, `idx > 2` can be used for a hard constraint for the third break period, or `idx > 3` can be used to calculate 1000 points for the third break period.
* Parameters 'streak' for climbers and 'range', formulas for 'T' and 'chance' for annealing can be changed in algorithms/hill_climber.py
* After making adjustments, run the program multiple times for a determined amount of time with `python3 code/distribution.py`

## Acknowledgements

* StackOverflow
* Minor Programmeren, Programming Lab, Faculty of Science, University of Amsterdam

## Authors

* [Karel Nijhuis](https://github.com/5inu)
* [Yvette Schröder](https://github.com/Yvysanna)
* [Julia Liem](https://github.com/julialfk)
