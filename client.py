import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import ToolMessage
import json
import os
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from langgraph.prebuilt import ToolNode

load_dotenv()

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
SERVERS = { 
    "git_repo": {
        "transport": "stdio",
        "command": "python",
        "args": [
            "server.py"
       ]
    }
}

async def main():
    
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()




    named_tools = {}
    for tool in tools:
        named_tools[tool.name] = tool

    print("Available tools:", named_tools.keys())

    model = ChatGroq(model="qwen/qwen3-32b")

    agent = create_agent(model,
                         tools,
                         system_prompt="You are a helpful assistant that can fetch GitHub repository information. Always provide clear, formatted responses.")


    response= await agent.ainvoke(
        {"messages":[{"role":"user","content":"Give me information campusx-official github repos"}]}
    )
 
    print("git response:", response['messages'][-1].content)

    

    # llm = ChatGroq(
    # model="openai/gpt-oss-120b",  
    # temperature=0.7,
    # max_tokens=1000
    # )

    # llm_with_tools = llm.bind_tools(tools)

    # reponse = llm_with_tools.invoke([
    #     HumanMessage(content="Give me information campusx-official github repo")
    # ])

    # print(reponse)
    # llm = ChatGroq(model="gpt-5")
    # llm_with_tools = llm.bind_tools(tools)

    # prompt = "Draw a triangle rotating in place using the manim tool."
    # response = await llm_with_tools.ainvoke(prompt)

    # if not getattr(response, "tool_calls", None):
    #     print("\nLLM Reply:", response.content)
    #     return

    # tool_messages = []
    # for tc in response.tool_calls:
    #     selected_tool = tc["name"]
    #     selected_tool_args = tc.get("args") or {}
    #     selected_tool_id = tc["id"]

    #     result = await named_tools[selected_tool].ainvoke(selected_tool_args)
    #     tool_messages.append(ToolMessage(tool_call_id=selected_tool_id, content=json.dumps(result)))
        

    # final_response = await llm_with_tools.ainvoke([prompt, response, *tool_messages])
    # print(f"Final response: {final_response.content}")


if __name__ == '__main__':
    asyncio.run(main())