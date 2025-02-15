"""Defines the Gradio interface."""

from typing import Callable
import gradio as gr
from dotenv import load_dotenv
from browser_use.agent.service import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig,  BrowserContext
from langchain_core.language_models.chat_models import BaseChatModel
from smartbrowser.llms import get_llm

load_dotenv()

def build_ui(llm: BaseChatModel) -> gr.Interface:
    """Builds the Gradio interface."""

    
    async def handle_task(
        task: str,
        model_name: str,
        use_vision: bool,
        max_failures: int,
        use_vision_for_planner: bool,
        retry_delay: int,
        max_input_tokens: int,
        validate_output: bool,
        planner_interval: int,
        headless: bool,
        disable_security: bool,
        min_wait_page_load: float,
        max_wait_page_load: float,
        wait_between_actions: float,
        browser_window_height: int,
        browser_window_width: int,
        highlight_elements: bool,
    ) -> str:
        """Handles the task submission and agent creation."""

        # Creates browser config
        # browser_config = BrowserConfig(
        #     headless=headless,
        #     disable_security=disable_security,
       
        # )
        # # Create browser context config
        # browser_config = BrowserContextConfig(
            
        #     minimum_wait_page_load_time=min_wait_page_load,
        #     maximum_wait_page_load_time=max_wait_page_load,
        #     wait_between_actions=wait_between_actions,
        #     disable_security=disable_security,
        #     browser_window_size={
        #         "width": browser_window_width,
        #         "height": browser_window_height
        #     },
        #     highlight_elements=highlight_elements
        # )

        # # Create browser instance
        # browser = Browser(config=browser_config)
        # browser_context = BrowserContext(browser=browser, config=browser_config)
        
        # Create agent
        agent = Agent(
            task=task,
            llm=llm,
            # browser_context=browser_context,
            # use_vision=use_vision,
            # use_vision_for_planner=use_vision_for_planner,
            # max_failures=max_failures,
            # retry_delay=retry_delay,
            # max_input_tokens=max_input_tokens,
            # validate_output=validate_output,
            # planner_interval=planner_interval
        )
        
        # Run the agent
        history = await agent.run()
        
        # Return results
        return f"Task completed. Results: {history.final_result()}"

    inputs = create_inputs()
    outputs = create_outputs()

    return gr.Interface(
        fn=handle_task,
        inputs=inputs,
        outputs=outputs,
        title="Browser-Use Agent Interface",
        description="Configure and run browser automation tasks using the browser-use agent."
    )

def create_inputs() -> list:
    """Creates the inputs for the Gradio interface."""
    return [
        # Task input
        gr.Textbox(
            label="Task",
            placeholder="Enter the task you want the agent to perform...",
            lines=3
        ),
        
        # Agent Configuration
        gr.Textbox(
            label="Model Name",
            value="claude-3-sonnet-20240229",
            info="The name of the model to use"
        ),
        gr.Checkbox(
            label="Use Vision",
            value=True,
            info="Enable vision capabilities"
        ),
        gr.Number(
            label="Max Failures",
            value=3,
            minimum=1,
            maximum=10,
            info="Maximum number of consecutive failures before stopping"
        ),
        gr.Checkbox(
            label="Use Vision for Planner",
            value=False,
            info="Enable vision for the planner"
        ),
        gr.Number(
            label="Retry Delay",
            value=10,
            info="Delay between retries in seconds"
        ),
        gr.Number(
            label="Max Input Tokens",
            value=1024,
            info="Maximum number of input tokens"
        ),
        gr.Checkbox(
            label="Validate Output",
            value=False,
            info="Enable output validation"
        ),
        gr.Number(
            label="Planner Interval",
            value=1,
            info="Interval between planning steps"
        ),
        
        # Browser Configuration
        gr.Checkbox(
            label="Headless",
            value=True,
            info="Run browser in headless mode"
        ),
        gr.Checkbox(
            label="Disable Security",
            value=False,
            info="Disable browser security features"
        ),
        gr.Number(
            label="Minimum Wait Page Load Time",
            value=0.5,
            info="Minimum time to wait for page load"
        ),
        gr.Number(
            label="Maximum Wait Page Load Time",
            value=5.0,
            info="Maximum time to wait for page load"
        ),
        gr.Number(
            label="Wait Between Actions",
            value=1.0,
            info="Time to wait between actions"
        ),
        gr.Number(
            label="Browser Window Height",
            value=1100,
            info="Browser window height"
        ),
        gr.Number(
            label="Browser Window Width",
            value=1280,
            info="Browser window width"
        ),
        gr.Checkbox(
            label="Highlight Elements",
            value=True,
            info="Highlight interacted elements"
        ),
    ]

def create_outputs() -> list:
    """Creates the outputs for the Gradio interface."""
    return [
        gr.Textbox(
            label="Results",
            lines=10
        )
    ]



def main():
    """Main function."""

    llm = get_llm("claude-3-5-sonnet-latest")
    ui = build_ui(llm)
    ui.launch(debug=True)


if __name__ == "__main__":
    main()

