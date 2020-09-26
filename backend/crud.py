from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.orm import Session

import models
import schemas


def get(db_session: Session, model, **kwargs):
    return db_session.query(model).filter_by(**kwargs).first()


def _get_or_create(db_session: Session, model, **kwargs):
    instance = get(db_session, model, **kwargs)
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        # db_session.add(instance)
        return instance, True


def save_query_with_details(db_session: Session, data: schemas.QueryWrite):
    db_query, is_created = _get_or_create(db_session, models.Query,
                                          query=data['query'].lower(), query_hash=data['query_hash'])

    for article in data['articles']:

        db_article, is_created = _get_or_create(
            db_session, models.Article,
            source_url=article['source_url'],
            source_url_hash=article['source_url_hash'],
            source_tag=str(article['source_tag']).lower(),
            published_at=datetime.strptime(article['published_at'], "%Y-%m-%dT%H:%M:%SZ"),
            title=article['title'],
            read_url=article['read_url'],
            content=article['content'],
            result=article['result'],
        )

        if article['categories']:
            for category in article['categories']:
                db_category, is_created = _get_or_create(
                    db_session,
                    models.Category,
                    name=category['name'],
                    tag=str(category['tag']).lower()
                )
                db_article.categories.append(db_category)
        db_query.articles.append(db_article)
    db_session.add(db_query)
    db_session.commit()
    return db_query


def get_queries(db_session: Session):
    return db_session.query(models.Query).order_by(desc('created_at')).all()


def get_query_with_details(db_session: Session, query_id: int):
    return db_session.query(models.Query).filter(models.Query.id == query_id).first()

# async def search_existing_query(query_input: schemas.QueryCreate, db_session: Session = Depends(database.get_db)):
#     return db_session.query(models.Query).filter(models.Query.content == query_input.content).first()


# async def register_query(query_input: schemas.QueryCreate, db_session: Session = Depends(database.get_db)):
#     db_query = models.Query(content=query_input.content)
#     db_session.add(db_query)
#     db_session.commit()
#     return db_query


#
#
# async def get_pizzas(db_session: Session):
#     """Select all records with relationships from database.
#
#     :param db_session: sqlalchemy.orm.session.Session instance
#     :return: models.Pizza[] a list records.
#     """
#     return db_session.query(models.Pizza).order_by(desc('created_at')).all()
#
#
# async def create_pizza(db_session: Session, pizza: schemas.PizzaBase):
#     """Store Pizza with ingredients or uses ingredient
#     configuration from database, if exist.
#
#     :param db_session: sqlalchemy.orm.session.Session instance
#     :param pizza: schemas.PizzaBase input data
#     :return: models.Pizza a single record after saving
#     """
#     db_pizza = models.Pizza(name=pizza.name, status=pizza.status)
#
#     for ingredient in pizza.ingredients:
#         # find next ingredient configuration in database
#         db_ingredient = db_session.query(models.Ingredient) \
#             .filter_by(name=ingredient.name, count=ingredient.count).first()
#         if not db_ingredient:
#             # create new ingredient configuration if not exist
#             db_ingredient = models.Ingredient(name=ingredient.name,
#                                               count=ingredient.count)
#         db_pizza.ingredients.append(db_ingredient)
#
#     db_session.add(db_pizza)
#     db_session.commit()
#     return db_pizza
#
#
# async def update_pizza_status(db_session: Session, pizza: schemas.PizzaBase):
#     """ Updating status for pizza
#
#     :param db_session: sqlalchemy.orm.session.Session instance
#     :param pizza: schemas.PizzaBase input data
#     :return: models.Pizza a single record after saving
#     """
#     db_pizza = db_session.query(models.Pizza) \
#         .filter(models.Pizza.id == pizza.id).first()
#     if db_pizza:
#         db_pizza.status = pizza.status
#         db_session.commit()
#         db_session.add(db_pizza)
#         db_session.refresh(db_pizza)
#         return db_pizza
#     raise NoResultFound("Entity is not found")
