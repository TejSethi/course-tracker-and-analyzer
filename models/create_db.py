from models.db_models import Base, engine

# Create all tables (MAKE SURE TO DROP TABLES THAT ALREADY EXIST FIRST)
print("Dropping all tables")
Base.metadata.drop_all(engine)
print("Creating all tables")
Base.metadata.create_all(engine)
print("Tables are Ready")
