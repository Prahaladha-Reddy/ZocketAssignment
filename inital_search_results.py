from dotenv import load_dotenv
import http.client
import json
import os
from models import queries
load_dotenv()
serp=os.getenv("SERPER_API_KEY")
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts import query_genaration_prompt , website_reader
from pydantic import BaseModel , Field
llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash")

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


def llm_for_question_gen(user_query:str, search_snippet:str):
  prompt=query_genaration_prompt.format(user_query=user_query, search_snippet=search_snippet)
  response=llm.with_structured_output(queries).invoke(prompt)
  question_list=[query.query for query in response.queries]
  return question_list

def llm_respond_for_link(queries,link):
    data=page_extractor(link)
    text = data.get('text')
    if not text:
        return f"No text found for link: {link}"
    llm_result=llm.invoke(website_reader.format(question=queries, website=text))
    return llm_result.content