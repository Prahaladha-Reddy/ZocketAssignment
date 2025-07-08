from dotenv import load_dotenv
load_dotenv()
serp=os.getenv("SERPER_API_KEY")
def search_results(query: list):
  answer=[]
  for q in query:
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
      "q": q,
      "num": 3
    })

    headers = {
      'X-API-KEY': serp,
      'Content-Type': 'application/json'
    }

    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data)
    organic=data['organic']
    for i in organic:
      answer.append({q:(i['link'])})
  return answer


def page_extractor(url):
  conn = http.client.HTTPSConnection("scrape.serper.dev")
  payload = json.dumps({
    "url": url,
    "includeMarkdown": True
  })
  headers = {
    'X-API-KEY': serp,
    'Content-Type': 'application/json'
  }
  conn.request("POST", "/", payload, headers)
  res = conn.getresponse()
  data = res.read()
  data=json.loads(data)
  return data

def llm_respond_for_link(queries,link):
  data=page_extractor(link)
  llm_result=llm.invoke(query_prompt.format(question=queries, website=data['text']))
  return llm_result.content