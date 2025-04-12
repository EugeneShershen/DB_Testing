import allure
from pytest import mark

from src.database import DataBase
from src.assertions.assertion import Assertion


@allure.feature("Table 'Course'")
class TestCourseTable:
    """Test-class for 'Course' table of the database.
    """
    assertion = Assertion()

    @allure.title('Add')
    @mark.parametrize('prepare_test_data_cud', [
        (1, "course"),
        (2, "course"),
        (3, "course")
    ], indirect=True)
    def test_add_course(self, database: DataBase, prepare_test_data_cud):
        """Tests adding a course.
        """
        name = prepare_test_data_cud['old_name']

        database.course.add_course(name=name)
        received_name = database.course.get_course_name_by_name(name)

        self.assertion.course.assert_add(database, received_name, name)

    @allure.title('Update')
    @mark.parametrize('prepare_test_data_cud', [
        (1, "course"),
        (2, "course"),
        (3, "course")
    ], indirect=True)
    def test_update_course(self, database: DataBase, prepare_test_data_cud):
        """Tests updating a course.
        """
        old_name = prepare_test_data_cud['old_name']
        new_name = prepare_test_data_cud['new_name']

        database.course.update_course(course_name=old_name, updated_name=new_name)
        received_name = database.course.get_course_name_by_name(new_name)

        self.assertion.course.assert_update(database, received_name, new_name)

    @allure.title('Delete')
    @mark.parametrize('prepare_test_data_cud', [
        (1, "course"),
        (2, "course"),
        (3, "course")
    ], indirect=True)
    def test_delete_course(self, database: DataBase, prepare_test_data_cud):
        """Tests deleting a course.
        """
        name = prepare_test_data_cud['new_name']

        database.course.delete_course(course_name=name)

        self.assertion.course.assert_delete(database, name)

    @allure.title('Get courses by student id')
    @mark.parametrize('prepare_test_data_search', [
        (1, "course"),
        (2, "course"),
        (3, "course")
    ], indirect=True)
    def test_course_list_of_certain_student(self, database: DataBase, prepare_test_data_search):
        """Tests getting a list of courses by student id.
        """
        student_id = prepare_test_data_search['student_id']
        course_info = prepare_test_data_search['course_info']

        result = database.course.course_list_of_certain_student(student_id=student_id)

        self.assertion.course.assert_get_courses_by_student_id(database, result, course_info)
