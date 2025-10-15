from fastmcp import FastMCP
import requests
import os

# Create MCP server
app = FastMCP("Salesforce MCP")

@app.tool()
def ping() -> str:
    """Simple health check."""
    return "pong"

@app.tool()
def sf_query(soql: str, access_token: str, instance_url: str):
    """
    Query Salesforce using provided access token & instance URL.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{instance_url}/services/data/v62.0/query"
    params = {"q": soql}
    r = requests.get(url, headers=headers, params=params, timeout=30)
    try:
        return r.json()
    except Exception:
        return {"status_code": r.status_code, "text": r.text}

if __name__ == "__main__":
    # Render provides the port via the PORT env variable
    port = int(os.getenv("PORT", 10000))
    app.run("http", host="0.0.0.0", port=port)
