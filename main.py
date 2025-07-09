from prompts import final_prompt
from initaian_question_list import initial_question_list
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
from final_extraction import final_process
from slogan_analysisagant import slogan_analyzer_agant
import pandas as pd
import requests
df=pd.read_csv("slogan_genarator/brand_slogans.csv")
from add_rewriter import build_graph

def researcher(query):
  url = "https://deep-research-gxlm.onrender.com/generate_report/"
  payload = {
      "topic": query
  }
  response = requests.post(url, json=payload)
  return response


def analyze_slogan(query):
  result=slogan_analyzer_agant(df,query)
  return result

def add_rewriter(state):
  graph = build_graph()
  final_state = graph.invoke(state)
  return final_state["polished_ad"]







