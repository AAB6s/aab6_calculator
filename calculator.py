from fastmcp import FastMCP
import math

mcp = FastMCP(name="Calculator-MCP")

@mcp.tool()
def add(a: float, b: float) -> float:
    return a + b

@mcp.tool()
def subtract(a: float, b: float) -> float:
    return a - b

@mcp.tool()
def multiply(a: float, b: float) -> float:
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

@mcp.tool()
def power(a: float, b: float) -> float:
    return a ** b

@mcp.tool()
def sqrt(x: float) -> float:
    if x < 0:
        raise ValueError("Negative value")
    return math.sqrt(x)

if __name__ == "__main__":
    mcp.run(transport="http")