from tkinter import Frame, Label, Button, ttk

import utils
from views.components.add_button import AddButton
from views.components.custom_button import CustomButton


class HomeView(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.config(padx=10, pady=10)

        title_label = Label(self, text="Courses", font=("Arial", 24), anchor="w", justify="left")
        title_label.pack(fill="x", pady=(0, 10))

        add_course_button = AddButton(self, text="Add Course", command=self.controller.show_add_course_page)
        add_course_button.pack(anchor="w")
        add_course_button.config(padx=10)


        # courses table
        columns = ("course", "instructor", "term", "average")
        self.courses_table_tree = ttk.Treeview(self, columns=columns, show="headings")
        self.courses_table_tree.pack(fill="x", pady=10)

        # Define column headings
        self.courses_table_tree.heading("course", text="Course", anchor="w")
        self.courses_table_tree.heading("instructor", text="Instructor", anchor="w")
        self.courses_table_tree.heading("term", text="Term", anchor="w")
        self.courses_table_tree.heading("average", text="Average", anchor="w")

        # Configure column properties (optional)
        self.courses_table_tree.column("course", width=150, anchor="w")
        self.courses_table_tree.column("instructor", width=150, anchor="w")
        self.courses_table_tree.column("term", width=100, anchor="w")
        self.courses_table_tree.column("average", width=50, anchor="w")

        # fetch data from db
        courses = self.controller.get_all_courses()

        for course in courses:
            assessments = self.controller.get_assessments_for_course(course.id)
            average = utils.calc_assessments_average(assessments)
            average_text = "-"
            if len(assessments) > 0:
                average_text = f"{average:.1f}%"
            values = (
                f"{course.code}: {course.name}",
                course.instructor,
                f"{course.semester} {course.year}",
                average_text
            )
            # attach db id to the row (to retrieve when double clicking)
            self.courses_table_tree.insert("", iid=course.id, index="end", values=values)

        # row double click event binding
        self.courses_table_tree.bind("<Double-Button-1>", self.select_course)

    def select_course(self, event):
        course_id = self.courses_table_tree.identify_row(event.y)
        # check user clicked on a valid row
        if course_id:
            self.controller.show_course_details_page(course_id)

