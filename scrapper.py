from bs4 import BeautifulSoup
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
import os
import sys

# Set up the proxy URL with authentication
PROXY_URL = 'https://brd-customer-hl_8582d4e0-zone-ai_scrapper:7m1k0yur6fc7@brd.superproxy.io:9515'

def scrape_website(website):
    """
    Scrapes the specified website using Selenium through a remote proxy connection.
    :param website: The URL of the website to scrape.
    :return: The HTML content of the website as a string.
    """
    print("Launching Chrome Browser...") 
    
    # Set up the remote proxy connection
    try:
        sbr_connection = ChromiumRemoteConnection(PROXY_URL, 'goog', 'chrome')  
        options = ChromeOptions()

        with Remote(sbr_connection, options=options) as driver: 
            print('Connected! Navigating to the website...')  
            driver.get(website)

            # Handle CAPTCHA if present
            try:
                solve_res = driver.execute('executeCdpCommand', {
                    'cmd': 'Captcha.waitForSolve',
                    'params': {'detectTimeout': 10000},
                })
                print("CAPTCHA Solve Status:", solve_res['value']['status']) 
            except Exception as e:
                print("CAPTCHA handling error:", e)

            page_source = driver.page_source  # Get the HTML source of the page
            print(page_source) 
            return page_source

    except Exception as e:
        print(f"An error occurred while scraping: {e}") 
        return None  # Return None in case of an error

def extract_body_content(html_content):
    """
    Extracts the body content from the HTML.
    :param html_content: The raw HTML of the webpage.
    :return: The body content as a string.
    """
    if not html_content:  # Check if html_content is None
        print("No HTML content found!")  # Print an error message
        return ""  # Return an empty string to prevent further errors
    
    soup = BeautifulSoup(html_content, "html.parser")  
    body_content = soup.body  
    return str(body_content) if body_content else ""

def clean_body_content(body_content):
    """
    Cleans the extracted body content by removing JavaScript, CSS, and other unnecessary elements.
    """
    soup = BeautifulSoup(body_content, "html.parser")  
    for script_or_style in soup(["script", "style"]): 
        script_or_style.extract()  
    
    cleaned_content = soup.get_text(separator="\n")  
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content  

def split_dom_content(dom_content, max_length=6000):
    """
    Splits the DOM content into chunks of a specified maximum length.
    """
    return [dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)]  

# Example usage
if __name__ == "__main__":
    url = "http://example.com"  # Replace with the target URL
    html_content = scrape_website(url)  # Scrape the website and get the HTML content

    if html_content:  # Check if HTML content was successfully scraped
        print(f"HTML Content Length: {len(html_content)}")  # Output the length for debugging
        body_content = extract_body_content(html_content)  # Extract the body content
        cleaned_content = clean_body_content(body_content)  # Clean the body content
        print(cleaned_content)  # Output the cleaned content
    else:
        print("Failed to retrieve HTML content.")  # Notify if scraping failed
