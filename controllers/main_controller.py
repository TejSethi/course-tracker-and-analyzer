from models.db_models import Session, Course
from views.course_form_view import CourseFormView
from views.home_view import HomeView


class MainController:

    def __init__(self, master):
        self.master = master
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

    def go_to_add_course_page(self):
        """Switch to the Add Course page"""
        previous_page = self.current_page
        # remove old page from memory
        if previous_page:
            previous_page.destroy()
        add_course_view = CourseFormView(parent=self.master, controller=self)  # calling with keyword args
        add_course_view.pack(fill="both", expand=True)
        self.current_page = add_course_view

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