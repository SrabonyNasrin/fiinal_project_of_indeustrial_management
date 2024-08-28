from fastapi import FastAPI
import uvicorn
from app.database import engine, Base
from app import models
from app.routes import news_scrap

app = FastAPI()

# # Create the database if it doesn't exist
# database.create_database()

# Create tables
models.Base.metadata.create_all(bind=engine)

app.include_router(news_scrap.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the News Summary API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8011, reload=True)