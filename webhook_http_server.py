from flask import Flask
from flask import request
from pathlib import Path
import gzip
import json
import os
import threading

REQUEST_SECURITY_ID = '8e1c3efb29fcc59d3c61f86960ccc9f5'

app = Flask("webhook_http_server")

def handle_webhook_request(request_content):
    crawlbase_rid = request_content[0]
    requested_url = request_content[1]
    original_status = request_content[2]
    crawlbase_status = request_content[3]
    content_encoding = request_content[4]
    body = request_content[5]

    if content_encoding == "gzip":
        try:
            body = gzip.decompress(body)
        except Exception:
            pass

    try:
        data_dir = os.path.join(Path.cwd(), "data")
        if not os.path.isdir(data_dir):
            Path(data_dir).mkdir(parents=True, exist_ok=True)

        rid_dir = os.path.join(data_dir, crawlbase_rid)
        if not os.path.isdir(rid_dir):
            Path(rid_dir).mkdir(parents=True, exist_ok=True)

        meta = {"rid": crawlbase_rid, "requested_url": requested_url, "original_status": original_status, "crawlbase_status": crawlbase_status}
        meta_file = os.path.join(rid_dir, f"{crawlbase_rid}.meta.json")
        with open(meta_file, "w") as f:
            pretty_json = json.dumps(meta, indent=2)
            f.write(pretty_json)

        body_file = os.path.join(rid_dir, crawlbase_rid)
        with open(body_file, "wb") as f:
            f.write(body)

        print(f"- Successfully processed RID {crawlbase_rid}. Output saved to '{rid_dir}'.")
    except Exception as e:
        print(f"- Error encountered while processing {crawlbase_rid}:\n{e}")

@app.route("/webhook", methods=["POST"])
def webhook():
    if 'Original-Status' not in request.headers or 'PC-Status' not in request.headers or 'rid' not in request.headers:
        return ("", 404)

    crawlbase_rid = request.headers.get("rid")

    if crawlbase_rid == "dummyrequest":
        print("- Dummy request received from Crawlbase.")
        return ("", 204)
    
    if request.headers.get("My-Id") != REQUEST_SECURITY_ID:
        return ("", 404)

    request_content = (
        crawlbase_rid, 
        request.headers.get("url"), 
        request.headers.get("Original-Status"), 
        request.headers.get("PC-Status"), 
        request.headers.get("Content-Encoding"), 
        request.data
    )

    thread = threading.Thread(target=handle_webhook_request, args=(request_content,))
    thread.start()

    return ("", 204)


if __name__ == "__main__":

    from waitress import serve
    host = "0.0.0.0"
    port = 5768
    print(f"\n\n- Webhook HTTP server is running at {host}:{port}.\n\n")
    serve(app, host=host, port=port)
