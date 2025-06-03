from pathlib import Path
import json
import os
import requests
import threading
import time
import urllib.parse

CRAWLBASE_TOKEN = "<Normal or Javascript requests token>"
CRAWLBASE_CRAWLER_NAME = "<Crawler name>"

REQUEST_SECURITY_ID = '8e1c3efb29fcc59d3c61f86960ccc9f5'

CRAWLBASE_CRAWLING_API_URL = "https://api.crawlbase.com?token={0}&url={1}&crawler={2}&callback=true&callback_headers={3}"

BATCH_SIZE = 100
DELAY_SECONDS = 1

def retry_operation(operation, max_retries=3, delay=2):
    for attempt in range(1, max_retries + 1):
        try:
            return operation()
        except Exception as e:
            print(f"- Error encountered on retry attempt '{attempt}':\n{e}")

        if attempt < max_retries:
            print(f"- Retrying in {delay} seconds...")
            time.sleep(delay)

    raise Exception("Max retries exceeded.")

def crawl(url):
    url = url.strip()
    encoded_url = urllib.parse.quote(url, safe="")
    encoded_crawlbase_crawler_name = urllib.parse.quote(CRAWLBASE_CRAWLER_NAME, safe="")
    encoded_callback_headers = urllib.parse.quote(f"MY-ID:{REQUEST_SECURITY_ID}", safe="")
    
    api_url = CRAWLBASE_CRAWLING_API_URL.format(CRAWLBASE_TOKEN, encoded_url, encoded_crawlbase_crawler_name, encoded_callback_headers)

    try:
        def perform_request():
            response = requests.get(api_url)
            response.raise_for_status()
            return response

        response = retry_operation(lambda: perform_request())
        json_response = json.loads(response.text)
        crawlbase_rid = json_response["rid"]

        data_dir = os.path.join(Path.cwd(), "data")
        Path(data_dir).mkdir(parents=True, exist_ok=True)

        rid_dir = os.path.join(data_dir, crawlbase_rid)
        Path(rid_dir).mkdir(parents=True, exist_ok=True)

        print(f"- Crawl request for '{url}' was sent successfully.")
        
    except Exception as e:
        print(f"- Error encountered while processing '{url}':\n{e}")

def batch_crawl(urls):
    threads = []

    for url in urls:
        t = threading.Thread(target=crawl, args=(url,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

def crawl_urls(urls):
    for i in range(0, len(urls), BATCH_SIZE):
        batched_urls = urls[i:i + BATCH_SIZE]
        print(batched_urls)
        batch_crawl(batched_urls)
        time.sleep(DELAY_SECONDS)


if __name__ == "__main__":

    urls = [
        "http://httpbin.org/",
        "https://github.com/crawlbase",
        "http://httpbin.org/ip",
        "http://httpbin.org/html",
    ]
    crawl_urls(urls)
