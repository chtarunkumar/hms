from bs4 import BeautifulSoup
import requests

url = "https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"

def scrape_book_titles(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    book_elements = soup.select('article.product_pod h3 a')
    book_titles = [book['title'] for book in book_elements]
    return book_titles

printed_titles = scrape_book_titles(url)
for title in printed_titles:
    print(title)