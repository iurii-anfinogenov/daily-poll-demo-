"""
Daily-Poll Demo with Instance Info
"""
import datetime, os, socket
from typing import List

from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import redis
from sqlalchemy import (
    create_engine, Column, Integer, String, Text,
    DateTime, ForeignKey, func
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Конфиг из окружения
DB_URL     = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://user:pass@db:5432/poll"
)
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
CACHE_TTL  = int(os.getenv("CACHE_TTL", 86400))

# Подключение Redis и Postgres
db_engine = create_engine(DB_URL, pool_pre_ping=True, future=True)
Base = declarative_base()
Session = sessionmaker(bind=db_engine, expire_on_commit=False, future=True)
rds = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Модели
class Question(Base):
    __tablename__ = "questions"
    id         = Column(Integer, primary_key=True)
    text       = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    choices    = relationship(
        "Choice", back_populates="question",
        cascade="all, delete-orphan"
    )

class Choice(Base):
    __tablename__ = "choices"
    id          = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    text        = Column(String(100), nullable=False)
    question    = relationship("Question", back_populates="choices")

class Vote(Base):
    __tablename__ = "votes"
    id        = Column(Integer, primary_key=True)
    choice_id = Column(Integer, ForeignKey("choices.id"))
    voted_at  = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(db_engine)

# FastAPI + Jinja2
app = FastAPI(title="Daily Poll Demo")
app.mount(
    "/static", StaticFiles(directory="app/static"), name="static"
)
templates = Jinja2Templates(directory="app/templates")

# Функция для получения информации об инстансе
def get_instance_info() -> dict:
    return {
        "instance": socket.gethostname(),
        "ip": socket.gethostbyname(socket.gethostname())
    }

@app.get("/")
def show_poll(request: Request):
    info = get_instance_info()
    with Session() as session:
        q = session.query(Question).order_by(
            Question.created_at.desc()
        ).first()
        if not q:
            return templates.TemplateResponse(
                "poll.html",
                {"request": request, **info, "no_poll": True}
            )
        rows = (
            session.query(Choice.id, Choice.text, func.count(Vote.id))
            .outerjoin(Vote, Vote.choice_id == Choice.id)
            .filter(Choice.question_id == q.id)
            .group_by(Choice.id)
            .all()
        )
        return templates.TemplateResponse(
            "poll.html",
            {"request": request, **info, "question": q, "results": rows}
        )

@app.post("/vote")
def submit_vote(choice_id: int = Form(...)):
    with Session() as session:
        if not session.get(Choice, choice_id):
            raise HTTPException(404, "Choice not found")
        session.add(Vote(choice_id=choice_id))
        session.commit()
    rds.delete("results")
    return RedirectResponse(url="/", status_code=303)

@app.get("/admin")
def admin_form(request: Request):
    info = get_instance_info()
    return templates.TemplateResponse(
        "admin.html", {"request": request, **info}
    )

@app.post("/admin")
def create_poll(
    text: str = Form(...), options: str = Form(...)
):
    opts = [o.strip() for o in options.split(',') if o.strip()]
    if len(opts) < 2:
        raise HTTPException(400, "Минимум два варианта")
    with Session() as session:
        q = Question(text=text)
        session.add(q)
        session.flush()
        for o in opts:
            session.add(Choice(question_id=q.id, text=o))
        session.commit()
    rds.delete("results")
    return RedirectResponse(url="/", status_code=303)