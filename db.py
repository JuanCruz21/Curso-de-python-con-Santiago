from fastapi import FastAPI
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine, SQLModel

sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(sqlite_url)

def get_session():
    with Session(engine) as session:
        yield session

def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

SessionDep = Annotated[Session, Depends(get_session)]