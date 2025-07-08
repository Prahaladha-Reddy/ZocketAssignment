from fastapi import FastAPI
from pydantic import BaseModel
from main import researcher

app=FastAPI()

class Query(BaseModel):
    query: str

@app.post("/analyze")
def read_root(query: Query):
    return {"response": researcher(query.query)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
