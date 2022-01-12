class Classroom:

    def __init__(self, classroom, capacity):
        self._classroom = classroom
        self._capacity = int(capacity)
        self._possible_subjects = []

    def __str__(self) -> str:
        return str([
            self._classroom, 
            self._capacity, 
            self._possible_subjects
        ])

    def __repr__(self) -> str:
        return str([
            self._classroom, 
            self._capacity, 
            self._possible_subjects
        ])