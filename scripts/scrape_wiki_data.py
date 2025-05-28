import sys
import os
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import Gundam

app = create_app()

WIKI_BASE_URL = "https://wiki.biligame.com/gundam/"
REQUEST_DELAY_SECONDS = 2 # Be respectful to the server

def sanitize_gundam_name_for_url(name):
    """Removes spaces and other problematic characters for URL construction."""
    return quote(name.replace(" ", ""))

def extract_tech_param(soup, param_name):
    """
    Extracts a specific technical parameter from the first table in the soup.
    Looks for a <th> containing param_name and returns the text of the next <td>.
    """
    try:
        # Find the "技术参数" headline span
        tech_param_headline = soup.find('span', class_='mw-headline', id='技术参数')
        if not tech_param_headline:
            print(f"    - Headline <span class='mw-headline' id='技术参数'> not found.")
            return None

        # Find the first table with class 'wikitable' that appears after this headline
        main_table = tech_param_headline.find_next('table', class_='wikitable')
        
        if not main_table:
            print(f"    - No <table class='wikitable'> found after '技术参数' headline.")
            return None
        
        # Now, proceed with extracting th/td from the correctly identified main_table
        th_elements = main_table.find_all('th')
        for th in th_elements:
            if param_name in th.get_text(strip=True):
                td = th.find_next_sibling('td')
                if td:
                    return td.get_text(strip=True)
                else:
                    print(f"    - Found <th> for '{param_name}' but no corresponding <td>.")
                    return None
        print(f"    - Technical parameter '{param_name}' not found in table headers.")
        return None
    except Exception as e:
        print(f"    - Error extracting tech param '{param_name}': {e}")
        return None

def extract_description(soup):
    """Extracts the description from the <p class="wiki-bot"> element."""
    try:
        head_img_box_element = soup.find('div', class_='headImg-box')
        if head_img_box_element:
            wiki_bot_p = head_img_box_element.find('p', class_='wiki-bot')
            if wiki_bot_p:
                # Extract all text content, including from child tags like <a>
                return ''.join(wiki_bot_p.find_all(string=True, recursive=True)).strip()
        print("    - Description <p class=\"wiki-bot\"> not found within <div class=\"headImg-box\">.")
        return None
    except Exception as e:
        print(f"    - Error extracting description: {e}")
        return None

def scrape_and_update_gundam(gundam_name):
    """Scrapes data for a single Gundam and updates the database."""
    print(f"Processing: {gundam_name}")
    
    gundam_record = Gundam.query.filter_by(name=gundam_name).first()
    if not gundam_record:
        print(f"  - Gundam '{gundam_name}' not found in database. Skipping.")
        return False

    wiki_page_name = sanitize_gundam_name_for_url(gundam_name)
    url = f"{WIKI_BASE_URL}{wiki_page_name}"
    print(f"  - Fetching data from: {url}")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"  - Error fetching URL {url}: {e}")
        return False

    soup = BeautifulSoup(response.content, 'html.parser')

    # Scrape required attributes
    print("  - Scraping technical parameters...")
    size = extract_tech_param(soup, "尺寸")
    base_weight = extract_tech_param(soup, "本体重量")
    full_weight = extract_tech_param(soup, "全备重量")
    engine_power = extract_tech_param(soup, "发动机功率") # or "出力" or "动力装置" depending on wiki consistency
    thrust = extract_tech_param(soup, "推进力") # or "总推力"
    acceleration = extract_tech_param(soup, "加速度")
    
    print("  - Scraping description...")
    description = extract_description(soup)

    # Update database record
    updated = False
    if size:
        gundam_record.size = size
        updated = True
        print(f"    - Size: {size}")
    if base_weight:
        gundam_record.base_weight = base_weight
        updated = True
        print(f"    - Base Weight: {base_weight}")
    if full_weight:
        gundam_record.full_weight = full_weight
        updated = True
        print(f"    - Full Weight: {full_weight}")
    if engine_power:
        gundam_record.engine_power = engine_power
        updated = True
        print(f"    - Engine Power: {engine_power}")
    if thrust:
        gundam_record.thrust = thrust
        updated = True
        print(f"    - Thrust: {thrust}")
    if acceleration:
        gundam_record.acceleration = acceleration
        updated = True
        print(f"    - Acceleration: {acceleration}")
    
    if description:
        # 只更新详细描述，不覆盖简介
        gundam_record.description = description 
        updated = True
        print(f"    - Detailed description updated (length: {len(description)} chars).")
        print(f"    - Brief intro preserved: {gundam_record.brief_intro[:50] if gundam_record.brief_intro else 'None'}...")
    else:
        print(f"    - No new detailed description found/extracted.")


    if updated:
        try:
            db.session.commit()
            print(f"  - Successfully updated '{gundam_name}' in database.")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"  - Error updating database for '{gundam_name}': {e}")
            return False
    else:
        print(f"  - No new data found/extracted to update for '{gundam_name}'.")
        return False


def main():
    with app.app_context():
        gundams_to_scrape = Gundam.query.with_entities(Gundam.name).all()
        gundam_names = [g[0] for g in gundams_to_scrape]
        
        if not gundam_names:
            print("No Gundam names found in the database to scrape.")
            return

        print(f"Found {len(gundam_names)} Gundams to process.")
        
        successful_updates = 0
        failed_updates = 0

        for i, name in enumerate(gundam_names):
            if scrape_and_update_gundam(name):
                successful_updates += 1
            else:
                failed_updates += 1
            
            # Respectful delay between requests
            if i < len(gundam_names) - 1: # Don't sleep after the last item
                print(f"  - Waiting {REQUEST_DELAY_SECONDS} seconds before next request...")
                time.sleep(REQUEST_DELAY_SECONDS)
        
        print("\nScraping complete.")
        print(f"Successfully updated: {successful_updates}")
        print(f"Failed/No updates: {failed_updates}")

if __name__ == "__main__":
    main() 