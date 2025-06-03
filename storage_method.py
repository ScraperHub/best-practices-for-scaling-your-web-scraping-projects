import requests
import json

url = "https://api.crawlbase.com/storage/bulk?token=09h0ZtQuqMrEtZApzmTy4w"

payload = json.dumps({
  "rids": [
    "RID1",
    "RID2",
    "RID3"
  ],
  "auto_delete": True
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
