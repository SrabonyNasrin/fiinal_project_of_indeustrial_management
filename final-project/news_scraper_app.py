import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://www.thedailystar.net"

# Function to scrape a single news article
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

        # Return all information
        return {
            "title": news_title,
            "body": news_body,
            "date": news_date,
            "reporter": reporter,
            "category": category,
            "images": images,
        }

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Main function to run the Streamlit app
def main():
    st.title("News Scraper and Summarizer")
    
    # URL of the webpage to scrape
    url = BASE_URL + "/news/bangladesh"

    # Send a GET request to fetch the raw HTML content
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all h1 to h6 tags with class "title"
    headers = soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6'], class_="title")

    # Prepare a dictionary to hold news title and their corresponding URLs
    news_options = {header.text.strip(): BASE_URL + header.a.attrs['href'] for header in headers}

    # Streamlit dropdown to select a news title
    selected_news_title = st.selectbox("Select a news title", list(news_options.keys()))

    # If a title is selected, display its details
    if selected_news_title:
        news_url = news_options[selected_news_title]
        news_details = single_news_scraper(news_url)

        if news_details:
            st.subheader(news_details['title'])
            st.write(f"**Date:** {news_details['date']}")
            st.write(f"**Reporter:** {news_details['reporter']}")
            st.write(f"**Category:** {news_details['category']}")
            st.write("**News Body:**")
            st.write(news_details['body'])

            # Summarize the news body (using a simple placeholder summarization method)
            st.write("**Summary:**")
            st.write(news_details['body'][:150] + "...")  # Simple summary for demonstration

            # Display images if available
            if news_details['images']:
                st.write("**Images:**")
                for img in news_details['images']:
                    st.image(img['url'])

if __name__ == "__main__":
    main()
