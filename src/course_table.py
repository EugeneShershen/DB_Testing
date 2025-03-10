import allure
import psycopg2

from src.db_tables import Course, Student, RegistrationList
from src.base_db import BaseDB


class CourseTable(BaseDB):
    """Class for interacting with the 'Course' table of the database.
    """

    @allure.step("Get course name by name")
    def get_course_name_by_name(self, course_name):
        """Returns a course name by its name.
        """
        self.logger.info('Getting course name by its name')
        received_name = self.session.query(Course.name).filter_by(name=course_name).first()[0]

        return received_name

    @allure.step("Add course")
    def add_course(self, name: str):
        """ Adds a new object "Course" to the database.
        """
        try:
            self.logger.info(f"Adding course '{name}'")
            new_course = Course(name=name)
            self.session.add(new_course)
            self.session.commit()

        except (Exception, psycopg2.Error) as error:
            self.logger.error(str(error))

    @allure.step("Update course")
    def update_course(self, course_name: str, updated_name: str):
        """ Updates an information about a certain object "Course".
        """
        try:
            self.logger.info(f"Updating course '{course_name}'")
            course_obj = self.session.query(Course).filter_by(name=course_name).first()

            if course_obj:
                course_obj.name = updated_name
                self.session.commit()

            else:
                self.logger.error(f"Course '{course_name}' does not exist")
                raise Exception

        except (Exception, psycopg2.Error) as error:
            self.logger.error(str(error))

    @allure.step("Delete course")
    def delete_course(self, course_name: str):
        """ Deletes a certain object "Course" from the database.
        """
        try:
            self.logger.info(f"Deleting course '{course_name}'")
            course_obj = self.session.query(Course).filter_by(name=course_name).first()

            if course_obj:
                self.session.query(RegistrationList).filter_by(id_course=course_obj.id).delete()
                self.session.delete(course_obj)
                self.session.commit()

            else:
                self.logger.error(f"Course '{course_name}' does not exist")
                raise Exception

        except (Exception, psycopg2.Error) as error:
            self.logger.error(str(error))

    @allure.step("Get courses by student id")
    def course_list_of_certain_student(self, student_id: int):
        """ Returns a list of courses by the specified student id.
        """
        try:
            self.logger.info(f"Getting courses of the student with an id '{student_id}'")
            student_obj = self.session.query(Student).filter_by(id=student_id).first()

            if student_obj is None:
                self.logger.error(f"Student with an id '{student_id}' does not exist")
                raise TypeError

            response = (self.session.query(Course.name)
                        .join(RegistrationList, Course.id == RegistrationList.id_course)
                        .join(Student, Student.id == RegistrationList.id_student)
                        .filter_by(id=student_id)
                        .all())

            course_list = []
            for name in response:
                course_list.append(name[0])

            return course_list

        except (Exception, psycopg2.Error) as error:
            self.logger.error(str(error))
