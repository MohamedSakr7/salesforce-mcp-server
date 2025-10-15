from fastmcp import FastMCP
from fastapi import FastAPI
import requests
import os
import uvicorn

# Create the MCP instance
mcp = FastMCP("Salesforce MCP")

# MCP tools
@mcp.tool
def ping() -> str:
    """Simple health check"""
    return "pong"

@mcp.tool
def sf_query(soql: str, access_token: str, instance_url: str):
    """Run a Salesforce SOQL query"""
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{instance_url}/services/data/v62.0/query"
    r = requests.get(url, headers=headers, params={"q": soql}, timeout=30)
    try:
        return r.json()
    except Exception:
        return {"status_code": r.status_code, "text": r.text}

# FastAPI app (manual mounting for FastMCP 2.12.x)
app = FastAPI(title="Salesforce MCP")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ping")
def ping_route():
    return {"result": ping()}

@app.post("/sf_query")
def sf_query_route(soql: str, access_token: str, instance_url: str):
    return {"result": sf_query(soql, access_token, instance_url)}

# Render entry point
if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
