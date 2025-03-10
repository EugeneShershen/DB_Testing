from src.assertions.assertions_database import AssertionsDataBase
from src.assertions.assetions_course_table import AssertionsCourseTable
from src.assertions.assetions_student_table import AssertionsStudentTable


class Assertion:
    def __init__(self):
        self.database = AssertionsDataBase()
        self.course = AssertionsCourseTable()
        self.student = AssertionsStudentTable()
