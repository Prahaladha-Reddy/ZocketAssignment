from prompts import final_prompt
from initaian_question_list import initial_question_list
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
from final_extraction import final_process

def researcher(query):
  questions=initial_question_list(query)
  print("initial queries finished")
  content=final_process(questions)
  print("final content finished")
  total_content=" ".join(content)
  response=llm.invoke(final_prompt.format(content=total_content,question=query))
  return response