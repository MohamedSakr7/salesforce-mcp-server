from fastmcp import FastMCP
import requests
import os

# Create the MCP app
app = FastMCP("Salesforce MCP")

# Simple test endpoint
@app.tool()
def ping() -> str:
    return "pong"

# Salesforce query tool
@app.tool()
def sf_query(soql: str, access_token: str, instance_url: str):
    """
    Query Salesforce using provided access token & instance URL.
    Lovable backend will supply these values via headers or parameters.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{instance_url}/services/data/v62.0/query"
    params = {"q": soql}
    r = requests.get(url, headers=headers, params=params, timeout=30)

    try:
        return r.json()
    except Exception:
        return {"status_code": r.status_code, "text": r.text}

# Run the app on Render
if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
