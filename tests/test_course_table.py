import allure
from pytest import mark

from src.database import DataBase
from data.tests_data_cud import courses_cud
from data.tests_data_search import courses_search
from src.assertions.assertion import Assertion


@allure.feature("Table 'Course'")
class TestCourseTable:
    """Test-class for 'Course' table of the database.
    """
    assertion = Assertion()

    @allure.title('Add')
    @mark.parametrize('course', [
        courses_cud[1],
        courses_cud[2],
        courses_cud[3]
    ])
    def test_add_course(self, database: DataBase, course):
        """Tests adding a course.
        """
        name = course['old_name']

        database.course.add_course(name=name)
        received_name = database.course.get_course_name_by_name(name)

        self.assertion.course.assert_add(database, received_name, name)

    @allure.title('Update')
    @mark.parametrize('course', [
        courses_cud[1],
        courses_cud[2],
        courses_cud[3]
    ])
    def test_update_course(self, database: DataBase, course):
        """Tests updating a course.
        """
        old_name = course['old_name']
        new_name = course['new_name']

        database.course.update_course(course_name=old_name, updated_name=new_name)
        received_name = database.course.get_course_name_by_name(new_name)

        self.assertion.course.assert_update(database, received_name, new_name)

    @allure.title('Delete')
    @mark.parametrize('course', [
        courses_cud[1],
        courses_cud[2],
        courses_cud[3]
    ])
    def test_delete_course(self, database: DataBase, course):
        """Tests deleting a course.
        """
        name = course['new_name']

        database.course.delete_course(course_name=name)

        self.assertion.course.assert_delete(database, name)

    @allure.title('Get courses by student id')
    @mark.parametrize('course', [
        courses_search[1],
        courses_search[2],
        courses_search[3]
    ])
    def test_course_list_of_certain_student(self, database: DataBase, course):
        """Tests getting a list of courses by student id.
        """
        student_id = course['student_id']
        course_info = course['course_info']

        result = database.course.course_list_of_certain_student(student_id=student_id)

        self.assertion.course.assert_get_courses_by_student_id(database, result, course_info)
