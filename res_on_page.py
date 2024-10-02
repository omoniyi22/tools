import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

FILE = 6
POSITION = ""
INPUT = f"id{FILE}.txt"
OUTPUT = f"href{FILE}.txt"
LAST_SAVED_FILE = f"lastsaved{FILE}.txt"

def save_last_saved_id(coin_id):
    # Save the current ID to the file
    with open(LAST_SAVED_FILE, "w") as file:
        file.write(str(coin_id))

def extract_and_save_hrefs(links_next):
    # Check if links_next is not None
    if links_next:
        # Find all <a> tags within links_next
        a_tags = links_next.find_all("a")
        # Open the output file to save hrefs
        with open(OUTPUT, "a", encoding="utf-8") as file:
            for a_tag in a_tags:
                href = a_tag.get("href")
                if href and "discord" in href:  # Check if 'href' contains "discord"
                    file.write(href + "\n")  # Save the href to the file
                    print(f"Saved: {href}")

def check_json(response):
    if "https://www.bitdegree.org/cryptocurrency-prices" in response.url:
        try:
            # Get the response body
            data_body = response.body()

            # Convert bytes to string if necessary
            if isinstance(data_body, bytes):
                data_body = data_body.decode("utf-8")

            # Parse with BeautifulSoup
            soup = BeautifulSoup(data_body, "html.parser")
            # Find the content of elements with class '.links-section.mt-3'
            links_section_content = soup.select_one(".links-section.mt-3")
            
            # Get the next sibling div
            links_next = links_section_content.find_next_sibling("div")
            
            # Call the function to extract and save hrefs
            extract_and_save_hrefs(links_next)
            save_last_saved_id(POSITION)
            

        except KeyError as e:
            print(f"KeyError: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Using Playwright
with sync_playwright() as p:
    # Launch Chromium in headless mode
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.on("response", check_json)

    # Open input file with the coin IDs
    with open(INPUT, "r", encoding="utf-8") as infile:
        for line in infile:
            coin_id = line.strip()
            POSITION = coin_id
            url = f"https://www.bitdegree.org/cryptocurrency-prices/{coin_id}"
            page.goto(url)
            page.wait_for_load_state("load")
            # time.sleep(1)  # You can adjust this based on load times
    # Close the browser
    browser.close()
