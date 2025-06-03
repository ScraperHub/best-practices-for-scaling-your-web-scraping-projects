from flask import Flask
from flask import request
from pathlib import Path
import threading
import gzip
import json
import os
import logging

app_name = "webhook_http_server"

logger = logging.getLogger(app_name)
logging.basicConfig(filename=f"{app_name}.log", encoding='utf-8', level=logging.DEBUG)

app = Flask(app_name)

def handle_webhook_request(request_content):
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
    with open(meta_file, 'w') as f:
      pretty_json = json.dumps(meta, indent=2)
      f.write(pretty_json)

    # body
    body_file = os.path.join(rid_dir, crawlbase_rid)
    with open(body_file, 'wb') as f:
      f.write(body)

    logger.debug(f"{crawlbase_rid} processed")
  except Exception as e:
    error_message = f"An error occured for {crawlbase_rid}\n{e}"
    logger.error(error_message)

@app.route('/webhook', methods=['POST'])
def webhook():
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

  thread = threading.Thread(target=handle_webhook_request, args=(request_content,))
  thread.start()

  return ('', 204)


if __name__ == '__main__':
  
  from waitress import serve
  host = "0.0.0.0"
  port = 5768
  print(f"Webhook HTTP Server is running at {host}:{port}")
  serve(app, host=host, port=port)
