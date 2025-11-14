from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Create an SQLite database engine
# The '///' indicates a relative path to the database file in the
# current directory.
# 'echo=True' will log all SQL statements executed, useful for debugging.
engine = create_engine('sqlite:///database.db', echo=False)

# 2. Define a declarative base for ORM models
Base = declarative_base()


# Create the session Class (NOT making the object though, this is just defining the class)
Session = sessionmaker(bind=engine)


# 3. Define all tables
class Course(Base):
    __tablename__ = 'courses' # Name of the table in the database

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    description = Column(String)
    instructor = Column(String, nullable=False)
    semester = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    def __repr__(self):
        return f"Course(id={self.id}, name='{self.name}', code='{self.code}')"


class Assessment(Base):
    __tablename__ = 'assessments' # Name of the table in the database

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    name = Column(String, nullable=False)
    grade = Column(Float)
    weight = Column(Float, nullable=False)
    type = Column(String, nullable=False)

    def __repr__(self):
        return f"Assessment(id={self.id}, name='{self.name}', course_id = {self.course_id})"
