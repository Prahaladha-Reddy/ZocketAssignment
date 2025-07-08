from simplesearc import simple_search
from inital_search_results import *
from inital_search_results import llm_respond_for_link,llm_for_question_gen

def initial_question_list(query):
  question=[]
  results=simple_search(query)
  links=[link["link"] for  link in results['organic']]
  for link in links:
    inital_extracted_data=page_extractor(link)
    question_list=llm_for_question_gen(query,inital_extracted_data['text'])
    for q in question_list:
      question.append(q)
  return question
