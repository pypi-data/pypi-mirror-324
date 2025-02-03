from flask import Flask, jsonify, request
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from Communist import Agent,Browser, BrowserConfig
from Communist.agent.views import FireflinkNLP
import asyncio
from Communist import BrowserConfig
from Communist.browser.context import BrowserContext,BrowserContextConfig
# Basic configuration



# Initialize Flask app
app = Flask(__name__)

# Async function to handle the agent's task
async def run_agent():
    context = BrowserContext(browser=Browser(BrowserConfig(headless=True)))
    token = "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"
    agent = Agent(
        task=""" verify user is able to login into www.fireflink.com with username diwahar.r@fireflink.com and password as Password@123 and check if any text is thier as zero code and automation for verification""",
        use_vision=False,
        llm=ChatOpenAI(model="gpt-4o-mini", api_key=token),
        browser_context=context
    )
    result=await agent.run()
    return  agent.resultstep


# Route to execute the agent task
@app.route('/run-agent', methods=['GET'])
def run_agent_endpoint():
        # Run the asynchronous task and get the result
    result = asyncio.run(run_agent())
    return jsonify({"Ouptut":result})
        

# Health check endpoint
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "API is running!"})

# Run the Flask app
if __name__ == '__main__':
    app.run()
