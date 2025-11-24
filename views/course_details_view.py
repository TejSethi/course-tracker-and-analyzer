from tkinter import Frame, Label

class CourseDetailsView(Frame):
    def __init__(self, parent, controller, course_id):
        super().__init__(parent)
        self.controller = controller

        self.config(padx=10, pady=10)

        # fetch the course from the database for the given course_id
        course = self.controller.get_course_by_id(course_id)

        title_text = f"{course.code}: {course.name}"
        title_label = Label(self, text=title_text, font=("Arial", 24), anchor="w", justify="left")
        title_label.pack(fill="x", pady=(0, 10))
