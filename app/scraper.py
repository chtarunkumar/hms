# app/scraper.py

import requests
from bs4 import BeautifulSoup
import logging
import re
from flask import current_app # <--- ADD 'current_app' here

logger = logging.getLogger(__name__)

def scrape_hospital_info(url: str) -> dict:
    """
    Scrapes general information from a given hospital website URL.
    This is a generic example and might need adjustment for specific sites.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('title').get_text(strip=True) if soup.find('title') else "N/A"
        description_meta = soup.find('meta', attrs={'name': 'description'})
        description = description_meta['content'].strip() if description_meta else "N/A"

        # Example: Try to find contact info (very generic, might not work for all sites)
        contact_info = []
        for tag in soup.find_all(text=re.compile(r'(\d{3}[-.\s]??\d{3}[-.\s]??\d{4}|\w+@\w+\.\w+)')):
            if tag.parent.name not in ['script', 'style']: # Avoid script/style tags
                 contact_info.append(tag.strip())
        contact_info = list(set(contact_info)) # Remove duplicates

        # Example: Find common headings that might indicate departments/services
        departments = []
        for h_tag in soup.find_all(['h2', 'h3', 'h4']):
            text = h_tag.get_text(strip=True)
            if any(keyword in text.lower() for keyword in ['department', 'service', 'specialty', 'clinic']):
                departments.append(text)
        departments = list(set(departments))

        info = {
            "url": url,
            "title": title,
            "description": description,
            "contact_details": contact_info,
            "potential_departments_services": departments,
            "scraped_at": current_app.config['CURRENT_DATETIME'] # 'current_app' is now available
        }
        logger.info(f"Successfully scraped hospital info from {url}")
        return info

    except requests.exceptions.RequestException as e:
        logger.error(f"Network or HTTP error while scraping {url}: {e}", exc_info=True)
        return {"error": f"Failed to fetch content from {url}: {e}"}
    except Exception as e:
        logger.error(f"General error while scraping {url}: {e}", exc_info=True)
        return {"error": f"An unexpected error occurred during scraping: {e}"}


def scrape_disease_info(disease_name: str) -> dict:
    """
    Scrapes information about a specific disease from a reliable source like Wikipedia.
    """
    search_url = f"https://en.wikipedia.org/wiki/{disease_name.replace(' ', '_')}"
    try:
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try to extract the first paragraph of the main content
        main_content = soup.find('div', class_='mw-parser-output')
        summary = "N/A"
        if main_content:
            first_paragraph = main_content.find('p', recursive=False) # Direct child paragraph
            if first_paragraph:
                summary = first_paragraph.get_text(strip=True)
            else: # Fallback to finding any paragraph
                paragraphs = main_content.find_all('p')
                if paragraphs:
                    summary = paragraphs[0].get_text(strip=True)

        # Find infobox data if available
        infobox = {}
        infobox_table = soup.find('table', class_='infobox')
        if infobox_table:
            for row in infobox_table.find_all('tr'):
                header = row.find('th')
                data = row.find('td')
                if header and data:
                    key = header.get_text(strip=True).replace(':', '').replace('.', '').replace(' ', '_').lower()
                    value = data.get_text(strip=True)
                    infobox[key] = value

        info = {
            "disease_name": disease_name,
            "source_url": search_url,
            "summary": summary,
            "infobox_data": infobox,
            "scraped_at": current_app.config['CURRENT_DATETIME'] # 'current_app' is now available
        }
        logger.info(f"Successfully scraped disease info for '{disease_name}' from Wikipedia.")
        return info

    except requests.exceptions.RequestException as e:
        logger.error(f"Network or HTTP error while scraping disease info for '{disease_name}': {e}", exc_info=True)
        return {"error": f"Failed to fetch content for disease '{disease_name}': {e}"}
    except Exception as e:
        logger.error(f"General error while scraping disease info for '{disease_name}': {e}", exc_info=True)
        return {"error": f"An unexpected error occurred during disease info scraping: {e}"}