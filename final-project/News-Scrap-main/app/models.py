from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

class Reporter(Base):
    __tablename__ = "reporters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)



class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    body = Column(Text)
    date = Column(String(255))
    link = Column(String(255))
    reporter_id = Column(Integer, ForeignKey("reporters.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    reporter = relationship("Reporter")
    category = relationship("Category")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255))
    news_id = Column(Integer, ForeignKey("news.id"))

    news = relationship("News")
