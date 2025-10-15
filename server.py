from fastmcp import FastMCP
from fastapi import FastAPI          # ✅ this import is crucial
import requests, os, uvicorn         # ✅ import uvicorn here too

# Initialize FastMCP app
app = FastMCP("Salesforce MCP")

@app.tool()
def ping() -> str:
    """Simple health check."""
    return "pong"

@app.tool()
def sf_query(soql: str, access_token: str, instance_url: str):
    """Query Salesforce using provided access token & instance URL."""
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{instance_url}/services/data/v62.0/query"
    params = {"q": soql}
    r = requests.get(url, headers=headers, params=params, timeout=30)
    try:
        return r.json()
    except Exception:
        return {"status_code": r.status_code, "text": r.text}

# ✅ Create a FastAPI app to handle /health and route MCP tools
fastapi_app = FastAPI()

@fastapi_app.get("/health")
def health():
    return {"status": "ok"}

# ✅ Mount FastMCP onto FastAPI
app.mount_to_fastapi(fastapi_app)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(fastapi_app, host="0.0.0.0", port=port)
