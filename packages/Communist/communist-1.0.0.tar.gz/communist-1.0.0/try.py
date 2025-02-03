from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
# from browser_use import Agent
from Communist import Agent
from Communist.controller.service import resultstep
# from browser_use.agent.views import FireflinkNLP
import asyncio


async def main():
    token = "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"
    endpoint = "https://models.inference.ai.azure.com"
    deepseek = "https://api.deepseek.com"
    agent = Agent(
        task=""" Navigate t0 flipkart""",
        use_vision=False,
        # llm=ChatGroq(model="llama-3.2-11b-vision-preview",api_key="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")
        llm=ChatOpenAI(model="gpt-4o-mini", api_key=token)
    )
    result = await agent.run()
    print(resultstep.get_steps())
    # output = {}
    # for index, step in enumerate(FireflinkNLP().steps):
    #     output[index] = step
    # print(output)
asyncio.run(main())
