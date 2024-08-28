from sqlalchemy.orm import Session,joinedload
from . import models, schemas


def get_news(db: Session, news_id: int):
    return db.query(models.News).filter(models.News.id == news_id).first()

def get_news_list(db: Session, skip: int = 0, limit: int = 10):
    news = session.query(News).options(joinedload(News.reporter)).all()
    return schemas.NewsResponse.from_orm(news);

def get_image(db: Session, image_id: int):
    return db.query(models.Image).filter(models.Image.id == image_id).first()

def get_or_create_category(db: Session, name: str):
    category = db.query(models.Category).filter(models.Category.name == name).first()
    if category is None:
        category = models.Category(name=name)
        db.add(category)
        db.commit()
        db.refresh(category)
    return category

def get_or_create_reporter(db: Session, name: str):
    reporter = db.query(models.Reporter).filter(models.Reporter.name == name).first()
    if reporter is None:
        reporter = models.Reporter(name=name)
        db.add(reporter)
        db.commit()
        db.refresh(reporter)
    return reporter

def get_news_existance(db: Session, news_title: str):
    return db.query(models.News).filter(models.News.title == news_title).first()


def create_news(db: Session, news: schemas.NewsCreate):
    category = get_or_create_category(db, news.category_name)
    reporter = get_or_create_reporter(db, news.reporter_name)

    news_exist = get_news_existance(db, news_title=news.title)
    if news_exist:
        return news_exist

    db_news = models.News(
        title=news.title,
        body=news.body,
        date=news.date,
        link=news.link,
        reporter_id=reporter.id,
        category_id=category.id
    )
    db.add(db_news)
    db.commit()
    db.refresh(db_news)

    for image_url in news.images:
        create_image(db, news_id=db_news.id, url=image_url)

    return db_news

def create_image(db: Session, news_id: int, url: str):
    db_image = models.Image(news_id=news_id, url=url)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image
