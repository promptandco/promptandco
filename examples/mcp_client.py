"""Minimal Prompt & Co. MCP client using only the Python standard library.

    python mcp_client.py "hotel check-in deposit"

Set PROMPTANDCO_TOKEN to an agent token (free: register_agent) for full history; without it you get the free preview.
"""
import json
import os
import sys
import urllib.request

URL = "https://promptandco.com/mcp"


def rpc(method, params=None, request_id=1):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "User-Agent": "promptandco-example-client/1.0",
    }
    token = os.environ.get("PROMPTANDCO_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = json.dumps({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params or {}}).encode()
    with urllib.request.urlopen(urllib.request.Request(URL, data=body, headers=headers), timeout=30) as response:
        return json.load(response)


def main():
    query = " ".join(sys.argv[1:]) or "check-in"
    init = rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                              "clientInfo": {"name": "example", "version": "1.0"}})
    print("Connected to", init["result"]["serverInfo"]["title"])
    tools = rpc("tools/list", request_id=2)["result"]["tools"]
    print("Tools:", ", ".join(t["name"] for t in tools))
    result = rpc("tools/call", {"name": "search_experiences", "arguments": {"query": query}}, request_id=3)["result"]
    found = result["structuredContent"]
    print(f"{found.get('matches_available', 0)} match(es) for {query!r}; showing {len(found.get('results', []))} ({found.get('access')})")
    for item in found.get("results", []):
        print(f"- #{item['id']} [{item['entity_id']}] {item['title']}")


if __name__ == "__main__":
    main()
