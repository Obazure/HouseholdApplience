from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, validator

from utils import generate_hash


class QueryBase(BaseModel):
    query: str
    query_hash: str = ''

    @validator('query', pre=True, always=True)
    def query_not_empty(cls, val):
        if not val:
            raise ValueError('content must contain a value')
        return val

    @validator('query_hash', pre=True, always=True)
    def query_hash_generate(cls, val, values):
        if val:
            return val
        return generate_hash(values['query'])


class QueryList(QueryBase):
    id: int
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    @validator('created_at', pre=True, always=True)
    def default_created_at(cls, val):
        return val or datetime.now()

    @validator('updated_at', pre=True, always=True)
    def default_updated_at(cls, val, values):
        return val or values['created_at']

    class Config:
        orm_mode = True


class QueryRead(QueryList):
    articles: List['ArticleRead'] = []


class Query(QueryRead):
    articles: List['Article'] = []


class QueryWrite(QueryBase):
    articles: List['ArticleWrite'] = []


class ArticleBase(BaseModel):
    source_url: str
    source_url_hash: str = ''
    source_tag: str
    published_at: datetime
    title: str
    read_url: str
    content: str

    @validator('source_url', pre=True, always=True)
    def source_url_not_empty(cls, val):
        if not val:
            raise ValueError('source_url must contain a value')
        return val

    @validator('source_tag', pre=True, always=True)
    def source_tag_not_empty(cls, val):
        if not val:
            raise ValueError('source_tag must contain a value')
        return val

    @validator('source_url_hash', pre=True, always=True)
    def source_url_hash_generate(cls, val, values):
        if val:
            return val
        return generate_hash(values['source_url'])

    @validator('published_at', pre=True, always=True)
    def published_at_not_empty(cls, val):
        if not val:
            raise ValueError('published_at must contain a value')
        return val

    @validator('title', pre=True, always=True)
    def title_not_empty(cls, val):
        if not val:
            raise ValueError('title must contain a value')
        return val

    @validator('read_url', pre=True, always=True)
    def read_url_not_empty(cls, val):
        if not val:
            raise ValueError('read_url must contain a value')
        return val

    @validator('content', pre=True, always=True)
    def content_not_empty(cls, val):
        if not val:
            raise ValueError('content must contain a value')
        return val


class ArticleRead(ArticleBase):
    id: int
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    categories: List['CategoryRead'] = []
    result: Optional[Any] = None

    @validator('created_at', pre=True, always=True)
    def default_created_at(cls, val):
        return val or datetime.now()

    @validator('updated_at', pre=True, always=True)
    def default_updated_at(cls, val, values):
        return val or values['created_at']

    class Config:
        orm_mode = True


class Article(ArticleRead):
    queries: Optional[List['Query']] = []
    categories: List['Category'] = []


class ArticleWrite(ArticleBase):
    categories: Optional[List['CategoryWrite']] = []
    result: Optional[Any] = None


class CategoryBase(BaseModel):
    name: str
    tag: str

    @validator('name', pre=True, always=True)
    def name_not_empty(cls, val):
        if not val:
            raise ValueError('name must contain a value')
        return val

    @validator('tag', pre=True, always=True)
    def tag_not_empty(cls, val):
        if not val:
            raise ValueError('tag must contain a value')
        return val


class CategoryRead(CategoryBase):
    id: int
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    @validator('created_at', pre=True, always=True)
    def default_created_at(cls, val):
        return val or datetime.now()

    @validator('updated_at', pre=True, always=True)
    def default_updated_at(cls, val, values):
        return val or values['created_at']

    class Config:
        orm_mode = True


class Category(CategoryRead):
    articles: List['Article'] = []


class CategoryWrite(CategoryBase):
    pass


Query.update_forward_refs()
QueryRead.update_forward_refs()
QueryWrite.update_forward_refs()
Article.update_forward_refs()
ArticleRead.update_forward_refs()
ArticleWrite.update_forward_refs()
Category.update_forward_refs()
CategoryRead.update_forward_refs()
CategoryWrite.update_forward_refs()
