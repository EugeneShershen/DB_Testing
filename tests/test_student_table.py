import allure
from pytest import mark

from src.database import DataBase
from src.assertions.assertion import Assertion


@allure.feature("Table 'Student'")
class TestCourseTable:
    """Test-class for 'Student' table of the database.
    """
    assertion = Assertion()

    @allure.title("Add")
    @mark.parametrize('prepare_test_data_cud', [
        (1, "student"),
        (2, "student"),
        (3, "student")
    ], indirect=True)
    def test_add_student(self, database: DataBase, prepare_test_data_cud):
        """Tests adding a student.
        """
        name = prepare_test_data_cud['old_name']
        age = prepare_test_data_cud['old_age']
        courses = prepare_test_data_cud['courses']

        database.student.add_student(name=name, age=age, courses=courses)
        student_id = database.student.get_student_id_by_name_age(name, age)
        received_name = database.student.get_student_name_by_id(student_id)

        self.assertion.student.assert_add(database, received_name, name)

    @allure.title("Update")
    @mark.parametrize('prepare_test_data_cud', [
        (1, "student"),
        (2, "student"),
        (3, "student")
    ], indirect=True)
    def test_update_student(self, database: DataBase, prepare_test_data_cud):
        """Tests updating a student.
        """
        old_name = prepare_test_data_cud['old_name']
        new_name = prepare_test_data_cud['new_name']
        old_age = prepare_test_data_cud['old_age']
        new_age = prepare_test_data_cud['new_age']

        student_id = database.student.get_student_id_by_name_age(old_name, old_age)
        database.student.update_student(student_id=student_id, updated_name=new_name, updated_age=new_age)
        received_name = database.student.get_student_name_by_id(student_id)

        self.assertion.student.assert_update(database, received_name, new_name)

    @allure.title("Delete")
    @mark.parametrize('prepare_test_data_cud', [
        (1, "student"),
        (2, "student"),
        (3, "student")
    ], indirect=True)
    def test_delete_student(self, database: DataBase, prepare_test_data_cud):
        """Tests deleting a student.
        """
        new_name = prepare_test_data_cud['new_name']
        new_age = prepare_test_data_cud['new_age']

        student_id = database.student.get_student_id_by_name_age(new_name, new_age)
        database.student.delete_student(student_id=student_id)

        self.assertion.student.assert_delete(database, student_id)

    @allure.title("Get students by course name")
    @mark.parametrize('prepare_test_data_search', [
        (1, "student"),
        (2, "student"),
        (3, "student")
    ], indirect=True)
    def test_student_list_of_certain_course(self, database: DataBase, prepare_test_data_search):
        """Tests for getting a list of students by the course`s name.
        """
        course_name = prepare_test_data_search['course_name']
        student_info = prepare_test_data_search['student_info']

        result = database.student.student_list_of_certain_course(course_name=course_name)

        self.assertion.student.assert_get_students_by_course_name(database, result, student_info)
