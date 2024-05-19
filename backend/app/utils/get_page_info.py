import re
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

# Extracts the URL from the given text by finding the first occurrence of 'http' or 'https'
# and returning the URL starting from that point until the next whitespace character
def extract_url(text):
    url = re.search(r'https?://[^\s]+', text)
    if url is not None:
        return url.group(0)
    return None

def get_webpage_title(url):
    try:

        mobile_emulation = {
            "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" 
            }

        # Set up the options for the Chrome browser
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')  # Run in headless mode, i.e., without a GUI
        # chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
        # chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        # To handle the website like a mobile device
        # chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
        
        # Create a new instance of the Chrome driver
        driver = webdriver.Chrome(options=chrome_options)
        
        # Visit the website
        driver.get(url)
        
        # Get the title of the webpage
        title = driver.title
        
        # Close the browser
        driver.quit()
        
        return title
    except WebDriverException as e:
        # Handle exceptions related to the WebDriver
        print("Error with WebDriver:", e)
        return None
    except Exception as e:
        # Handle any other exceptions that occur during the process
        print("Error:", e)
        return None

def generate_screenshot(url, screenshot_name):
    # Set up the options for the Chrome browser
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # Run in headless mode, i.e., without a GUI
    chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
    chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)
    
    # Visit the website
    driver.get(url)
    
    # Take a screenshot of the page
    driver.save_screenshot(screenshot_name)
    
    # Close the browser
    driver.quit()

import socket
import ssl

def get_dns(url):
    try:
        # Extract the hostname from the URL
        hostname = url.split("//")[-1].split("/")[0].split(":")[0]
        
        # Get the DNS information
        dns_info = socket.gethostbyname(hostname)
        
        return dns_info
    except socket.gaierror as e:
        # Handle the case where the hostname cannot be resolved
        print("Error resolving hostname:", e)
        return None

def get_url_certificate(url):
    try:
        # Extract the hostname from the URL
        hostname = url.split("//")[-1].split("/")[0].split(":")[0]
        
        # Get the certificate information
        cert_info = ssl.get_server_certificate((hostname, 443))
        
        return cert_info
    except Exception as e:
        # Handle any exceptions that occur during the process
        print("Error getting certificate information:", e)
        return None
    
def get_dns_and_certificate(url):
    if url is None:
        return None
    dns = get_dns(url)
    cert_info = get_url_certificate(url)
    info = {
        "url": url,
        "dns": dns,
        "certificate": cert_info
    }
    return info