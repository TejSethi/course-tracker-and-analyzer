from tkinter import Frame, Label, Button, Entry, Text, messagebox, StringVar
from tkinter.ttk import Combobox

from views.components.custom_button import CustomButton


class CourseFormView(Frame):
    """
    This class is used to create a form for "Adding" / "Editing" a course.
    """
    def __init__(self, parent, controller, course):
        super().__init__(parent)
        self.controller = controller

        self.config(padx=10, pady=10)

        self.is_editing = course is not None  # boolean
        self.course = course

        title = "Add Course"
        if self.is_editing:
            title = "Edit Course"

        title_label = Label(self, text=title, font=("Arial", 24), anchor="w", justify="left")
        title_label.pack(fill="x", pady=(0, 10))

        form_errors_frame = Frame(self)
        form_errors_frame.pack(fill="x")

        # set up the form_frame for the form
        form_frame = Frame(self)
        form_frame.pack(fill="x")
        # 6 rows
        form_frame.grid_rowconfigure(0, weight=1, pad=10)
        form_frame.grid_rowconfigure(1, weight=1, pad=10)
        form_frame.grid_rowconfigure(2, weight=1, pad=10)
        form_frame.grid_rowconfigure(3, weight=1, pad=10)
        form_frame.grid_rowconfigure(4, weight=1, pad=10)
        form_frame.grid_rowconfigure(5, weight=1, pad=10)
        # 2 column
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=4)

        # Labels
        name_label = Label(form_frame, text="Name:")
        name_label.grid(row=0, column=0, sticky="w")

        code_label = Label(form_frame, text="Code:")
        code_label.grid(row=1, column=0, sticky="w")

        instructor_label = Label(form_frame, text="Instructor:")
        instructor_label.grid(row=2, column=0, sticky="w")

        semester_label = Label(form_frame, text="Semester:")
        semester_label.grid(row=3, column=0, sticky="w")

        self.year_label = Label(form_frame, text="Year:")
        self.year_label.grid(row=4, column=0, sticky="w")

        description_label = Label(form_frame, text="Description:")
        description_label.grid(row=5, column=0, sticky="nw")


        # entries
        self.name_entry = Entry(form_frame)
        self.name_entry.grid(row=0, column=1, sticky="we")
        self.code_entry = Entry(form_frame)
        self.code_entry.grid(row=1, column=1, sticky="we")
        self.instructor_entry = Entry(form_frame)
        self.instructor_entry.grid(row=2, column=1, sticky="we")
        self.semester_var = StringVar()
        self.semester_entry = Combobox(form_frame, textvariable=self.semester_var,
                                       values=["Fall", "Winter", "Summer", "Full-Year"], state="readonly")
        self.semester_entry.grid(row=3, column=1, sticky="we")
        self.year_entry = Entry(form_frame)
        self.year_entry.grid(row=4, column=1, sticky="we")
        self.description_textarea = Text(form_frame, width=30, height=5, wrap="word")
        self.description_textarea.grid(row=5, column=1, sticky="we")

        # validators
        validate_command = (self.controller.master.register(self.validate_year_entry),
                            "%P")  # %P - Pass the proposed text (after the keystroke)
        self.year_entry.config(validate="key", validatecommand=validate_command)
        validate_only_alpha = (self.controller.master.register(self.validate_only_alpha),
                            "%P")  # %P - Pass the proposed text (after the keystroke)
        self.instructor_entry.config(validate="key", validatecommand=validate_only_alpha)

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
            original_description = course.description if course.description else ''
            self.name_entry.insert(0, course.name)
            self.instructor_entry.insert(0, course.instructor)
            self.code_entry.insert(0, course.code)
            self.description_textarea.insert(1.0, original_description)
            self.year_entry.insert(0, str(course.year))
            self.semester_var.set(course.semester)

    def validate_only_alpha(self, new_value):
        """
        Return True when the new_value is a valid alph string, ignoring spaces (allow to fully erase).
        Otherwise, return False.
        """
        if new_value.replace(' ', '').isalpha() or new_value == '':
            return True
        return False

    def validate_year_entry(self, new_value):
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

        name = self.name_entry.get()
        code = self.code_entry.get()
        instructor = self.instructor_entry.get()
        semester = self.semester_entry.get()
        year = self.year_entry.get()
        # to get all text from Text object, 1.0 means start on line 1 character 0, and get all till the end
        description = self.description_textarea.get("1.0", 'end-1c')

        # validate that required inputs are not empty
        errors = []
        if name == '':
            errors.append("- Name must not be empty.")
        if code == '':
            errors.append("- Code must not be empty.")
        if instructor == '':
            errors.append("- Instructor must not be empty.")
        if semester == '':
            errors.append("- Semester must not be empty.")
        if year == '':
            errors.append("- Year must not be empty.")

        # Future TODO: verify course isn't a duplicate (course with the same code, semester, year doesn't already exist)

        if len(errors) > 0:
            errors_text = "Form errors:\n"
            errors_text += "\n".join(errors)
            self.errors_label.config(text=errors_text)
            self.errors_label.pack(fill="x", pady=(0, 5))
            return # avoid the submission

        year = int(year)  # cast year to int

        if self.is_editing:
            self.controller.update_course(
                course_id=self.course.id,
                name=name,
                code=code,
                instructor=instructor,
                semester=semester,
                year=year,
                description=description
            )
        # add course to db
        else:
            self.controller.create_course(
                name=name,
                code=code,
                instructor=instructor,
                semester=semester,
                year=year,
                description=description
            )
        # go to the home view
        self.controller.show_home_page()


    def handle_click_cancel(self):
        """
        Show a cancel confirm dialog.
        If confirming, disregard any entered data and navigate to the home page.
        """

        is_cancel = messagebox.askokcancel("Cancel?", "Are you sure you want leave unsaved changes?")
        if is_cancel:
            if self.is_editing:
                self.controller.show_course_details_page(self.course.id)
            else:
                self.controller.show_home_page()
