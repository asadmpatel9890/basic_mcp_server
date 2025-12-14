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

# Load environment variables from .env file
load_dotenv()

# Set up Groq API key from environment variables
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

# Configuration for MCP servers
# This defines the GitHub repository server that will be used to interact with GitHub API
SERVERS = { 
    "git_repo": {
        "transport": "stdio",  # Communication method with the server
        "command": "python",   # Command to run the server
        "args": [
            "server.py"        # Python script that implements the GitHub MCP server
       ]
    }
}

async def main():
    # Initialize the MCP client with the configured servers
    client = MultiServerMCPClient(SERVERS)
    
    # Retrieve all available tools from the connected MCP servers
    tools = await client.get_tools()

    # Create a dictionary mapping tool names to tool objects for easy access
    named_tools = {}
    for tool in tools:
        named_tools[tool.name] = tool

    # Display available tools for debugging/information purposes
    print("Available tools:", named_tools.keys())

    # Initialize Groq language model with Qwen model
    model = ChatGroq(model="qwen/qwen3-32b")

    # Create an agent that can use the available tools
    # The agent combines the language model with the MCP tools
    agent = create_agent(model,
                         tools,
                         system_prompt="You are a helpful assistant that can fetch GitHub repository information. Always provide clear, formatted responses.")

    # Invoke the agent with a user query about GitHub repositories
    response= await agent.ainvoke(
        {"messages":[{"role":"user","content":"Give me information campusx-official github repos"}]}
    )
 
    # Print the agent's response
    print("git response:", response['messages'][-1].content)

    # Alternative implementation using direct tool binding (commented out)
    # This approach directly binds tools to the LLM without using an agent framework
    
    # llm = ChatGroq(
    # model="openai/gpt-oss-120b",  
    # temperature=0.7,
    # max_tokens=1000
    # )

    # # Bind tools directly to the language model
    # llm_with_tools = llm.bind_tools(tools)

    # # Invoke the model with tools
    # reponse = llm_with_tools.invoke([
    #     HumanMessage(content="Give me information campusx-official github repo")
    # ])

    # print(reponse)

    # Another alternative implementation (also commented out)
    # Shows manual tool calling and response handling
    
    # llm = ChatGroq(model="gpt-5")
    # llm_with_tools = llm.bind_tools(tools)

    # prompt = "Draw a triangle rotating in place using the manim tool."
    # response = await llm_with_tools.ainvoke(prompt)

    # # Check if the model made any tool calls
    # if not getattr(response, "tool_calls", None):
    #     print("\nLLM Reply:", response.content)
    #     return

    # # Process each tool call made by the model
    # tool_messages = []
    # for tc in response.tool_calls:
    #     selected_tool = tc["name"]              # Get tool name
    #     selected_tool_args = tc.get("args") or {}  # Get tool arguments
    #     selected_tool_id = tc["id"]             # Get tool call ID
    
    #     # Execute the selected tool with the provided arguments
    #     result = await named_tools[selected_tool].ainvoke(selected_tool_args)
    #     # Create a tool message with the result
    #     tool_messages.append(ToolMessage(tool_call_id=selected_tool_id, content=json.dumps(result)))
        
    # # Get final response from the model after tool execution
    # final_response = await llm_with_tools.ainvoke([prompt, response, *tool_messages])
    # print(f"Final response: {final_response.content}")

# Entry point - run the async main function
if __name__ == '__main__':
    asyncio.run(main())
