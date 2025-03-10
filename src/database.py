import logging
import psycopg2
import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import allure

from src.db_tables import Base

from src.course_table import CourseTable
from src.student_table import StudentTable


class DataBase:
    """Base class for database.
    """

    def __init__(self, env='local'):
        try:
            self.logger = logging.getLogger(self.__class__.__name__)

            config = configparser.ConfigParser()
            config_path = Path(__file__).resolve().parent.parent / "settings.ini"
            config.read(config_path)
            if env in config:
                db_url = config[env]["DATABASE_URL"]
            else:
                raise ValueError(f"Environment '{env}' is not supported")

            self.logger.info('Connecting to the database')
            self.engine = create_engine(db_url)

            self.logger.info('Creating session with database')
            Session = sessionmaker(bind=self.engine, autoflush=False)
            self.session = Session()

            config = {section: dict(config[section]) for section in config.sections()}
            config["logger"] = self.logger
            config["engine"] = self.engine
            config["session"] = self.session

            self.course = CourseTable(config)
            self.student = StudentTable(config)

        except (Exception, psycopg2.Error) as error:
            self.logger.error(str(error))

    @allure.step("Create tables")
    def create_tables(self):
        """Creates tables into the database.
        """
        try:
            self.logger.info('Creating tables for database')
            Base.metadata.create_all(self.engine)

        except (Exception, psycopg2.Error) as error:
            self.logger.error(str(error))
