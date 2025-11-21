from models.db_models import Session, Course
from views.home_view import HomeView


class MainController:

    def __init__(self, master):
        self.master = master
        self.master.geometry("500x500")
        self.master.title("Course Tracker And Analyzer")
        self.current_page = None
        self.show_home_page()

    def show_home_page(self):
        # cleanup previous page
        home_view = HomeView(parent=self.master, controller=self)  # calling with keyword args
        home_view.place(x=0, y=0, height=500, width=500)
        previous_page = self.current_page
        self.current_page = home_view
        # remove old page from memory
        if previous_page:
            previous_page.destroy()

    def go_to_add_course_page(self):
        """Switch to the Add Course page"""
        print("Go to add course page")

    def get_all_courses(self):
        """Return all courses from the database."""
        db = Session()
        courses = db.query(Course).all()
        db.close()
        return courses
