''''Importing requests and BeautifulSoup to scrape book titles from a webpage'''

from bs4 import BeautifulSoup
import requests

url = "https://www.who.int/health-topics/hospitals#tab=tab_1"

def scrape_hospital_news(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve webpage: Status code {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    news_items = soup.find_all('div', class_='list-view--item vertical-list-item')

    hospital_news = []
    for item in news_items:
        title_tag = item.find('a', class_='link-container')
        if title_tag:
            title = title_tag.get_text(strip=True)
            hospital_news.append(title.replace('\n', ' '))

    return hospital_news

if __name__ == "__main__":
    news = scrape_hospital_news(url)
    for idx, title in enumerate(news):
        print(f"{idx + 1}. {title}")
    