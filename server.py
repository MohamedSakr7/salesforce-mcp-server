from fastmcp import FastMCP
import requests

# Initialize FastMCP app
app = FastMCP("Salesforce MCP")

@app.tool()
def ping() -> str:
    """Simple health check."""
    return "pong"

@app.tool()
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

if __name__ == "__main__":
    # No host/port args in new FastMCP
    app.run("http")
