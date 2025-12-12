from mcp.server.fastmcp import FastMCP
import os
import json

FLIGHTS_PATH = os.path.join(os.path.dirname(__file__), "flights.json")

mcp = FastMCP(name="Aéroport Info")

def _load_flights():
    with open(FLIGHTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f).get("flights", [])

@mcp.resource("flights://today")
def flights_resource():
    with open(FLIGHTS_PATH, "r", encoding="utf-8") as f:
        return f.read()

@mcp.tool()
def search_by_number(flight_number: str) -> dict:
    flights = _load_flights()
    for f in flights:
        if f.get("number") == flight_number:
            return f
    return {"error": "Flight not found"}

@mcp.tool()
def filter_by_destination(destination: str) -> list:
    flights = _load_flights()
    return [f for f in flights if f.get("destination", "").lower() == destination.lower()]

@mcp.tool()
def filter_by_status(status: str) -> list:
    flights = _load_flights()
    return [f for f in flights if f.get("status", "").lower() == status.lower()]

@mcp.tool()
def flights_after(hour: int) -> list:
    flights = _load_flights()
    result = []
    for f in flights:
        time_str = f.get("time", "00:00")
        flight_hour = int(time_str.split(":")[0])
        if flight_hour > hour:
            result.append(f)
    return result

if __name__ == "__main__":
    mcp.run(transport="stdio") 