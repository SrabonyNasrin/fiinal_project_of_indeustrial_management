from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, dependencies, scraper
import requests
from bs4 import BeautifulSoup

BASE_URL="https://www.thedailystar.net"

router = APIRouter(
    prefix="/news",
    tags=["news"],
)

@router.post("/scrape", response_model=schemas.Response)
def scrape_news():
    # URL of the webpage you want to scrape
    url = BASE_URL+"/news/bangladesh"

    # Send a GET request to fetch the raw HTML content
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    all_inserted_news = []

    # Find all h1 to h6 tags with class "title"
    headers = soup.find_all(['h2','h3','h4','h5','h6'], class_="title")

    # Print the text content of each matching header
    for header in headers:
        scraper.scrape_and_store_news(BASE_URL+header.a.attrs['href'])

    result = {
        "message": f"Successfully scraped news from {BASE_URL}",
        "status": "success"
    }
    return schemas.Response(**result)