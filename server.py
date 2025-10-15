from fastmcp import FastMCP
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import uvicorn

# ---------------------------------------------------------
# Create MCP
# ---------------------------------------------------------
mcp = FastMCP("Salesforce MCP")

# ---------------------------------------------------------
# Define logic functions
# ---------------------------------------------------------
def ping_logic() -> str:
    """Simple health check"""
    return "pong"

def sf_query_logic(soql: str, access_token: str, instance_url: str):
    """Run a Salesforce SOQL query"""
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{instance_url}/services/data/v62.0/query"
    r = requests.get(url, headers=headers, params={"q": soql}, timeout=30)
    try:
        return r.json()
    except Exception:
        return {"status_code": r.status_code, "text": r.text}

# ---------------------------------------------------------
# Register functions as tools (positional arguments only)
# ---------------------------------------------------------
mcp.add_tool("ping", "Simple health check", ping_logic)
mcp.add_tool("sf_query", "Run a Salesforce SOQL query", sf_query_logic)

# ---------------------------------------------------------
# FastAPI app setup
# ---------------------------------------------------------
app = FastAPI(title="Salesforce MCP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Endpoints
# ---------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.options("/ping")
def ping_options():
    return {}

@app.post("/ping")
def ping_route():
    return {"result": ping_logic()}

@app.options("/sf_query")
def sf_query_options():
    return {}

@app.post("/sf_query")
async def sf_query_route(request: Request):
    data = await request.json()
    soql = data.get("soql")
    access_token = data.get("access_token")
    instance_url = data.get("instance_url")
    return {"result": sf_query_logic(soql, access_token, instance_url)}

# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
