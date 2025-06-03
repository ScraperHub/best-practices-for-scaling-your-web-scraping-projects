from pathlib import Path
import json
import os
import requests
import urllib.parse

CRAWLBASE_TOKEN = "<Normal or Javascript requests token>"
CRAWLBASE_CRAWLER_NAME = "<Crawler name>"

REQUEST_SECURITY_ID = '8e1c3efb29fcc59d3c61f86960ccc9f5'

CRAWLBASE_CRAWLING_API_URL = "https://api.crawlbase.com?token={0}&url={1}&crawler={2}&callback=true&callback_headers={3}"

def crawl(url, use_storage = False):
    url = url.strip()
    encoded_url = urllib.parse.quote(url, safe="")
    encoded_crawlbase_crawler_name = urllib.parse.quote(CRAWLBASE_CRAWLER_NAME, safe="")
    encoded_callback_headers = urllib.parse.quote(f"MY-ID:{REQUEST_SECURITY_ID}", safe="")
    
    api_url = CRAWLBASE_CRAWLING_API_URL.format(CRAWLBASE_TOKEN, encoded_url, encoded_crawlbase_crawler_name, encoded_callback_headers)

    try:
        response = requests.get(api_url)
        json_response = json.loads(response.text)
        crawlbase_rid = json_response["rid"]

        data_dir = os.path.join(Path.cwd(), "data")
        Path(data_dir).mkdir(parents=True, exist_ok=True)

        rid_dir = os.path.join(data_dir, crawlbase_rid)
        Path(rid_dir).mkdir(parents=True, exist_ok=True)

        print(f"- Crawl request for '{url}' was sent successfully.")
        
    except Exception as e:
        print(f"- Error encountered while processing '{url}':\n{e}")


if __name__ == "__main__":

    urls = [
        "http://httpbin.org/",
        "https://github.com/crawlbase"
    ]

    for url in urls:
        crawl(url, use_storage=True)
