from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
llm   = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)  

def slogan_analyzer_agant(df,queries):
    agent = create_pandas_dataframe_agent(llm, df,agent_type="openai-tools" ,verbose=True,allow_dangerous_code=True)
    result=agent.run(queries)
    return result
