import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "uv",
                "args": ["run", "/code/udemy/mcp-crash-course/servers/math_server.py"],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            },
        }
    )
    tools = await client.get_tools()

    agent = create_agent(
        model="gpt-4.1-mini",
        tools=tools,
        system_prompt="You are a helpful assistant.",
    )
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in tokyo?"}]}
    )
    # response = await agent.ainvoke(
    #     {"messages": [{"role": "user", "content": "what is 2 + 2?"}]}
    # )
    print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
