import allure
from assertpy import assert_that
from pytest import raises

from src.database import DataBase


class AssertionsCourseTable:

    @allure.step("Assert that course was added")
    def assert_add(self, database: DataBase, received_name, name):
        database.logger.info("Asserting that course was added")
        assert_that(received_name).is_equal_to(name)

    @allure.step("Assert that course was updated")
    def assert_update(self, database: DataBase, received_name, new_name):
        database.logger.info("Asserting that course was updated")
        assert_that(received_name).is_equal_to(new_name)

    @allure.step("Assert that course was deleted")
    def assert_delete(self, database: DataBase, name):
        database.logger.info("Asserting that course was deleted")
        with raises(TypeError):
            database.course.get_course_name_by_name(name)

    @allure.step("Assert that courses was gotten by student id")
    def assert_get_courses_by_student_id(self, database: DataBase, result, course_info):
        database.logger.info("Asserting that courses was gotten by student id")
        assert_that(result).is_equal_to(course_info)
