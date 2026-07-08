from mcp.server.fastmcp import FastMCP
import json
import os

FLIGHTS_PATH = os.path.join(os.path.dirname(__file__), "flights.json")

mcp = FastMCP(name="Airport Info")

def _load_flights():
    with open(FLIGHTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f).get("flights", [])

@mcp.resource("flights://today")
def flights_resource():
    with open(FLIGHTS_PATH, "r", encoding="utf-8") as f:
        return f.read()

@mcp.tool()
def search_by_number(flight_number: str) -> dict:
    for flight in _load_flights():
        if flight.get("flight_number") == flight_number:
            return flight
    return {"error": "Flight not found"}

@mcp.tool()
def filter_by_destination(destination: str) -> list:
    query = destination.lower()
    return [
        flight for flight in _load_flights()
        if flight.get("arrival", "").lower() == query
        or flight.get("arrival_city", "").lower() == query
    ]

@mcp.tool()
def filter_by_status(status: str) -> list:
    query = status.lower()
    return [flight for flight in _load_flights() if flight.get("status", "").lower() == query]

@mcp.tool()
def flights_after(hour: int) -> list:
    result = []
    for flight in _load_flights():
        departure_time = flight.get("departure_time", "00:00")
        departure_hour = int(departure_time.split(":")[0])
        if departure_hour > hour:
            result.append(flight)
    return result

if __name__ == "__main__":
    mcp.run(transport="stdio")
