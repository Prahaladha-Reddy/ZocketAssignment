from models import queries
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from prompts import query_genaration_prompt
from dotenv import load_dotenv
load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash")
structured_llm=llm.with_structured_output(queries)


def generate_questions(user_query:str, search_snippet:str):
  prompt=query_genaration_prompt.format(user_query=user_query, search_snippet=search_snippet)
  response=structured_llm.invoke(prompt)
  question_list=[query.query for query in response.queries]
  return question_list
