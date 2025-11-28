from tkinter import Frame, Label, Button, Entry, messagebox
from tkinter.ttk import Treeview

import utils
from views.components.add_button import AddButton
from views.components.custom_button import CustomButton
from views.components.delete_button import DeleteButton


class CourseDetailsView(Frame):
    def __init__(self, parent, controller, course_id):
        super().__init__(parent)
        self.controller = controller

        self.config(padx=10, pady=10)

        # fetch the course from the database for the given course_id
        self.course = self.controller.get_course_by_id(course_id)

        header_frame = Frame(self)
        header_frame.pack(fill="x", pady=(0, 10))

        # title
        title_text = f"{self.course.code}: {self.course.name}"
        title_label = Label(header_frame, text=title_text, wraplength=350, font=("Arial", 16), anchor="w", justify="left")
        title_label.pack(side="left", fill="x")

        # edit / delete buttons
        edit_button = CustomButton(header_frame, text="Edit")
        delete_button = DeleteButton(header_frame, text="Delete")
        back_button = CustomButton(header_frame, text="<-- Go back")
        edit_button.pack(side="left", padx=(30, 10))
        delete_button.pack(side="left", padx=(0, 10))
        back_button.pack(side="right")
        edit_button.config(command=self.handle_edit_click)
        back_button.config(command=self.handle_go_back)
        delete_button.config(command=self.handle_delete_click)

        # direct course details (term, instructor, description)
        details_frame = Frame(self, bg="white", bd=2, relief="groove", padx=10, pady=10)
        details_frame.pack(fill="x", pady=(0, 20))

        term_text = f"Term: {self.course.semester} {self.course.year}"
        instructor_text = f"Instructor: {self.course.instructor}"
        description_text = f"Description:\n{self.course.description}"
        term_label = Label(details_frame, text=term_text, bg="white", anchor="w", justify="left")
        instructor_label = Label(details_frame, text=instructor_text, bg="white", anchor="w", justify="left")
        description_label = Label(details_frame, text=description_text, bg="white", anchor="w", justify="left")
        term_label.pack(fill="x")
        instructor_label.pack(fill="x")
        description_label.pack(fill="x")


        # assessments section
        assessments_frame = Frame(self)
        assessments_frame.pack(fill="x", pady=(0, 20))
        assessments_header_frame = Frame(assessments_frame)
        assessments_header_frame.pack(fill="x", pady=(0, 10))
        header_title_label = Label(assessments_header_frame, text="Assessments")
        header_title_label.pack(side="left")
        add_assessment_button = AddButton(assessments_header_frame, text="Add Assessment")
        add_assessment_button.pack(side="left", padx=(10, 0))
        add_assessment_button.config(command=self.handle_add_assessment_click)

        # display tree table
        self.assessments_tree_table = Treeview(assessments_frame,
                                               columns=("name", "type", "weight", "earned", "grade"),
                                               show="headings",
                                               height=6)
        self.assessments_tree_table.pack(fill="x")

        # Define column headings
        self.assessments_tree_table.heading("name", text="Name", anchor="w")
        self.assessments_tree_table.heading("type", text="Type", anchor="w")
        self.assessments_tree_table.heading("weight", text="Weight", anchor="w")
        self.assessments_tree_table.heading("earned", text="Earned", anchor="w")
        self.assessments_tree_table.heading("grade", text="Grade", anchor="w")

        # Configure column properties (optional)
        self.assessments_tree_table.column("name", width=100, anchor="w")
        self.assessments_tree_table.column("type", width=100, anchor="w")
        self.assessments_tree_table.column("weight", width=75, anchor="w")
        self.assessments_tree_table.column("earned", width=75, anchor="w")
        self.assessments_tree_table.column("grade", width=75, anchor="w")

        # fetch assessments from db
        assessments = self.controller.get_assessments_for_course(course_id)

        for assessment in assessments:

            grade = f"{assessment.grade:.1f}%" if assessment.grade else '-'
            earned = f"{(assessment.grade / 100) * assessment.weight:.1f}" if assessment.grade else '-'

            values = (
                assessment.name,
                assessment.type,
                assessment.weight,
                earned,
                grade
            )
            # attach db id to the row (to retrieve when double clicking)
            self.assessments_tree_table.insert("", iid=assessment.id, index="end", values=values)

        # row double click event binding
        self.assessments_tree_table.bind("<Double-Button-1>", self.select_assessment)


        # analytics section
        analytics_frame = Frame(self)
        analytics_frame.pack(fill="x", pady=(0, 20))
        analytics_title_label = Label(analytics_frame, anchor="w", justify="left", text="Analytics")
        analytics_title_label.pack(fill="x", pady=(0, 10))
        analytics_data_frame = Frame(analytics_frame, bg="white", bd=2, relief="groove", padx=10, pady=10)
        analytics_data_frame.pack(fill="x")
        current_average_text = "Current average:"
        remaining_weight_text = "Remaining weight:"
        worst_case_text = "Worst case final mark:"
        best_case_text = "Best case final mark:"
        row_1 = Frame(analytics_data_frame, bg="white")
        row_1.pack(fill="x", pady=(0, 5))
        current_average_label = Label(row_1, text=current_average_text, bg="white", anchor="w", justify="left")
        current_average_label.pack(side="left")
        average = utils.calc_assessments_average(assessments)
        average_value = Label(row_1, text=f"{average:.1f}%", bg="white", anchor="e", justify="right")
        average_value.pack(side="right")
        row_2 = Frame(analytics_data_frame, bg="white")
        row_2.pack(fill="x", pady=(0, 5))
        remaining_weight_label = Label(row_2, text=remaining_weight_text, bg="white", anchor="w", justify="left")
        remaining_weight = utils.get_remaining_weight(assessments)
        remaining_weight_value = Label(row_2, text=f"{remaining_weight:.1f}%", bg="white", anchor="e", justify="right")
        remaining_weight_label.pack(side="left")
        remaining_weight_value.pack(side="right")
        row_3 = Frame(analytics_data_frame, bg="white")
        row_3.pack(fill="x", pady=(0, 5))
        worst_case_label = Label(row_3, text=worst_case_text, bg="white", anchor="w", justify="left")
        worst_case_mark = utils.calc_worst_case_final_mark(assessments)
        worst_case_value = Label(row_3, text=f"{worst_case_mark:.1f}%", bg="white", anchor="e", justify="right")
        worst_case_label.pack(side="left")
        worst_case_value.pack(side="right")
        row_4 = Frame(analytics_data_frame, bg="white")
        row_4.pack(fill="x", pady=(0, 5))
        best_case_label = Label(row_4, text=best_case_text, bg="white", anchor="w", justify="left")
        best_case_mark = utils.calc_best_case_final_mark(assessments)
        best_case_value = Label(row_4, text=f"{best_case_mark:.1f}%", bg="white", anchor="e", justify="right")
        best_case_label.pack(side="left")
        best_case_value.pack(side="right")

        self.assessments = assessments
        if remaining_weight > 0:
            row_5 = Frame(analytics_data_frame, bg="white")
            row_5.pack(fill="x")
            before_text_label = Label(row_5, text="To reach a final mark of ", bg="white")
            aspired_final_mark_entry = Entry(row_5, width=3, relief="flat", justify="right", bg="lightblue")
            self.aspired_final_grade_text_label = Label(row_5, text="%", bg="white")
            before_text_label.pack(side="left")
            aspired_final_mark_entry.pack(side="left")
            self.aspired_final_grade_text_label.pack(side="left")
            validate_command = (self.controller.master.register(self.compute_aspired_mark),
                                "%P")  # %P - Pass the proposed text (after the keystroke)
            aspired_final_mark_entry.config(validate="key", validatecommand=validate_command)

    def compute_aspired_mark(self, new_value):
        """
        When the user types into the aspired mark entry,
        validate the new_value entered and update the aspired_final_grade_text_label
        with the computed necessary average.
        """
        # case 1: empty text
        if new_value == '':
            self.aspired_final_grade_text_label.config(text="%")
            return True
        # case 2: numeric text
        if new_value.isnumeric():
            aspired_mark = int(new_value)
            required_average = utils.calc_required_remaining_average(
                assessments=self.assessments, aspired_final_mark=aspired_mark)
            # case 2.1: impossible required average (negative number or above 100 percent)
            if required_average < 0 or required_average > 100:
                self.aspired_final_grade_text_label.config(text=f"% is impossible (based on your recorded assessments).")
            else:  # case 2.2: valid required average
                text = f"%, you must average {required_average:.1f}% on the remaining weight."
                self.aspired_final_grade_text_label.config(text=text)
            return True
        # case 3: invalid input
        return False


    def handle_edit_click(self):
        """
        Navigate to the edit page when clicking on the edit button.
        """
        self.controller.show_edit_course_page(self.course)

    def handle_go_back(self):
        """
        Navigate back to the courses page when clicking on the Go back button.
        """
        self.controller.show_home_page()

    def handle_delete_click(self):
        """
        Show a confirmation dialog to delete course.
        If confirmed, delete course and all of its assessments
        """
        is_yes = messagebox.askyesno("Delete",
        f"Are you sure you want delete {self.course.code}?"
                f"\nThis action will delete all of its assessments as well.")

        if is_yes:
            self.controller.delete_course(self.course.id)
            self.controller.show_home_page()

    def handle_add_assessment_click(self):
        """Navigate to the Add Assessment page when clicking on the add button."""
        self.controller.show_add_assessment_page(course=self.course)

    def select_assessment(self, event):
        """Navigate user to the Edit Assessment page for selected assessment."""
        assessment_id = self.assessments_tree_table.identify_row(event.y)
        # check user clicked on a valid row
        if assessment_id:
            assessment = self.controller.get_assessment_by_id(assessment_id)
            self.controller.show_edit_assessment_page(course=self.course, assessment=assessment)