class Student:

    def __init__(self, last_name, first_name, student_number, courses):
        self._last_name = last_name
        self._first_name = first_name
        self._student_number = student_number
        self._courses = courses

    def __str__(self) -> str:
        return str([
            self._last_name, 
            self._first_name, 
            self._student_number, 
            self._courses
        ])

    def __repr__(self) -> str:
        return str([
            self._last_name, 
            self._first_name, 
            self._student_number, 
            self._courses
        ])