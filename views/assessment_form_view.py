from tkinter import Frame, Label, Entry, messagebox, StringVar
from tkinter.ttk import Combobox

from views.components.custom_button import CustomButton
from views.components.delete_button import DeleteButton


class AssessmentFormView(Frame):
    """
    This class is used to create a form for "Adding" / "Editing" an assessment.
    """
    def __init__(self, parent, controller, course, assessment):
        super().__init__(parent)
        self.controller = controller

        self.config(padx=10, pady=10)

        self.is_editing = assessment is not None  # boolean
        self.assessment = assessment
        self.course = course

        title = "Add Assessment"
        if self.is_editing:
            title = "Edit Assessment"

        title_label = Label(self, text=title, font=("Arial", 24), anchor="w", justify="left")
        title_label.pack(fill="x", pady=(0, 10))

        form_errors_frame = Frame(self)
        form_errors_frame.pack(fill="x")

        # set up the form_frame for the form
        form_frame = Frame(self)
        form_frame.pack(fill="x")
        # 5 rows
        form_frame.grid_rowconfigure(0, weight=1, pad=10)
        form_frame.grid_rowconfigure(1, weight=1, pad=10)
        form_frame.grid_rowconfigure(2, weight=1, pad=10)
        form_frame.grid_rowconfigure(3, weight=1, pad=10)
        form_frame.grid_rowconfigure(4, weight=1, pad=10)
        # 2 column
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=4)

        # Labels
        course_label = Label(form_frame, text="Course:")
        course_label.grid(row=0, column=0, sticky="w")

        title_label = Label(form_frame, text="Title:")
        title_label.grid(row=1, column=0, sticky="w")

        weight_label = Label(form_frame, text="Weight:")
        weight_label.grid(row=2, column=0, sticky="w")

        grade_label = Label(form_frame, text="Grade (%):")
        grade_label.grid(row=3, column=0, sticky="w")

        self.type_label = Label(form_frame, text="Type:")
        self.type_label.grid(row=4, column=0, sticky="w")

        # entries
        self.course_name_label = Label(form_frame, text=f"{course.code} - {course.name}", justify="left", anchor="w")
        self.course_name_label.grid(row=0, column=1, sticky="we")
        self.title_entry = Entry(form_frame)
        self.title_entry.grid(row=1, column=1, sticky="we")
        self.weight_entry = Entry(form_frame)
        self.weight_entry.grid(row=2, column=1, sticky="we")
        self.grade_entry = Entry(form_frame)
        self.grade_entry.grid(row=3, column=1, sticky="we")
        self.type_var = StringVar()
        self.type_entry = Combobox(form_frame, textvariable=self.type_var,
                                       values=["Assignment", "Lab", "Test", "Quiz", "Exam"], state="readonly")
        self.type_entry.grid(row=4, column=1, sticky="we")

        # validators
        validate_command = (self.controller.master.register(self.validate_number_only),
                            "%P")  # %P - Pass the proposed text (after the keystroke)
        self.grade_entry.config(validate="key", validatecommand=validate_command)
        validate_only_alpha = (self.controller.master.register(self.validate_number_only),
                            "%P")  # %P - Pass the proposed text (after the keystroke)
        self.weight_entry.config(validate="key", validatecommand=validate_only_alpha)

        # form errors
        self.errors_label = Label(form_errors_frame, text="", fg="red", bg="pink", justify="left", anchor="w",
                                  padx=10, pady=10)

        # buttons
        buttons_container = Frame(self)
        buttons_container.pack(fill="x", pady=20)
        save_button = CustomButton(buttons_container, text="Save")
        save_button.pack(side="right", padx=(10, 0))
        save_button.config(command=self.handle_click_save)
        cancel_button = CustomButton(buttons_container, text="Cancel")
        cancel_button.pack(side="right")
        cancel_button.config(command=self.handle_click_cancel)

        # editing scenario (pre-fill the entries with values)
        if self.is_editing:
            grade = str(int(assessment.grade)) if assessment.grade else ""
            self.title_entry.insert(0, assessment.name)
            self.weight_entry.insert(0, str(int(assessment.weight)))
            self.grade_entry.insert(0, grade)
            self.type_var.set(assessment.type)
            # include delete functionality when in edit mode
            delete_button = DeleteButton(buttons_container, text="Delete")
            delete_button.pack(side="right", padx=(0, 10))
            delete_button.config(command=self.handle_delete_click)

    def validate_only_alpha(self, new_value):
        """
        Return True when the new_value is a valid alph string, ignoring spaces (allow to fully erase).
        Otherwise, return False.
        """
        if new_value.replace(' ', '').isalpha() or new_value == '':
            return True
        return False

    def validate_number_only(self, new_value):
        """
        Return True when the new_value is a valid integer for the year (allow to fully erase).
        Otherwise, return False.
        """
        if new_value.isnumeric() or new_value == '':
            return True
        return False

    def handle_click_save(self):
        """
        Handle the clicking on the save button by collecting the data from
        the entries and submitting it to the database
        """

        title = self.title_entry.get()
        weight = self.weight_entry.get()
        grade = self.grade_entry.get()
        assessment_type = self.type_entry.get()

        # validate that required inputs are not empty
        errors = []
        if title == '':
            errors.append("- Title must not be empty.")
        if weight == '':
            errors.append("- Weight must not be empty.")
        if assessment_type == '':
            errors.append("- Type must not be empty.")

        if len(errors) > 0:
            errors_text = "Form errors:\n"
            errors_text += "\n".join(errors)
            self.errors_label.config(text=errors_text)
            self.errors_label.pack(fill="x", pady=(0, 5))
            return # avoid the submission

        grade = int(grade) if grade else None

        if self.is_editing:
            self.controller.update_assessment(
                assessment_id=self.assessment.id,
                title=title,
                weight=weight,
                grade=grade,
                assessment_type=assessment_type,
            )
        # add assessment to db
        else:
            self.controller.create_assessment(
                course_id=self.course.id,
                title=title,
                weight=weight,
                grade=grade,
                assessment_type=assessment_type,
            )
        # go to the course details page
        self.controller.show_course_details_page(self.course.id)

    def handle_click_cancel(self):
        """
        Show a cancel confirm dialog.
        If confirming, disregard any entered data and navigate to the course details page.
        """

        is_cancel = messagebox.askokcancel("Cancel?", "Are you sure you want leave unsaved changes?")
        if is_cancel:
            self.controller.show_course_details_page(self.course.id)


    def handle_delete_click(self):
        """Delete existing assessment when clicking delete button. Navigate to course details page on confirmation."""
        is_yes = messagebox.askyesno("Delete", "Are you sure you want to delete this assessment?")
        if is_yes:
            self.controller.delete_assessment(assessment_id=self.assessment.id)
            self.controller.show_course_details_page(self.course.id)
