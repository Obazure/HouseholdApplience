from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

import models
import schemas


def create_entity(db_session: Session, entity: schemas.HouseholdCreate):
    db_entity = models.Household(**entity.dict())
    db_session.add(db_entity)
    db_session.commit()
    db_session.refresh(db_entity)
    return db_entity


def get_entities(db_session: Session):
    return db_session.query(models.Household).all()


def get_entity(db_session: Session, id: int):
    return db_session.query(models.Household).filter(models.Household.id == id).first()


def edit_entity(db_session: Session, entity: schemas.Household):
    db_entity = db_session.query(models.Household).filter(models.Household.id == entity['id']).first()
    if not db_entity:
        raise NoResultFound("Entity not found while updating")
    db_entity.query.update(entity.dict())
    db_session.add(db_entity)
    db_session.commit()
    db_session.refresh(db_entity)
    return db_entity


def remove_entity(db_session: Session, id: int):
    db_session.query(models.Household).filter(models.Household.id == id).delete()
    db_session.commit()
    return True
