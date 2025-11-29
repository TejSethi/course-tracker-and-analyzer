from tkinter.ttk import Style

from models.db_models import Session, Course, Assessment
from views.assessment_form_view import AssessmentFormView
from views.course_details_view import CourseDetailsView
from views.course_form_view import CourseFormView
from views.home_view import HomeView


class MainController:

    def __init__(self, master):
        self.master = master
        self.master.option_add("*Font", "Arial 11")  # global font
        style = Style()
        style.configure("Treeview", font=("Arial", 11))
        self.master.geometry("600x600")
        self.master.title("Course Tracker And Analyzer")
        self.current_page = None
        self.show_home_page()

    def show_home_page(self):
        # cleanup previous page
        previous_page = self.current_page
        # remove old page from memory
        if previous_page:
            previous_page.destroy()

        home_view = HomeView(parent=self.master, controller=self)  # calling with keyword args
        home_view.pack(fill="both", expand=True)
        self.current_page = home_view

    def show_add_course_page(self):
        """Switch to the Add Course page"""
        previous_page = self.current_page
        # remove old page from memory
        if previous_page:
            previous_page.destroy()
        add_course_view = CourseFormView(parent=self.master, controller=self, course=None)  # calling with keyword args
        add_course_view.pack(fill="both", expand=True)
        self.current_page = add_course_view

    def show_course_details_page(self, course_id):
        """Switch to the Course Details page"""
        previous_page = self.current_page
        # remove old page from memory
        if previous_page:
            previous_page.destroy()
        course_details_view = CourseDetailsView(parent=self.master, controller=self, course_id=course_id)
        course_details_view.pack(fill="both", expand=True)
        self.current_page = course_details_view

    def show_edit_course_page(self, course):
        """Switch to the Course Edit page to edit the course given."""
        previous_page = self.current_page
        # remove old page from memory
        if previous_page:
            previous_page.destroy()
        edit_course_view = CourseFormView(parent=self.master, controller=self, course=course)  # calling with keyword args
        edit_course_view.pack(fill="both", expand=True)
        self.current_page = edit_course_view

    def show_add_assessment_page(self, course):
        """Switch to the Assessment Add page to add new assessment for the course given."""
        previous_page = self.current_page
        # remove old page from memory
        if previous_page:
            previous_page.destroy()
        add_assessment_view = AssessmentFormView(parent=self.master, controller=self, course=course, assessment=None)
        add_assessment_view.pack(fill="both", expand=True)
        self.current_page = add_assessment_view

    def show_edit_assessment_page(self, course, assessment):
        """Switch to the Assessment Edit page to edit existing assessment for the course given."""
        previous_page = self.current_page
        # remove old page from memory
        if previous_page:
            previous_page.destroy()
        edit_assessment_view = AssessmentFormView(parent=self.master, controller=self,
                                                  course=course, assessment=assessment)
        edit_assessment_view.pack(fill="both", expand=True)
        self.current_page = edit_assessment_view

    def get_all_courses(self):
        """Return all courses from the database."""
        db = Session()
        courses = db.query(Course).all()
        db.close()
        return courses

    def create_course(self, name, description, code, instructor, semester, year):
        """Create a new course in the database."""
        db = Session()
        course = Course(name=name, description=description, code=code,
                        instructor=instructor, semester=semester, year=year)
        db.add(course)
        db.commit()
        db.close()

    def get_course_by_id(self, course_id):
        """Return course by course_id (pk) from the database."""
        db = Session()
        course = db.query(Course).filter(Course.id == course_id).first()
        db.close()
        return course

    def get_assessments_for_course(self, course_id):
        """Return list of assessments for course by the given course_id."""
        db = Session()
        assessments = db.query(Assessment).filter(Assessment.course_id == course_id).all()
        db.close()
        return assessments

    def update_course(self, course_id, name, description, code, instructor, semester, year):
        """Update course by course_id with the new values."""
        db = Session()
        course = db.query(Course).filter(Course.id == course_id).first()
        course.name = name
        course.description = description
        course.code = code
        course.instructor = instructor
        course.semester = semester
        course.year = year
        db.commit()
        db.close()

    def delete_course(self, course_id):
        """Delete course by course_id, deleting all related assessments as well."""
        db = Session()
        course = db.query(Course).filter(Course.id == course_id).first()
        # delete each assessment (ondelete='CASCADE' not working)
        assessments = db.query(Assessment).filter(Assessment.course_id == course_id).all()
        for a in assessments:
            db.delete(a)
        db.delete(course)
        db.commit()
        db.close()

    def create_assessment(self, course_id, title, weight, grade, assessment_type):
        """Create assessment for course course_id with the given values."""
        db = Session()
        assessment = Assessment(
            course_id=course_id,
            name=title,
            weight=weight,
            grade=grade,
            type=assessment_type
        )
        db.add(assessment)
        db.commit()
        db.close()

    def update_assessment(self, assessment_id, title, weight, grade, assessment_type):
        """Update assessment by assessment_id with the given values."""
        db = Session()
        assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
        assessment.name = title
        assessment.weight = weight
        assessment.grade = grade
        assessment.type = assessment_type
        db.commit()
        db.close()

    def get_assessment_by_id(self, assessment_id):
        """Get Assessment by id."""
        db = Session()
        assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
        db.close()
        return assessment

    def delete_assessment(self, assessment_id):
        """Delete assessment by assessment_id."""
        db = Session()
        assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
        db.delete(assessment)
        db.commit()
        db.close()