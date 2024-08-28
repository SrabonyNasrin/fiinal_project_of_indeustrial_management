from pydantic import BaseModel
from typing import List, Optional


# Reporter Schemas
class ReporterBase(BaseModel):
    name: str

class ReporterCreate(ReporterBase):
    pass

class Reporter(ReporterBase):
    id: int

    class Config:
        from_attributes  = True


# Category Schemas
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes  = True


# News Schemas
class NewsBase(BaseModel):
    title: str
    body: str
    link: str
    date: str  # Consider using `datetime` if your date field is in ISO format
    reporter: Optional[Reporter] = None
    category: Optional[Category] = None

class NewsCreate(NewsBase):
    reporter_name: str
    category_name: str
    images: List[str] = []

class News(NewsBase):
    images: List["Image"] = []

    class Config:
        from_attributes  = True


# Image Schemas
class ImageBase(BaseModel):
    url: str

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int
    news_id: int

    class Config:
        from_attributes  = True

class NewsResponse(BaseModel):
    title: str
    body: str
    link: str
    date: str
    reporter: str

    class Config:
        from_attributes = True


class Response(BaseModel):
    message: str
    status: str
