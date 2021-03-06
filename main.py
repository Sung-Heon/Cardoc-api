
from fastapi import FastAPI

from sql_app import models
from sql_app.database import engine
from api import auth, tire

models.Base.metadata.create_all(bind=engine)

def create_app():
    app = FastAPI(title="Cardoc Restfull API",)
    app.include_router(auth.router)
    app.include_router(tire.router)

    return app


app = create_app()

