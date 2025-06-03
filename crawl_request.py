from pathlib import Path
import json
import os
import requests
import urllib.parse

crawlbase_api_url = 'https://api.crawlbase.com?token={0}&callback=true&crawler={1}&url={2}&autoparse=true' # store=true

crawlbase_token = "<Normal or JavaScript requests token>"
crawlbase_crawler = "<Crawler name>"

urls = open('urls.txt', 'r').readlines()

for url in urls:
  url = url.strip()
  encoded_url = urllib.parse.quote(url, safe='')
  api_url = crawlbase_api_url.format(crawlbase_token, crawlbase_crawler, encoded_url)

  print(f'Requesting to crawl {url}')

  try:
    response = requests.get(api_url)
    json_response = json.loads(response.text)
    crawlbase_rid = json_response['rid']

    # `data` directory
    data_dir = os.path.join(Path.cwd(), 'data')
    Path(data_dir).mkdir(parents=True, exist_ok=True)

    # `data/<rid>` directory
    rid_dir = os.path.join(data_dir, crawlbase_rid)
    Path(rid_dir).mkdir(parents=True, exist_ok=True)
    
  except Exception as e:
    print(f"An error occured while crawling {url}\n{e}")

print('Done sending crawl requests.')
