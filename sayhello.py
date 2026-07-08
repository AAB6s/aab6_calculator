from mcp.server.fastmcp import FastMCP

mcp = FastMCP("SayHelloServer")

@mcp.tool()
def say_hello() -> str:
    return "Hello World!"

if __name__ == "__main__":
    mcp.run()
