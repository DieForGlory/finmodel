from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.db.database import engine, Base
from app.api.v1 import simulate
from app.db import base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Real Estate FinModel")

# Подключение статики и шаблонов
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(simulate.router, prefix="/api/v1/simulation", tags=["Simulation"])

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "FinModel Dashboard"})