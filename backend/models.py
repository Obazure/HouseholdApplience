from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Table, UniqueConstraint, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

pivot_article_category = Table('article_category', Base.metadata,
                               Column('category_id', Integer, ForeignKey('categories.id')),
                               Column('article_id', Integer, ForeignKey('articles.id')),
                               )

pivot_query_article = Table('query_article', Base.metadata,
                            Column('query_id', Integer, ForeignKey('queries.id')),
                            Column('article_id', Integer, ForeignKey('articles.id')),
                            )


class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    query = Column(Text)
    query_hash = Column(String(255))

    articles = relationship('Article', secondary=pivot_query_article)

    __table_args__ = (
        UniqueConstraint('query_hash', name='_unique_query'),
    )


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    source_url = Column(String(2048))
    source_url_hash = Column(String(255))
    source_tag = Column(String(255))

    published_at = Column(DateTime, default=None, nullable=True)
    title = Column(String(1024))
    read_url = Column(String(2048))
    content = Column(Text)
    result = Column(JSON)

    queries = relationship('Query', secondary=pivot_query_article)
    categories = relationship('Category', secondary=pivot_article_category)

    __table_args__ = (
        UniqueConstraint('source_url_hash', name='_unique_article'),
    )


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    name = Column(String(255))
    tag = Column(String(255))

    articles = relationship('Article', secondary=pivot_article_category)

    __table_args__ = (
        UniqueConstraint('name', 'tag', name='_unique_category'),
    )
