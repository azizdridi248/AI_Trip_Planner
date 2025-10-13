from fastapi import FastAPI
from pydantic import BaseModel
import os
from agent.agent_workflow import GraphBuilder
app = FastAPI()

class QueryRequest(BaseModel):
    query: str
@app.post("/query")
async def query_travel_agent(q:QueryRequest) :
    try :
        graph =GraphBuilder(model_provider="groq")
        react_app = graph()
        png_graph =react_app.get_graph().draw_mermaid_png()
        with open("graph.png","wb") as f:
            f.write(png_graph)
        print(f"Graph saved as graph.png in {os.getcwd()}")
        response = react_app.invoke({"messages": [q.query]})
        if isinstance(response, dict) and "messages" in response:
            return {"response": response["messages"][-1].content}
        else:
            return {"response": "Unexpected response format from the agent."}
    except Exception as e:
        return {"error": str(e)}