from typing import List

import nltk
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
import uvicorn

import config
import crud
import models
import schemas
import database
from modules import media_providers, analysis
from utils import generate_hash

models.Base.metadata.create_all(bind=database.engine)

nltk.download('punkt', download_dir=config.NLTK_DATA_PATH)
nltk.download('stopwords', download_dir=config.NLTK_DATA_PATH)
nltk.download('wordnet', download_dir=config.NLTK_DATA_PATH)

app = FastAPI(
    title='MediaSource',
    docs_url="/api/docs",
    openapi_url="/api"
)

origins = [
    "https//localhost",
    "http://localhost:3000",
    "http://localhost:8080",
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


@app.post('/api/queries/', response_model=schemas.QueryRead)
async def make_query_request(query_input: schemas.QueryWrite, db_session: Session = Depends(get_db)):
    try:
        db_query = crud.get(db_session, models.Query, query=query_input.query, query_hash=query_input.query_hash)
        if not db_query:

            media_provider = media_providers.MediaProviderManager(query_input.query)
            query_processed = media_provider.process_query()

            query_processed['query_hash'] = query_input.query_hash
            for idx, article in enumerate(query_processed['articles']):
                article['source_url_hash'] = generate_hash(article['source_url'])
                result = analysis.simple_article_analysis(article['content'])
                query_processed['articles'][idx]['result'] = result

            db_query = crud.save_query_with_details(db_session, query_processed)
        return db_query
    except (HTTPException, NoResultFound, ValueError) as error:
        raise HTTPException(status_code=404, detail=error.detail) from error


@app.get('/api/queries/', response_model=List[schemas.QueryList])
async def get_query_details(db_session: Session = Depends(get_db)):
    db_queries = crud.get_queries(db_session)
    if db_queries is None:
        raise HTTPException(status_code=404, detail="Query in history not found.")
    return db_queries


@app.get('/api/queries/{id}/', response_model=schemas.Query)
async def get_query_details(query_id: int, db_session: Session = Depends(get_db)):
    db_query = crud.get_query_with_details(db_session, query_id)
    if db_query is None:
        raise HTTPException(status_code=404, detail="Query in history not found.")
    return db_query


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=config.BACKEND_PORT)
