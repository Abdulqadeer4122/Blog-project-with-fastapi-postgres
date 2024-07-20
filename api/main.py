from fastapi import FastAPI
from .routes import users, auth, password_reset,blog_content
from api.database import engine, SessionLocal, get_db, Base

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(password_reset.router)
app.include_router(blog_content.router)
