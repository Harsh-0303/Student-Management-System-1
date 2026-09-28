from Database.database import engine, Base
from Database.models import User, Movie, Rating


Base.metadata.create_all(bind=engine)

print("Tables created successfully!")