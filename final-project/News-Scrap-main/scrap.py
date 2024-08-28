import requests
from bs4 import BeautifulSoup,Comment
import re

BASE_URL="https://www.thedailystar.net"

# def single_news_scraper(url:str):
#     try:
#         # print(url)
#         response = requests.get(url)
#         html_content = response.text
#         # print(html_content)

#         # Parse the HTML content using BeautifulSoup
#         soup = BeautifulSoup(html_content, "html.parser")
        
#         news_section = soup.find('article')
        
#         news_title = news_section.find(class_='article-title')
#         news_body_paragraph = news_section.find_all('p')
#         news_body = ""

#         print("Title : ",news_title.text)
#         for paragraph in news_body_paragraph:
#             news_body += paragraph.text
#             news_body += "\n"
#         print(news_body)


#         # Find all sections with class 'section-media'
#         images = soup.find_all(class_='section-media')

#         # Extract and print all image URLs
#         for im in images:
#             # Look for img tags within the section
#             img_tag = im.find('img')
#             if img_tag and 'data-srcset' in img_tag.attrs:
#                 img_link = img_tag['data-srcset']
#                 print("Image URL =>", img_link)

#         related_section = soup.find(class_='pane-content')
        
#         category = re.sub(r'^[^a-zA-Z]+', '', related_section.find(class_='author-name').text)
#         print("Category : ",category)

#         reporter = re.sub(r'^[^a-zA-Z]+', '', related_section.find(class_='byline').text)
#         print("Reporter : ",reporter)

#         news_date = re.sub(r'^[^a-zA-Z]+', '', related_section.find(class_='date').text)
#         print("News Date : ",news_date)

#     except Exception as e:
#         print(f"An error occurred: {e}")

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
                images.append({"url": img_tag['data-srcset']})

        # Extract related information (category, reporter, date)
        related_section = soup.find(class_='pane-content')

        # Extract category
        category = re.sub(r'^[^a-zA-Z]+', '', related_section.find(class_='author-name').text) if related_section.find(class_='author-name') else "No category found"

        # Extract reporter name
        reporter = re.sub(r'^[^a-zA-Z]+', '', related_section.find(class_='byline').text) if related_section.find(class_='byline') else "No reporter found"

        # Extract publication date
        news_date = re.sub(r'^[^a-zA-Z]+', '', related_section.find(class_='date').text) if related_section.find(class_='date') else "Not Found Date"

        print(f"Scraped news from {url}")
        print(f"Title: {news_title}")
        print(f"Reporter: {reporter}")
        print(f"Date: {news_date}")
        print(f"Category: {category}")
        print(f"body: {new}")
        print(f"Images: {images}")

        # Return a populated NewsCreate schema object
        return NewsCreate(
            title=news_title,
            body=news_body,
            date=news_date,
            link=url,
            reporter_id=reporter,  # This will be handled in the database
            category_id=category,  # This will be handled in the database
            images=images,
        )

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # URL of the webpage you want to scrape
    url = BASE_URL+"/news/bangladesh"

    # Send a GET request to fetch the raw HTML content
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all h1 to h6 tags with class "title"
    headers = soup.find_all(['h2','h3','h4','h5','h6'], class_="title")

    # Print the text content of each matching header
    for header in headers:
        single_news_scraper(BASE_URL+header.a.attrs['href'])
