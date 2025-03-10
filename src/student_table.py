import allure
import psycopg2

from src.db_tables import Course, Student, RegistrationList
from src.base_db import BaseDB


class StudentTable(BaseDB):
    """Class for interacting with the 'Student' table of the database.
    """

    @allure.step("Get student id by name and age")
    def get_student_id_by_name_age(self, student_name, student_age):
        """Returns a student id by his name and age.
        """
        self.logger.info(f"Getting student id by his name and age")
        student_id = self.session.query(Student.id).filter_by(name=student_name, age=student_age).first()[0]

        return student_id

    @allure.step("Get student name by id")
    def get_student_name_by_id(self, student_id):
        """Returns a student name by his id.
        """
        self.logger.info(f"Getting student name by his id")
        received_name = self.session.query(Student.name).filter_by(id=student_id).first()[0]

        return received_name

    @allure.step("Add student")
    def add_student(self, name: str, age: int, courses: list[str]):
        """ Adds a new object "Student" to the database.
        """
        try:
            self.logger.info(f"Adding student '{name}'")
            new_student = Student(name=name, age=age)
            self.session.add(new_student)

            for course in courses:
                course_obj = self.session.query(Course).filter_by(name=course).first()

                if course_obj is None:
                    self.logger.error(f"Course '{course}' does not exist")
                    raise TypeError

                new_registration = RegistrationList(student=new_student,
                                                    course=course_obj)
                self.session.add(new_registration)

            self.session.commit()

        except (Exception, psycopg2.Error) as error:
            self.logger.error(str(error))

    @allure.step("Update student")
    def update_student(self, student_id: int, updated_name: str = None, updated_age: int = None):
        """ Updates an information about a certain object "Student".
        """
        try:
            self.logger.info(f"Updating student with an id '{student_id}'")
            student_obj = self.session.query(Student).filter_by(id=student_id).first()

            if student_obj:
                if updated_name is not None:
                    student_obj.name = updated_name

                if updated_age is not None:
                    student_obj.age = updated_age

                self.session.commit()

            else:
                self.logger.error(f"Student with an id '{student_id}' does not exist")
                raise Exception

        except (Exception, psycopg2.Error) as error:
            self.logger.error(str(error))

    @allure.step("Delete student")
    def delete_student(self, student_id: int):
        """ Deletes a certain object "Student" from the database.
        """
        try:
            self.logger.info(f"Deleting student with an id '{student_id}'")
            student_obj = self.session.query(Student).filter_by(id=student_id).first()

            if student_obj:
                self.session.query(RegistrationList).filter_by(id_student=student_id).delete()
                self.session.delete(student_obj)
                self.session.commit()

            else:
                self.logger.error(f"Student with an id '{student_id}' does not exist")
                raise Exception

        except (Exception, psycopg2.Error) as error:
            self.logger.error(str(error))

    @allure.step("Get students by course name")
    def student_list_of_certain_course(self, course_name: str):
        """ Prints and returns a list of students by the specified course name.
        """
        try:
            self.logger.info(f"Getting students with the course '{course_name}'")
            course_obj = self.session.query(Course).filter_by(name=course_name).first()

            if course_obj is None:
                self.logger.error(f"Course '{course_name}' does not exist")
                raise TypeError

            response = (self.session.query(Student.name, Student.age)
                        .join(RegistrationList, Student.id == RegistrationList.id_student)
                        .join(Course, Course.id == RegistrationList.id_course)
                        .filter_by(name=course_name)
                        .all())

            return response

        except (Exception, psycopg2.Error) as error:
            self.logger.error(str(error))
