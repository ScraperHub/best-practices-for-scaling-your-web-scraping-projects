# Best Practices for Scaling Your Web Scraping Projects in 2025

We invite you to explore our [blog](https://crawlbase.com/blog/best-practices-for-scaling-your-web-scraping-projects/) for more details.

## Setting Up Your Coding Environment

Before building your Amazon proxy unblocker, you'll need to set up a basic Python environment. Here's how to get started:

1. [Install Python 3](https://kinsta.com/knowledgebase/install-python/#how-to-install-python) on your computer
2. Run `python -m pip install -r requirements.txt`
3. To make our webhook publicly accessible by Crawlbase servers for demonstration purposes, we need to [install and configure ngrok](https://ngrok.com/docs/getting-started/).

## Obtaining API Credentials

1. Create an account at [Crawlbase](https://crawlbase.com/signup) and log in.
2. After registration, you will receive 5,000 free requests.
3. Locate and copy your Crawling API [Normal or Javascript requests token](https://crawlbase.com/dashboard/account/docs).
4. [Create a new Crawler](https://crawlbase.com/dashboard/crawler/new).

## Running the Example Scripts

Before running the examples, ensure that you replace all instances of the following placeholders:

1. `<Normal or Javascript requests token>` - Replace this with your [Crawling API requests token](https://crawlbase.com/dashboard/account/docs).
2. `<Crawler name>` - Replace this with the name of your newly created crawler. You can create or view it [here](https://crawlbase.com/dashboard/crawler/crawlers).

### Example Scripts

1. Start the ngrok tunnel:

```bash
ngrok http 5768
```

2. Set the callback URL:Set the callback URL:

Copy the forwarding URL provided by ngrok and paste it into the **Callback URL** field of your [Crawler settings](https://crawlbase.com/dashboard/crawler/crawlers).
Example:
`https://xxxx-xxx-xxx-xxx-xx.ngrok-free.app/webhook`

3. Run the Webhook HTTP server:

```bash
python webhook_http_server.py
```

4. Send a crawl request (in a separate terminal):

```bash
python crawl.py
```
---

Copyright 2025 Crawlbase
