from dotenv import load_dotenv
load_dotenv()
import os
from pydantic import BaseModel , Field
from typing import Literal
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
class State(BaseModel):
    initial_ad: str = Field(description="The original ad")
    tone: str = Field(description="The tone of the ad")
    platform: str = Field(description="The platform for the ad")
    polished_ad: str = Field(description="The polished ad")
    is_ok: bool = Field(description="Whether the ad is ok")
    feed_back: str = Field(description="The feedback for the ad")


class reviw_feedback(BaseModel):
  review:bool=Field(description="Whether the ad is good or not")


add_writer_prompt="""
You are a professional ad writer.
You are given an ad and you need to write a new ad for the same product.
The ad should be in the same tone as the original ad.
The ad should be in the same platform as the original ad.
The ad should be in the same tone as the original ad.
You should be very creative and unique in your writing.


Here is the original ad:
{initial_ad}

You might also have some feedback for the ad.
{feedback}
"""

review_prompt="""
You are a professional ad reviewer.
You are given an ad and you need to review it.
You need to check if the ad is well-written and suitable for the platform and tone.
If you it is good then return True else return False. remember only return True or False.

Here is the ad:
{polished_ad}

The tone of the ad is {tone} and the platform is {platform}.
"""

feedback_prompt="""
You are a professional ad reviewer.
You are given an ad and you need to review it.
You need to check if the ad is well-written and suitable for the platform and tone.
You need to provide actionable feedback to improve the ad.
You need to provide feedback in the same tone as the original ad.
You need to provide feedback in the same platform as the original ad.

Here is the ad:
{polished_ad}

"""



llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash",api_key=os.getenv("GOOGLE_API_KEY"))


class State(BaseModel):
    initial_ad: str = Field(description="The original ad")
    tone: str = Field(description="The tone of the ad")
    platform: str = Field(description="The platform for the ad")
    polished_ad: str = Field(description="The polished ad")
    is_ok: bool = Field(description="Whether the ad is ok")
    feed_back: str = Field(description="The feedback for the ad")


def polish_node(state):
    text = state["polished_ad"] if state["polished_ad"] else state["initial_ad"]
    feedback = state["feed_back"] or ""
    prompt=add_writer_prompt.format(initial_ad=text,feedback=feedback)
    polished = llm.invoke(prompt)
    state["polished_ad"] = polished.content
    return state

def review_node(state):
    polished = state["polished_ad"]
    prompt=review_prompt.format(polished_ad=polished,tone=state["tone"],platform=state["platform"])
    llm_new=llm.with_structured_output(reviw_feedback)
    is_ok = llm_new.invoke(prompt).review
    state["is_ok"] = is_ok
    return state

def feedback_node(state):
    polished = state["polished_ad"]
    prompt=feedback_prompt.format(polished_ad=polished)
    feedback = llm.invoke(prompt).content
    state["feed_back"] = feedback
    return state

def build_graph():
    graph = StateGraph(dict)
    graph.add_node("polish", polish_node)
    graph.add_node("review", review_node)
    graph.add_node("feedback", feedback_node)

    # Edges
    graph.add_edge("polish", "review")
    graph.add_conditional_edges(
        "review",
        lambda state: "end" if state["is_ok"] else "feedback",
        {"end": END, "feedback": "feedback"}
    )
    graph.add_edge("feedback", "polish")

    graph.set_entry_point("polish")
    return graph.compile()
