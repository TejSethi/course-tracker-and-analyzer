from tkinter import Frame, Label, Button, ttk


class HomeView(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.config(padx=10, pady=10)

        title_label = Label(self, text="Courses", font=("Arial", 24), anchor="w", justify="left")
        title_label.pack(fill="x", pady=(0, 10))

        add_course_button = Button(self, text="Add Course", bg="white", bd=1, relief="solid", cursor="hand2",
                                   command=self.controller.go_to_add_course_page)
        add_course_button.pack(anchor="w")
        add_course_button.config(padx=10)


        # courses table
        columns = ("course", "instructor", "term", "average")
        courses_table_tree = ttk.Treeview(self, columns=columns, show="headings")
        courses_table_tree.pack(fill="x", pady=10)

        # Define column headings
        courses_table_tree.heading("course", text="Course", anchor="w")
        courses_table_tree.heading("instructor", text="Instructor", anchor="w")
        courses_table_tree.heading("term", text="Term", anchor="w")
        courses_table_tree.heading("average", text="Average", anchor="w")

        # Configure column properties (optional)
        courses_table_tree.column("course", width=150, anchor="w")
        courses_table_tree.column("instructor", width=150, anchor="w")
        courses_table_tree.column("term", width=100, anchor="w")
        courses_table_tree.column("average", width=50, anchor="w")

        # fetch data from db
        courses = self.controller.get_all_courses()

        for course in courses:
            values = (
                f"{course.code}: {course.name}",
                course.instructor,
                f"{course.semester} {course.year}",
                "85%"
            )
            courses_table_tree.insert("", index="end", values=values)
