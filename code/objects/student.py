class Student:
    '''
    Represents a student at the campus

    ATTRIBUTES:
    _last_name : str
        The student's surname
    _first_name : str
        The student's first name
    _student_number : str
        The student number
    courses : list[str]
        A list of all the courses in which the student has enrolled

    METHODS:
    __str__()
        Represents the class as a string
    '''

    def __init__(self, last_name, first_name, student_number, courses):
        '''
        ARGUMENTS:
        _last_name : str
            The student's surname
        _first_name : str
            The student's first name
        _student_number : str
            The student number
        courses : list[str]
            A list of all the courses in which the student has enrolled
        '''

        self._last_name = last_name
        self._first_name = first_name
        self._student_number = student_number
        self.courses = courses

    def __str__(self) -> str:
        '''Represents the class as a string'''
        return str([
            self._last_name,
            self._first_name,
            self._student_number,
            self._courses
        ])

    def __repr__(self) -> str:
        '''Represents the class as a string'''
        return str([
            self._last_name,
            self._first_name,
            self._student_number,
            self._courses
        ])