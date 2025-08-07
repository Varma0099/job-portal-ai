from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from linkedin_gmail_prompt import linkedin_gmail_prompt
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Optional, Dict, Any, Callable
import asyncio
import json

cfg = RunnableConfig(recursion_limit=100)

def initialize_model(google_api_key: str) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=google_api_key
    )

async def setup_agent_with_tools(
    google_api_key: str,
    linkedin_pipedream_url: str,
    gmail_pipedream_url: str,
    progress_callback: Optional[Callable[[str], None]] = None
) -> Any:
    """
    Set up the agent with LinkedIn and Gmail tools.
    """
    try:
        if progress_callback:
            progress_callback("Setting up agent with tools... ✅")
        
        # Initialize tools configuration
        tools_config = {
            "linkedin": {
                "url": linkedin_pipedream_url,
                "transport": "streamable_http"
            },
            "gmail": {
                "url": gmail_pipedream_url,
                "transport": "streamable_http"
            }
        }

        if progress_callback:
            progress_callback("Added LinkedIn integration... ✅")

        if progress_callback:
            progress_callback("Added Gmail integration... ✅")

        if progress_callback:
            progress_callback("Initializing MCP client... ✅")
        # Initialize MCP client with configured tools
        mcp_client = MultiServerMCPClient(tools_config)
        
        if progress_callback:
            progress_callback("Getting available tools... ✅")
        # Get all tools
        tools = await mcp_client.get_tools()
        
        if progress_callback:
            progress_callback("Creating AI agent... ✅")
        # Create agent with initialized model
        mcp_orch_model = initialize_model(google_api_key)
        
        # Create a simple agent without langgraph
        class SimpleAgent:
            def _init_(self, model, tools):
                self.model = model
                self.tools = tools
            
            async def ainvoke(self, inputs, config=None):
                # Simple implementation without langgraph
                messages = inputs.get("messages", [])
                if messages:
                    last_message = messages[-1].content
                    
                    # Create detailed prompt
                    detailed_prompt = f"""
{last_message}

Please execute the requested actions using the available tools.
"""
                    
                    # Use the model to generate response
                    response = await self.model.ainvoke([HumanMessage(content=detailed_prompt)])
                    return {"messages": [response]}
                return {"messages": []}
        
        agent = SimpleAgent(mcp_orch_model, tools)
        
        if progress_callback:
            progress_callback("Setup complete! Starting to process your request... ✅")
        
        return agent
    except Exception as e:
        print(f"Error in setup_agent_with_tools: {str(e)}")
        raise

def run_agent_sync(
    google_api_key: str,
    linkedin_pipedream_url: str,
    gmail_pipedream_url: str,
    content_data: Dict[str, Any],
    progress_callback: Optional[Callable[[str], None]] = None
) -> dict:
    """
    Synchronous wrapper for running the agent.
    """
    async def _run():
        try:
            agent = await setup_agent_with_tools(
                google_api_key=google_api_key,
                linkedin_pipedream_url=linkedin_pipedream_url,
                gmail_pipedream_url=gmail_pipedream_url,
                progress_callback=progress_callback
            )
            
            # Prepare the prompt with content data
            action_type = content_data.get("action_type", "")
            linkedin_data = content_data.get("linkedin", {})
            email_data = content_data.get("email", {})
            
            # Create detailed prompt
            detailed_prompt = f"""
Action Type: {action_type}

LinkedIn Data:
- Content: {linkedin_data.get('content', '')}
- Hashtags: {linkedin_data.get('hashtags', '')}
- Visibility: {linkedin_data.get('visibility', 'Public')}

Email Data:
- Recipient: {email_data.get('recipient', '')}
- Subject: {email_data.get('subject', '')}
- Content: {email_data.get('content', '')}
- Priority: {email_data.get('priority', 'Normal')}

{linkedin_gmail_prompt}
"""
            
            if progress_callback:
                progress_callback("Processing your request...")
            
            # Run the agent
            result = await agent.ainvoke(
                {"messages": [HumanMessage(content=detailed_prompt)]},
                config=cfg
            )
            
            if progress_callback:
                progress_callback("Action completed successfully!")
            
            return result
        except Exception as e:
            print(f"Error in _run: {str(e)}")
            raise

    # Run in new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_run())
    finally:
        loop.close()