"""Defines the Gradio interface."""

from pathlib import Path
from typing import Callable
import gradio as gr
from dotenv import load_dotenv
from browser_use.agent.service import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from langchain_core.language_models.chat_models import BaseChatModel
from smartbrowser.llms import get_llm

load_dotenv()

TITLE = "Browser-Use Agent Interface"
DESCRIPTION = "Configure and run browser automation tasks using the browser-use agent."


class UIBuilder:
    """Builds the Gradio interface."""

    def __init__(
        self,
        title: str = TITLE,
        description: str = DESCRIPTION,
        handler: Callable | None = None,
    ) -> None:
        self.handler = handler
        self.inputs = {}
        self.outputs = None
        self.submit: gr.Button | None = None

        with gr.Blocks(title=title) as interface:
            self.interface = interface
            self.add_title_and_description(title, description)

    def build(self) -> gr.Interface:
        """Builds the Gradio interface."""

        with self.interface:
            with gr.Row():
                with gr.Column(scale=1):
                    self.add_task_input()
                    self.add_submit_button()
                    self.add_results_output()

                with gr.Column(scale=1):
                    self.add_agent_configuration()
                    self.add_browser_configuration()
                    self.add_browser_context_configuration()

            self.submit.click(
                fn=self.handler,
                inputs=list(self.inputs.values()),
                outputs=self.outputs,
            )

        return self.interface

    def add_title_and_description(self, title: str, description: str) -> None:
        """Adds the title and description to the interface."""
        gr.Markdown(f"# {title}")
        gr.Markdown(description)

    def add_task_input(self) -> gr.Textbox:
        """Adds the task input to the left column."""

        task_input = gr.Textbox(
            label="Task",
            placeholder="Enter the task you want the agent to perform...",
            lines=3,
        )
        self.inputs["task"] = task_input
        return task_input

    def add_submit_button(self) -> gr.Button:
        """Adds the submit button to the left column."""

        submit_btn = gr.Button("Run Task", variant="primary")
        self.submit = submit_btn
        return submit_btn

    def add_results_output(self) -> gr.Textbox:
        """Adds the results output to the left column."""

        results_output = gr.Textbox(label="Results", lines=10)
        self.outputs = results_output
        return results_output

    def add_agent_configuration(self) -> None:
        """Adds the agent configuration menu to the right column."""

        with gr.Accordion(
            "Agent Configuration", open=False
        ) as agent_configuration_accordion:
            model_name = gr.Textbox(
                label="Model Name",
                value="claude-3-5-sonnet-latest",
                info="The name of the model to use",
            )
            use_vision = gr.Checkbox(
                label="Use Vision", value=True, info="Enable vision capabilities"
            )
            max_failures = gr.Number(
                label="Max Failures",
                value=3,
                minimum=1,
                maximum=10,
                info="Maximum number of consecutive failures before stopping",
            )
            use_vision_for_planner = gr.Checkbox(
                label="Use Vision for Planner",
                value=False,
                info="Enable vision for the planner",
            )
            retry_delay = gr.Number(
                label="Retry Delay", value=10, info="Delay between retries in seconds"
            )
            max_input_tokens = gr.Number(
                label="Max Input Tokens",
                value=1024,
                info="Maximum number of input tokens",
            )
            validate_output = gr.Checkbox(
                label="Validate Output", value=False, info="Enable output validation"
            )
            planner_interval = gr.Number(
                label="Planner Interval",
                value=1,
                info="Interval between planning steps",
            )

        self.inputs["model_name"] = model_name
        self.inputs["use_vision"] = use_vision
        self.inputs["max_failures"] = max_failures
        self.inputs["use_vision_for_planner"] = use_vision_for_planner
        self.inputs["retry_delay"] = retry_delay
        self.inputs["max_input_tokens"] = max_input_tokens
        self.inputs["validate_output"] = validate_output
        self.inputs["planner_interval"] = planner_interval

        return agent_configuration_accordion

    def add_browser_configuration(self) -> gr.Accordion:
        """Adds the browser configuration menu to the right column."""

        with gr.Accordion(
            "Browser Configuration", open=False
        ) as browser_configuration_accordion:
            chrome_path = gr.File(
                label="Chrome Executable Path",
                file_types=[".exe"],
                type="filepath",
                # info="Path to Chrome executable (optional)"
            )
            headless = gr.Checkbox(
                label="Headless", value=True, info="Run browser in headless mode"
            )
            disable_security = gr.Checkbox(
                label="Disable Security",
                value=False,
                info="Disable browser security features",
            )

        self.inputs["chrome_path"] = chrome_path
        self.inputs["headless"] = headless
        self.inputs["disable_security"] = disable_security

        return browser_configuration_accordion

    def add_browser_context_configuration(self) -> gr.Accordion:
        """Adds the browser context configuration menu to the right column."""

        with gr.Accordion(
            "Browser Context Configuration", open=False
        ) as browser_context_configuration_accordion:
            min_wait_page_load = gr.Number(
                label="Minimum Wait Page Load Time",
                value=0.5,
                info="Minimum time to wait for page load",
            )
            max_wait_page_load = gr.Number(
                label="Maximum Wait Page Load Time",
                value=5.0,
                info="Maximum time to wait for page load",
            )
            wait_between_actions = gr.Number(
                label="Wait Between Actions",
                value=1.0,
                info="Time to wait between actions",
            )
            browser_window_height = gr.Number(
                label="Browser Window Height", value=1100, info="Browser window height"
            )
            browser_window_width = gr.Number(
                label="Browser Window Width", value=1280, info="Browser window width"
            )
            highlight_elements = gr.Checkbox(
                label="Highlight Elements",
                value=True,
                info="Highlight interacted elements",
            )

        self.inputs["min_wait_page_load"] = min_wait_page_load
        self.inputs["max_wait_page_load"] = max_wait_page_load
        self.inputs["wait_between_actions"] = wait_between_actions
        self.inputs["browser_window_height"] = browser_window_height
        self.inputs["browser_window_width"] = browser_window_width
        self.inputs["highlight_elements"] = highlight_elements

        return browser_context_configuration_accordion


