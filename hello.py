"""Getting started exploration script."""

import asyncio

from dotenv import load_dotenv
import gradio as gr
from browser_use import Agent, Browser, BrowserConfig
from browser_use.browser.browser import BrowserContext, BrowserContextConfig
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

def get_llm():

    model_name = "gemini-2.0-flash-exp" # should be an input
    return ChatGoogleGenerativeAI(model=model_name)


def create_agent(task:str, llm:BaseChatModel)->Agent:
    """Creates an agent."""

    browser_context_config = BrowserContextConfig(
        
    )
    browser_context = BrowserContext()

    browser = Browser(
        config = BrowserConfig(
            headless=False,
            disable_security=True
        )
    )
    agent = Agent(task, llm=llm, browser=browser)
    return agent


async def work(task:str)->str:
    
    llm = get_llm()
    agent = create_agent(task, llm)
    history = await agent.run()
    history.save_to_file("history.json") 
    # history.json should change with each run, the name should be generated automatically or be taken as an input

    return history.final_result()



def main():
    print("Hello from SmartBrowser!")

    demo = gr.Interface(
        fn=work,
        inputs=["text"],
        outputs=["text"]
    )
    demo.launch(debug=True)

demo_task = "Go to Yahoo Finance and tell me what's Meta market captialization"


if __name__ == "__main__":
    main()