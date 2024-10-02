import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

FILE = 1

INPUT = f"id{FILE}.txt"
OUTPUT = f"href{FILE}.txt"
LAST_SAVED_FILE = f"lastsaved{FILE}.txt"

def save_last_saved_id(coin_id):
    with open(LAST_SAVED_FILE, "w") as file:
        file.write(str(coin_id))

def extract_slugs(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    slugs = []
    
    # Find all <script> tags and extract JSON data
    for script in soup.find_all("script"):
        if script.string:
            try:
                # Attempt to parse the JSON data
                json_data = json.loads(script.string)
                
                # If the JSON structure is known, extract the slug
                # Adjust the path according to the actual JSON structure
                if 'slug' in json_data:
                    slugs.append(json_data['slug'])
                # You can add more checks if the slug is nested in other objects
            except json.JSONDecodeError:
                continue  # Skip if it's not valid JSON
                
    return slugs

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # with open(INPUT, "r", encoding="utf-8") as infile:
    for i in range(30):
        # coin_id = line.strip()
        # url = coin_id
        # page.goto(url)
        page.goto(f"https://api.pro.opensea.io/collections?offset={i *50}&limit=50&fields%5BcreatedDate%5D=1&fields%5BcreatedAt%5D=1&fields%5Bname%5D=1&fields%5Baddress%5D=1&fields%5Baddresses%5D=1&fields%5BimageUrl%5D=1&fields%5BisVerified%5D=1&fields%5Bslug%5D=1&fields%5Bstats.floor_price%5D=1&fields%5Bstats.items_listed%5D=1&fields%5Bstats.num_owners%5D=1&fields%5Bstats.total_supply%5D=1&fields%5Bstats.total_change%5D=1&fields%5Bstats.total_difference%5D=1&fields%5Bstats.total_sales%5D=1&fields%5Bstats.total_sales_change%5D=1&fields%5Bstats.total_volume%5D=1&fields%5Bstats.rolling_total_change%5D=1&fields%5Bstats.rolling_total_sales%5D=1&fields%5Bstats.rolling_total_sales_change%5D=1&fields%5Bstats.rolling_total_volume%5D=1&fields%5Bstats.top_offer_price%5D=1&fields%5Bstats.floor_price_token_price%5D=1&fields%5Bstats.floor_price_token_address%5D=1&fields%5Bstats.floor_price_token_decimals%5D=1&fields%5Bstats.floor_price_token_symbol%5D=1&fields%5BchainName%5D=1&sort%5Bstats.total_volume%5D=-1&filters%5BchainNames%5D%5B%5D=ethereum&filters%5BchainNames%5D%5B%5D=polygon&filters%5Btrending.top_total%5D=true")
        page.wait_for_load_state("load")

        try:
            # Get the full page content
            body_content = page.content()
            
            # Extract slugs from the JSON content
            # slugs = extract_slugs(body_content)
            
            # Save extracted slugs to the output file
            with open(OUTPUT, "a", encoding="utf-8") as outfile:
                # for slug in slugs:
                outfile.write(body_content + "\n")
            
            print(f"Extracted and saved {body_content} slugs from {i}.")
            save_last_saved_id(i)

        except Exception as e:
            print(f"An error occurred with coin ID {i}: {e}")
    
    browser.close()
