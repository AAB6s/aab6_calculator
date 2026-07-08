import requests
from fastmcp import FastMCP

BASE_URL = "https://openlibrary.org"
mcp = FastMCP("OpenLibrary Assistant")

@mcp.tool()
def search_books(query: str) -> list:
    r = requests.get(f"{BASE_URL}/search.json", params={"q": query}, timeout=10)
    if r.status_code != 200:
        return {"error": f"API Error {r.status_code}"}
    d = r.json().get("docs", [])[:10]
    return [
        {
            "title": b.get("title"),
            "author": b.get("author_name", ["Unknown"])[0],
            "year": b.get("first_publish_year"),
            "work_id": b.get("key")
        }
        for b in d
    ]

@mcp.tool()
def get_book_details(work_id: str) -> dict:
    if not work_id.startswith("/works/"):
        work_id = f"/works/{work_id}"
    r = requests.get(f"{BASE_URL}{work_id}.json", timeout=10)
    if r.status_code == 404:
        return {"error": "Book not found"}
    if r.status_code != 200:
        return {"error": f"API Error {r.status_code}"}
    return r.json()

if __name__ == "__main__":
    mcp.run(transport="stdio")