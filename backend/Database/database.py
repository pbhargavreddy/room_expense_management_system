from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base


# URL for db connection 
URL = "postgresql://bhargav:bhargav123!@localhost:5432/p2"

#Engine for sessionLocal
engine = create_engine(URL)

# SessionLocal
SessionLocal = sessionmaker(autoflush=False, bind=engine)

#Base model
Base = declarative_base()

# Function for session management. Scalability
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# exports  engine, SessionLocal, Base, get_db