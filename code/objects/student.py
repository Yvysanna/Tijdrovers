from collections import Counter

class Student:
    '''
    Represents a student at the campus

    ATTRIBUTES:
    last_name : str
        The students last name
    first_name : str
        The students first name
    activities : set()
        A set of all activities in which the student participates

    METHODS:
    add_activity(activity):
        Adds activity to set of activities
    remove_activity(activity):
        Removes activity from set of activities
    maluspoints():
        Returns the number of maluspoints caused by conflicts
    '''

    def __init__(self, last_name, first_name):
        '''
        ARGUMENTS:
        last_name : str
            The student's surname
        first_name : str
            The student's first name
        '''

        self.last_name = last_name
        self.first_name = first_name
        self.activities = set()

    def add_activity(self, activity):
        '''Adds activity to set of activities'''
        self.activities.add(activity)

    def remove_activity(self, activity):
        '''Removes activity from set of activities'''
        self.activities.remove(activity)

    def maluspoints(self):
        '''Returns the number of maluspoints caused by conflicts'''
        return sum(c - 1 for c in Counter([f'{activity.get_day_time()}' for activity in self.activities]).values())

    def __str__(self) -> str:
        return str(f'\n{self.last_name}' )

    def __repr__(self) -> str:
        return str(f'\n{self.last_name}' )