def build_ui(self) -> gr.Interface:
    """Builds the Gradio interface."""

    with gr.Blocks(title=TITLE) as interface:
        gr.Markdown(f"# {TITLE}")
        gr.Markdown(DESCRIPTION)

        with gr.Row():
            # Left Column - Task and Results
            with gr.Column(scale=1):
                task_input = gr.Textbox(
                    label="Task",
                    placeholder="Enter the task you want the agent to perform...",
                    lines=3,
                )
                submit_btn = gr.Button("Run Task", variant="primary")
                results_output = gr.Textbox(label="Results", lines=10)

            # Right Column - Configuration Parameters
            with gr.Column(scale=1):
                with gr.Accordion("Agent Configuration", open=False):
                    model_name = gr.Textbox(
                        label="Model Name",
                        value="claude-3-5-sonnet-latest",
                        info="The name of the model to use",
                    )
                    use_vision = gr.Checkbox(
                        label="Use Vision",
                        value=True,
                        info="Enable vision capabilities",
                    )
                    max_failures = gr.Number(
                        label="Max Failures",
                        value=3,
                        minimum=1,
                        maximum=10,
                        info="Maximum number of consecutive failures before stopping",
                    )
                    use_vision_for_planner = gr.Checkbox(
                        label="Use Vision for Planner",
                        value=False,
                        info="Enable vision for the planner",
                    )
                    retry_delay = gr.Number(
                        label="Retry Delay",
                        value=10,
                        info="Delay between retries in seconds",
                    )
                    max_input_tokens = gr.Number(
                        label="Max Input Tokens",
                        value=1024,
                        info="Maximum number of input tokens",
                    )
                    validate_output = gr.Checkbox(
                        label="Validate Output",
                        value=False,
                        info="Enable output validation",
                    )
                    planner_interval = gr.Number(
                        label="Planner Interval",
                        value=1,
                        info="Interval between planning steps",
                    )

                with gr.Accordion("Browser Configuration", open=False):
                    chrome_path = gr.File(
                        label="Chrome Executable Path",
                        file_types=[".exe"],
                        type="filepath",
                        # info="Path to Chrome executable (optional)"
                    )
                    headless = gr.Checkbox(
                        label="Headless",
                        value=True,
                        info="Run browser in headless mode",
                    )
                    disable_security = gr.Checkbox(
                        label="Disable Security",
                        value=False,
                        info="Disable browser security features",
                    )

                with gr.Accordion("Browser Context Configuration", open=False):
                    min_wait_page_load = gr.Number(
                        label="Minimum Wait Page Load Time",
                        value=0.5,
                        info="Minimum time to wait for page load",
                    )
                    max_wait_page_load = gr.Number(
                        label="Maximum Wait Page Load Time",
                        value=5.0,
                        info="Maximum time to wait for page load",
                    )
                    wait_between_actions = gr.Number(
                        label="Wait Between Actions",
                        value=1.0,
                        info="Time to wait between actions",
                    )
                    browser_window_height = gr.Number(
                        label="Browser Window Height",
                        value=1100,
                        info="Browser window height",
                    )
                    browser_window_width = gr.Number(
                        label="Browser Window Width",
                        value=1280,
                        info="Browser window width",
                    )
                    highlight_elements = gr.Checkbox(
                        label="Highlight Elements",
                        value=True,
                        info="Highlight interacted elements",
                    )

        # Wire up the submit button
        submit_btn.click(
            fn=handle_task,
            inputs=[
                task_input,
                model_name,
                use_vision,
                max_failures,
                use_vision_for_planner,
                retry_delay,
                max_input_tokens,
                validate_output,
                planner_interval,
                chrome_path,
                headless,
                disable_security,
                min_wait_page_load,
                max_wait_page_load,
                wait_between_actions,
                browser_window_height,
                browser_window_width,
                highlight_elements,
            ],
            outputs=results_output,
        )

    return interface


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
    chrome_path: str | None,
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

    llm = get_llm(model_name)

    # Create browser config
    browser_config = BrowserConfig(
        headless=headless,
        disable_security=disable_security,
        chrome_instance_path=Path("C:\Program Files\Google\Chrome\Application")
        / "chrome.exe",
        # chrome_path.name if chrome_path else None
    )

    # Create browser context config
    context_config = BrowserContextConfig(
        # min_wait_page_load=min_wait_page_load,
        # max_wait_page_load=max_wait_page_load,
        # wait_between_actions=wait_between_actions,
        # browser_window_height=browser_window_height,
        # browser_window_width=browser_window_width,
        # highlight_elements=highlight_elements
    )

    # Create browser and context
    browser = Browser(config=browser_config)
    context = BrowserContext(browser=browser, config=context_config)

    agent = Agent(task=task, llm=llm, browser_context=context)

    history = await agent.run()
    return f"Task completed. Results: {history.final_result()}"


def main():
    """Main function."""
    llm = get_llm("claude-3-5-sonnet-latest")
    # ui = build_ui(llm)
    ui = UIBuilder().build()
    ui.launch(debug=True)


if __name__ == "__main__":
    main()
