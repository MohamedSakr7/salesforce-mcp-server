from fastmcp import FastMCP
from fastapi import FastAPI
import requests
import os

# Create the MCP instance
mcp = FastMCP("Salesforce MCP")

# Define tools
@mcp.tool
def ping() -> str:
    """Simple health check."""
    return "pong"

@mcp.tool
def sf_query(soql: str, access_token: str, instance_url: str):
    """Run a Salesforce SOQL query."""
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{instance_url}/services/data/v62.0/query"
    params = {"q": soql}
    r = requests.get(url, headers=headers, params=params, timeout=30)
    try:
        return r.json()
    except Exception:
        return {"status_code": r.status_code, "text": r.text}

# Create FastAPI app and mount MCP routes
app = FastAPI(title="Salesforce MCP")
mcp.mount_to_fastapi(app)

# For Render deployment
if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
