import re
import socket
import ssl
from playwright.async_api import async_playwright, TimeoutError
import asyncio
import base64
import os

# Extracts the URL from the given text by finding the first occurrence of 'http' or 'https'
# and returning the URL starting from that point until the next whitespace character
def extract_url(text):
    url = re.search(r'https?://[^\s]+', text)
    if url is not None:
        return url.group(0)
    return None

async def capture_page_info(url, screenshot_path='screenshot.png', device_name='Galaxy S5', wait_state='networkidle', headless=True, retry_count=3):
    if url is None:
        return None, None, None
    async with async_playwright() as playwright:
        device = playwright.devices[device_name]
        browser = await playwright.chromium.launch(headless=headless)
        context = await browser.new_context(**device)
        
        urls = []
        
        def handle_response(response):
            if response.url not in urls:
                urls.append(response.url)
        
        page = await context.new_page()
        page.on('response', handle_response)
        
        for attempt in range(retry_count):
            try:
                await page.goto(url)
                await page.wait_for_load_state(wait_state)
                break  # If successful, exit the loop
            except (TimeoutError, Exception) as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == retry_count - 1:
                    raise  # Raise the last exception if all retries fail
        
        title = await page.title()
        await page.screenshot(path=screenshot_path)
        await browser.close()
        screenshot = base64.b64encode(open(screenshot_path, "rb").read()).decode("utf-8")
        # now we delete the screenshot file
        os.remove(screenshot_path)
        
        return title, urls, screenshot 

def get_ip(url):
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
    
def get_ip_and_certificate(url):
    if url is None:
        return None
    dns = get_ip(url)
    cert_info = get_url_certificate(url)
    return dns, cert_info