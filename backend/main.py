from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.Database.database import Base, engine, ensure_schema
from backend.routes import notification_routes, user_routes

app = FastAPI(title="Room Expenses Notification API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
ensure_schema()

app.include_router(user_routes.router)
app.include_router(notification_routes.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
