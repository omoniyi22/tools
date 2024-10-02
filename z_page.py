import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

FILE = 2

INPUT = f"lastsave{FILE}.txt"
OUTPUT = f"outputer{FILE}.txt"
LAST_SAVED_FILE = f"lastsaved{FILE}.txt"


def save_last_saved_id(coin_id):
    # Save the current ID to the file
    with open(LAST_SAVED_FILE, "w") as file:
        file.write(str(coin_id))


def extract_hrefs(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    hrefs = []
    # Find all <a> tags
    for a_tag in soup.find_all("a"):
        href = a_tag.get("href")
        if href and "discord" in href:  # Check if 'href' contains "discord"
            hrefs.append(href)
    return hrefs


# Using Playwright
with sync_playwright() as p:
    # Launch Chromium in headless mode
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Open input file with the coin IDs
    with open(INPUT, "r", encoding="utf-8") as infile:
        for line in infile:
            coin_id = line.strip()
            url = coin_id
            print(url)
            try:
                page.goto(url)
            except Exception as e:
                print(e)
            # time.sleep(1)  # You can adjust this based on load times

            try:
                # Find the description section using XPath
                description_section = page.query_selector(
                    ".jsx-1559142571.relevant-urls"
                )
                print(description_section)

                if description_section:
                    # Get the inner HTML of the description section
                    body_content = description_section.inner_html()

                    # Extract Discord hrefs from the content
                    hrefs = extract_hrefs(body_content)

                    # Save extracted hrefs to the output file
                    with open(OUTPUT, "a", encoding="utf-8") as outfile:
                        for href in hrefs:
                            outfile.write(href + "\n")

                    print(f"Extracted and saved {len(hrefs)} hrefs from {coin_id}.")
                else:
                    print(f"No description found for coin ID {coin_id}.")

                # Save the last processed coin ID
                save_last_saved_id(coin_id)

            except Exception as e:
                print(f"An error occurred with coin ID {coin_id}: {e}")

    # Close the browser
    browser.close()
