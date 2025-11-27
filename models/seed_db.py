from db_models import Session, Course, Assessment

# insert a few courses (test data)
db = Session()

course1 = Course(
    name="Intro to programming",
    code="CSC108",
    instructor="Daniel Zingaro",
    semester="Fall",
    year=2021,
    description="Python fundamentals programming for beginners..."
)

course2 = Course(
    name="Software Design",
    code="CSC148",
    instructor="David Liu",
    semester="Winter",
    year=2022,
    description="Introduction to object-oriented programming and software design principles."
)

course3 = Course(
    name="Data Structures and Algorithms",
    code="CSC263",
    instructor="Michelle Craig",
    semester="Fall",
    year=2022,
    description="Algorithm design, time complexity, and classic data structures."
)

course4 = Course(
    name="Operating Systems",
    code="CSC369",
    instructor="Shen Wang",
    semester="Winter",
    year=2023,
    description="Processes, threads, concurrency, memory management, and OS architecture."
)

course5 = Course(
    name="Artificial Intelligence",
    code="CSC384",
    instructor="Graeme Hirst",
    semester="Fall",
    year=2023,
    description="Search, constraint satisfaction, planning, reasoning, and introductory AI theory."
)

db.add_all([course1, course2, course3, course4, course5])
db.commit()


# Seed assessments

assessment1 = Assessment(
    course_id=course1.id,
    name="A1",
    grade=80.0,
    weight=10.0,
    type="Assignment"
)

assessment2 = Assessment(
    course_id=course1.id,
    name="Midterm 1",
    grade=75.0,
    weight=20.0,
    type="Test"
)

assessment3 = Assessment(
    course_id=course1.id,
    name="A2",
    grade=80.0,
    weight=20.0,
    type="Assignment"
)

assessment4 = Assessment(
    course_id=course1.id,
    name="Midterm 2",
    grade=None,
    weight=20.0,
    type="Test"
)

assessment5 = Assessment(
    course_id=course1.id,
    name="Final Exam",
    grade=None,
    weight=30.0,
    type="Exam"
)

db.add_all([assessment1, assessment2, assessment3, assessment4, assessment5])
db.commit()

db.close()


print("Database Seeded")