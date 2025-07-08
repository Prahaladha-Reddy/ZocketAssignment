import imp
from langchain_google_genai import ChatGoogleGenerativeAI
from initial_extractor import *
from dotenv import load_dotenv
load_dotenv()
from prompts import query_prompt
from simplesearc import simple_search
from pydantic import BaseModel , Field
def initial_extractor(user_query:str):
  question_list=simple_search(user_query)
  answers=search_results(question_list)
  llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash")

actual_links = [
    {k:v}
    for d in answers
    for k, v in d.items()
    if "youtube" not in v
]

content=actual_links = [
    llm_respond_for_link(k,v)
    for d in actual_links
    for k, v in d.items()
]
