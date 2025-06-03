from flask import Flask
from flask import request
from pathlib import Path
import aiofiles
import gzip
import json
import os
import logging

app_name = "webhook_http_server"

logger = logging.getLogger(app_name)
logging.basicConfig(filename=f"{app_name}.log", encoding='utf-8', level=logging.DEBUG)

app = Flask(app_name)

async def handle_webhook_request(request_content):
  crawlbase_rid = request_content[0]
  requested_url = request_content[1]
  original_status = request_content[2]
  crawlbase_status = request_content[3]
  content_encoding = request_content[4]
  body = request_content[5]

  if content_encoding == 'gzip':
    try:
      body = gzip.decompress(body)
    except Exception:
      pass

  try:
    # `data` directory
    data_dir = os.path.join(Path.cwd(), 'data')
    if not os.path.isdir(data_dir):
      Path(data_dir).mkdir(parents=True, exist_ok=True)

    # `data/<rid>` directory
    rid_dir = os.path.join(data_dir, crawlbase_rid)
    if not os.path.isdir(rid_dir):
      Path(rid_dir).mkdir(parents=True, exist_ok=True)

    # meta.json
    meta = {'rid': crawlbase_rid, 'requested_url': requested_url, 'original_status': original_status, 'crawlbase_status': crawlbase_status}
    meta_file = os.path.join(rid_dir, f"{crawlbase_rid}.meta.json")
    async with aiofiles.open(meta_file, 'w') as f:
        pretty_json = json.dumps(meta, indent=2)
        await f.write(pretty_json)

    # body
    body_file = os.path.join(rid_dir, crawlbase_rid)
    async with aiofiles.open(body_file, 'wb') as f:
        await f.write(body)

    logger.debug(f"{crawlbase_rid} processed")
  except Exception as e:
    error_message = f"An error occured for {crawlbase_rid}\n{e}"
    logger.error(error_message)
    raise

@app.route('/webhook', methods=['POST'])
async def webhook():
  crawlbase_rid = request.headers.get('rid')
  if crawlbase_rid == "dummyrequest":
    logger.info("Dummy request from crawlbase received")
    return ('', 204)

  request_content = (
        crawlbase_rid, 
        request.headers.get('url'), 
        request.headers.get('Original-Status'), 
        request.headers.get('PC-Status'), 
        request.headers.get('Content-Encoding'), 
        request.data
    )

  try:
    await handle_webhook_request(request_content)
  except Exception as e:
    return ('', 500)

  return ('', 204)


if __name__ == '__main__':
  
  from waitress import serve
  host = "0.0.0.0"
  port = 5768
  print(f"Webhook HTTP Server is running at {host}:{port}")
  serve(app, host=host, port=port)
