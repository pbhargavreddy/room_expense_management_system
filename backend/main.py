from fastapi import FastAPI,Depends,HTTPException, status
from backend.Database.database import Base,get_db,SessionLocal,engine
from backend.routes import user_routes,response_routes,resquest_routes
#fastapi object
app = FastAPI()

# Create tables
Base.metadata.create_all(bind = engine)


app.include_router(user_routes.router)
