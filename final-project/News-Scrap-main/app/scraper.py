import requests
from bs4 import BeautifulSoup,Comment
import re
from .crud import create_news
from .schemas import NewsCreate, News
from .database import SessionLocal
from contextlib import contextmanager

def single_news_scraper(url: str):
    try:
        # Get HTML content
        response = requests.get(url)
        html_content = response.text

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Extract the main news section
        news_section = soup.find('article')

        # Extract title
        news_title = news_section.find(class_='article-title').text if news_section.find(class_='article-title') else "No title found"

        # Extract body content
        news_body_paragraphs = news_section.find_all('p')
        news_body = "\n".join([paragraph.text for paragraph in news_body_paragraphs])

        # Extract images
        images = []
        image_sections = soup.find_all(class_='section-media')
        for im in image_sections:
            img_tag = im.find('img')
            if img_tag and 'data-srcset' in img_tag.attrs:
                images.append(img_tag['data-srcset'])  # Append URL directly

        # Extract related information (category, reporter, date)
        related_section = soup.find(class_='pane-content')

        # Extract category
        category = re.sub(r'^[^a-zA-Z]+', '', related_section.find(class_='author-name').text) if related_section.find(class_='author-name') else "No category found"

        # Extract reporter name
        reporter = re.sub(r'^[^a-zA-Z]+', '', related_section.find(class_='byline').text) if related_section.find(class_='byline') else "No reporter found"

        # Extract publication date
        news_date = re.sub(r'^[^a-zA-Z]+', '', related_section.find(class_='date').text) if related_section.find(class_='date') else "Not Found Date"

        # print(f"Scraped news from {url}")
        # print(f"Title: {news_title}")
        # print(f"Reporter: {reporter}")
        # print(f"Date: {news_date}")
        # print(f"Category: {category}")
        # print(f"body: {news_body}")
        # print(f"Images: {images}")

        # Return a populated NewsCreate schema object
        return NewsCreate(
            title=news_title,
            body=news_body,
            date=news_date,
            link=url,
            reporter_name=reporter,
            category_name=category , # This will be handled in the database
            images=images
        )

    except Exception as e:
        print(f"An error occurred: {e}")



@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()

def scrape_and_store_news(url: str):
    with get_db_session() as db:
        news_data = single_news_scraper(url)
        if news_data:
            inserted_news = create_news(db=db, news=news_data)
