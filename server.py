from fastmcp import FastMCP
from fastapi import FastAPI
import requests, os, uvicorn

# ---- MCP server ----
mcp = FastMCP("Salesforce MCP")

@mcp.tool
def ping() -> str:
    """Simple health check."""
    return "pong"

@mcp.tool
def sf_query(soql: str, access_token: str, instance_url: str):
    """Run a Salesforce SOQL query using the provided token and org URL."""
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{instance_url}/services/data/v62.0/query"
    params = {"q": soql}
    r = requests.get(url, headers=headers, params=params, timeout=30)
    try:
        return r.json()
    except Exception:
        return {"status_code": r.status_code, "text": r.text}

# ---- FastAPI wrapper (for /health and serving HTTP) ----
# Create the MCP ASGI app (served at /mcp)
mcp_app = mcp.http_app(path="/mcp")

# IMPORTANT: pass MCP lifespan to FastAPI so sessions init correctly
fastapi_app = FastAPI(title="Salesforce MCP HTTP", lifespan=mcp_app.lifespan)

@fastapi_app.get("/health")
def health():
    return {"status": "ok"}

# Mount MCP under /mcp (so your MCP URL will be .../mcp)
fastapi_app.mount("/mcp", mcp_app)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    uvicorn.run(fastapi_app, host="0.0.0.0", port=port)
