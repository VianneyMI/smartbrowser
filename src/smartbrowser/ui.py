"""`smartbrowser.ui` module.
Defines a Gradio interface to configure and run browser automation tasks using the browser-use agent.

"""

from typing import Callable, get_args
import gradio as gr
from dotenv import load_dotenv
from smartbrowser.llms import all_models_literal

load_dotenv()

TITLE = "Browser-Use Agent Interface"
DESCRIPTION = "Configure and run browser automation tasks using the browser-use agent."


class UIBuilder:
    """`smartbrowser.ui.UIBuilder` class.

    Gathers all the components of the UI and builds the Gradio interface.
    """

    def __init__(
        self,
        title: str = TITLE,
        description: str = DESCRIPTION,
        handler: Callable | None = None,
    ) -> None:
        self.title = title
        self.description = description
        self.handler = handler
        self.inputs: dict[int, gr.Component] = {}
        self.outputs: gr.Component | None = None
        self.submit: gr.Button = None  # type: ignore

        with gr.Blocks(title=title) as interface:
            self.interface = interface

    def build(self) -> gr.Interface:
        """Builds the Gradio interface."""

        with self.interface:
            self.add_title()
            self.add_description()
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

    def add_title(self) -> gr.Markdown:
        """Adds the title to the interface."""

        return gr.Markdown(f"# {self.title}")

    def add_description(self) -> gr.Markdown:
        """Adds the description to the interface."""

        return gr.Markdown(self.description)

    def add_task_input(self) -> gr.Textbox:
        """Adds the task input to the left column."""

        task_input = gr.Textbox(
            label="Task",
            placeholder="Enter the task you want the agent to perform...",
            lines=3,
        )
        self.inputs[1] = task_input
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
            model_name = gr.Dropdown(
                label="Model Name",
                choices=list(get_args(all_models_literal)),
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

        self.inputs[2] = model_name
        self.inputs[3] = use_vision
        self.inputs[4] = max_failures
        self.inputs[5] = use_vision_for_planner
        self.inputs[6] = retry_delay
        self.inputs[7] = max_input_tokens
        self.inputs[8] = validate_output
        self.inputs[9] = planner_interval

        return agent_configuration_accordion

    def add_browser_configuration(self) -> gr.Accordion:
        """Adds the browser configuration menu to the right column."""

        with gr.Accordion(
            "Browser Configuration", open=False
        ) as browser_configuration_accordion:
            chrome_path = gr.Text(
                label="Enter path to Chrome executable",
            )
            headless = gr.Checkbox(
                label="Headless", value=False, info="Run browser in headless mode"
            )
            disable_security = gr.Checkbox(
                label="Disable Security",
                value=False,
                info="Disable browser security features",
            )

        self.inputs[10] = chrome_path
        self.inputs[11] = headless
        self.inputs[12] = disable_security

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

        self.inputs[13] = min_wait_page_load
        self.inputs[14] = max_wait_page_load
        self.inputs[15] = wait_between_actions
        self.inputs[16] = browser_window_height
        self.inputs[17] = browser_window_width
        self.inputs[18] = highlight_elements

        return browser_context_configuration_accordion
