import allure
from assertpy import assert_that
from pytest import raises

from src.database import DataBase


class AssertionsStudentTable:

    @allure.step("Assert that student was added")
    def assert_add(self, database: DataBase, received_name, name):
        database.logger.info("Asserting that student was added")
        assert_that(received_name).is_equal_to(name)

    @allure.step("Assert that student was updated")
    def assert_update(self, database: DataBase, received_name, new_name):
        database.logger.info("Asserting that student was updated")
        assert_that(received_name).is_equal_to(new_name)

    @allure.step("Assert that student was deleted")
    def assert_delete(self, database: DataBase, student_id):
        database.logger.info("Asserting that student was deleted")
        with raises(TypeError):
            database.student.get_student_name_by_id(student_id)

    @allure.step("Assert that students was gotten by course name")
    def assert_get_students_by_course_name(self, database: DataBase, result, student_info):
        database.logger.info("Asserting that students was gotten by course name")
        assert_that(result).is_equal_to(student_info)
