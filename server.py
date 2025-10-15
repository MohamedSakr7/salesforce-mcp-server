from fastmcp import FastMCP, tool
import requests, os

app = FastMCP()

@tool()
def ping():
    return "pong"

@tool()
def sf_query(soql: str, access_token: str, instance_url: str):
    """
    Query Salesforce using provided access token & instance URL.
    Lovable backend will supply these values via headers.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{instance_url}/services/data/v62.0/query"
    params = {"q": soql}
    r = requests.get(url, headers=headers, params=params)
    return r.json()

if __name__ == "__main__":
    # FastMCP automatically exposes /mcp and /health endpoints
    app.run()
