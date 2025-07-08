import http.client
import json
from dotenv import load_dotenv
load_dotenv()
import os
from dotenv import load_dotenv
import http.client
import json
import os
load_dotenv()
serp=os.getenv("SERPER_API_KEY")
def simple_search(query):
  conn = http.client.HTTPSConnection("google.serper.dev")
  payload = json.dumps({
    "q": query,
    "num": 5
  })
  headers = {
    'X-API-KEY': serp,
    'Content-Type': 'application/json'
  }
  conn.request("POST", "/search", payload, headers)
  res = conn.getresponse()
  data = res.read()
  data=json.loads(data)
  return data



def single_search(query):
  conn = http.client.HTTPSConnection("google.serper.dev")
  payload = json.dumps({
    "q": query,
    "num": 1
  })
  headers = {
    'X-API-KEY': serp,
    'Content-Type': 'application/json'
  }
  conn.request("POST", "/search", payload, headers)
  res = conn.getresponse()
  data = res.read()
  data=json.loads(data)
  return data