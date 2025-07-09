from fastapi import FastAPI
from pydantic import BaseModel
from main import researcher , analyze_slogan , add_rewriter
from models import State_add
app=FastAPI()

class Query(BaseModel):
    query: str

@app.post("/analyze")
def read_root(query: Query):
    return {"response": researcher(query.query)}


@app.post("/slogan_analyzer")
def read_root(query: Query):
    return {"response": analyze_slogan(query.query)}


@app.post("/add_rewriter")
def read_root(state: State_add):
    state=state.dict()
    return {"response": add_rewriter(state)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
