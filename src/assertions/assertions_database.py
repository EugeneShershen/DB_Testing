import allure
from assertpy import assert_that

from src.database import DataBase


class AssertionsDataBase:

    @allure.step("Assert that connection was created")
    def assert_connection(self, database: DataBase, connection):
        database.logger.info("Asserting that connection was created")
        assert_that(connection).is_not_equal_to(None)
