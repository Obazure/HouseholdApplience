from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
import uvicorn

import config
import crud
import models
import schemas
import database

models.Base.metadata.create_all(bind=database.engine)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title='Household',
    docs_url="/api/docs",
    openapi_url="/api"
)
origins = [
    "https://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = database.SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


def get_db(request: Request):
    return request.state.db


@app.post("/api/household/", response_model=schemas.Household)
def create_entity(entity: schemas.HouseholdCreate, db_session: Session = Depends(get_db)):
    try:
        db_entity = crud.create_entity(db_session, entity=entity)
        if not db_entity:
            raise HTTPException(status_code=400, detail="Something wrong, try again")
        return db_entity
    except (HTTPException, NoResultFound, ValueError) as error:
        raise HTTPException(status_code=404, detail=error.detail) from error


@app.get("/api/household/", response_model=List[schemas.Household])
def get_entities(db_session: Session = Depends(get_db)):
    db_entities = crud.get_entities(db_session)
    if not db_entities:
        raise HTTPException(status_code=400, detail="Something wrong, try again")
    return db_entities


@app.get("/api/household/{id}", response_model=schemas.Household)
def get_entity(id: int, db_session: Session = Depends(get_db)):
    db_entity = crud.get_entity(db_session, id)
    if not db_entity:
        raise HTTPException(status_code=400, detail="Something wrong, try again")
    return db_entity


@app.put("/api/household", response_model=schemas.Household)
def edit_entity(entity: schemas.Household, db_session: Session = Depends(get_db)):
    try:
        db_entity = crud.edit_entity(db_session, entity)
        if not db_entity:
            raise HTTPException(status_code=400, detail="Something wrong, try again")
        return db_entity
    except (HTTPException, NoResultFound, ValueError) as error:
        raise HTTPException(status_code=404, detail=error.detail) from error


@app.delete("/api/household/{id}")
def remove_entity(id: int, db_session: Session = Depends(get_db)):
    try:
        confirmation = crud.remove_entity(db_session, id=id)
        if not confirmation:
            raise HTTPException(status_code=400, detail="Email already registered")
        return confirmation
    except (HTTPException, NoResultFound, ValueError) as error:
        raise HTTPException(status_code=404, detail=error.detail) from error


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=config.BACKEND_PORT)
