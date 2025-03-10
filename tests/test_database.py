import allure

from src.database import DataBase
from src.assertions.assertion import Assertion


@allure.feature("Basic Database actions")
class TestDataBase:
    """Test-class for basic actions with database.
    """
    assertion = Assertion()

    @allure.title("Connection")
    def test_db_connection(self, database: DataBase):
        """Tests connection with database.
        """
        connection = None
        try:
            connection = database.engine.connect()
            self.assertion.database.assert_connection(database, connection)
        finally:
            if connection:
                connection.close()
