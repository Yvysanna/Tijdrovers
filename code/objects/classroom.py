class Classroom:
    '''
    The classroom objects represents one of the campus' classrooms
    where a course may be taught at any time of the week

    ATTRIBUTES:
    name : str
        The name of the classroom
    capacity : int
        The number of students that can be scheduled in the classroom

    METHODS:
    get_capacity():
        Returns the capacity of the classroom
    '''

    def __init__(self, name, capacity):
        '''
        ARGUMENTS:
        name : str
            The name of the classroom
        capacity : int
            The number of students that can be scheduled in the classroom
        '''

        self.name = name
        self.capacity = int(capacity)

    def get_capacity(self):
        '''Returns the capacity of the classroom'''
        return self.capacity

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return str(self.name)
