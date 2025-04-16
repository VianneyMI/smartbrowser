"""`smartbrowser.ui` module.
Defines a Tkinter interface to configure and run browser automation tasks using the browser-use agent.

"""

import asyncio
import tkinter as tk
from tkinter import ttk
from typing import Callable, get_args
from dotenv import load_dotenv
from smartbrowser.llms import all_models_literal

load_dotenv()

TITLE = "Browser-Use Agent Interface"
DESCRIPTION = "Configure and run browser automation tasks using the browser-use agent."


class CollapsibleFrame(ttk.Frame):
    def __init__(self, parent, text="", *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)

        self.show = tk.BooleanVar(value=False)
        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        ttk.Label(self.title_frame, text=text).pack(side="left", fill="x", expand=1)
        self.toggle_button = ttk.Checkbutton(
            self.title_frame,
            width=2,
            text="+",
            command=self.toggle,
            variable=self.show,
            style="Toolbutton",
        )
        self.toggle_button.pack(side="left")

        self.sub_frame = ttk.Frame(self)

    def toggle(self):
        if self.show.get():
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text="-")
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text="+")


class UIBuilder:
    """`smartbrowser.ui.UIBuilder` class.

    Gathers all the components of the UI and builds the Tkinter interface.
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
        self.inputs = {}
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("1000x800")  # Larger default size
        self.root.minsize(800, 600)  # Minimum size

        # Configure style
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#2196F3")
        style.configure("TLabel", padding=6)
        style.configure("TFrame", padding=6)

        # Create main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create left and right columns
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

    def build(self) -> tk.Tk:
        """Builds the Tkinter interface."""
        self.add_title()
        self.add_description()
        self.add_task_input()
        self.add_submit_button()
        self.add_results_output()
        self.add_agent_configuration()
        self.add_browser_configuration()
        self.add_browser_context_configuration()
        return self.root

    def add_title(self) -> None:
        """Adds the title to the interface."""
        title_label = ttk.Label(
            self.left_frame, text=self.title, font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=10)

    def add_description(self) -> None:
        """Adds the description to the interface."""
        desc_label = ttk.Label(self.left_frame, text=self.description, wraplength=350)
        desc_label.pack(pady=5)

    def add_task_input(self) -> None:
        """Adds the task input to the left column."""
        task_frame = ttk.LabelFrame(self.left_frame, text="Task")
        task_frame.pack(fill=tk.X, pady=5)

        # Add scrollbar to text widget
        scrollbar = ttk.Scrollbar(task_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_input = tk.Text(task_frame, height=3, width=40, wrap=tk.WORD)
        self.task_input.pack(fill=tk.X, padx=5, pady=5)
        self.task_input.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_input.yview)

        self.inputs[1] = self.task_input

    def add_submit_button(self) -> None:
        """Adds the submit button to the left column."""
        self.submit = ttk.Button(
            self.left_frame, text="Run Task", command=self._on_submit
        )
        self.submit.pack(pady=10)

    def add_results_output(self) -> None:
        """Adds the results output to the left column."""
        results_frame = ttk.LabelFrame(self.left_frame, text="Results")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Add scrollbar to text widget
        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.results_output = tk.Text(results_frame, height=10, width=40, wrap=tk.WORD)
        self.results_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.results_output.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.results_output.yview)

        self.outputs = self.results_output

    def add_agent_configuration(self) -> None:
        """Adds the agent configuration menu to the right column."""
        agent_frame = CollapsibleFrame(self.right_frame, text="Agent Configuration")
        agent_frame.pack(fill=tk.X, pady=5)

        # API Key
        ttk.Label(agent_frame.sub_frame, text="API Key:").pack(anchor="w")
        api_key = ttk.Entry(agent_frame.sub_frame)
        api_key.pack(fill=tk.X, padx=5, pady=2)
        self.inputs[19] = api_key

        # Model Name
        ttk.Label(agent_frame.sub_frame, text="Model Name:").pack(anchor="w")
        model_name = ttk.Combobox(
            agent_frame.sub_frame,
            values=list(get_args(all_models_literal)),
            state="readonly",
        )
        model_name.set("claude-3-5-sonnet-latest")
        model_name.pack(fill=tk.X, padx=5, pady=2)
        self.inputs[2] = model_name

        # Checkboxes
        use_vision = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            agent_frame.sub_frame, text="Use Vision", variable=use_vision
        ).pack(anchor="w", padx=5, pady=2)
        self.inputs[3] = use_vision

        use_vision_for_planner = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            agent_frame.sub_frame,
            text="Use Vision for Planner",
            variable=use_vision_for_planner,
        ).pack(anchor="w", padx=5, pady=2)
        self.inputs[5] = use_vision_for_planner

        validate_output = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            agent_frame.sub_frame, text="Validate Output", variable=validate_output
        ).pack(anchor="w", padx=5, pady=2)
        self.inputs[8] = validate_output

        # Number inputs
        self._add_number_input(agent_frame.sub_frame, "Max Failures", 3, 1, 10, 4)
        self._add_number_input(agent_frame.sub_frame, "Retry Delay", 10, 0, 60, 6)
        self._add_number_input(
            agent_frame.sub_frame, "Max Input Tokens", 1024, 1, 4096, 7
        )
        self._add_number_input(agent_frame.sub_frame, "Planner Interval", 1, 0, 10, 9)

    def add_browser_configuration(self) -> None:
        """Adds the browser configuration menu to the right column."""
        browser_frame = CollapsibleFrame(self.right_frame, text="Browser Configuration")
        browser_frame.pack(fill=tk.X, pady=5)

        # Chrome Path
        ttk.Label(browser_frame.sub_frame, text="Chrome Path:").pack(anchor="w")
        chrome_path = ttk.Entry(browser_frame.sub_frame)
        chrome_path.pack(fill=tk.X, padx=5, pady=2)
        self.inputs[10] = chrome_path

        # Checkboxes
        headless = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            browser_frame.sub_frame, text="Headless", variable=headless
        ).pack(anchor="w", padx=5, pady=2)
        self.inputs[11] = headless

        disable_security = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            browser_frame.sub_frame, text="Disable Security", variable=disable_security
        ).pack(anchor="w", padx=5, pady=2)
        self.inputs[12] = disable_security

    def add_browser_context_configuration(self) -> None:
        """Adds the browser context configuration menu to the right column."""
        context_frame = CollapsibleFrame(
            self.right_frame, text="Browser Context Configuration"
        )
        context_frame.pack(fill=tk.X, pady=5)

        # Number inputs
        self._add_number_input(
            context_frame.sub_frame, "Min Wait Page Load", 0.5, 0, 10, 13
        )
        self._add_number_input(
            context_frame.sub_frame, "Max Wait Page Load", 5.0, 0, 30, 14
        )
        self._add_number_input(
            context_frame.sub_frame, "Wait Between Actions", 1.0, 0, 10, 15
        )
        self._add_number_input(
            context_frame.sub_frame, "Browser Window Height", 1100, 100, 2000, 16
        )
        self._add_number_input(
            context_frame.sub_frame, "Browser Window Width", 1280, 100, 2000, 17
        )

        # Checkbox
        highlight_elements = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            context_frame.sub_frame,
            text="Highlight Elements",
            variable=highlight_elements,
        ).pack(anchor="w", padx=5, pady=2)
        self.inputs[18] = highlight_elements

    def _add_number_input(self, parent, label, default, min_val, max_val, input_id):
        """Helper method to add number input fields."""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(frame, text=f"{label}:").pack(side=tk.LEFT)

        var = tk.DoubleVar(value=default)
        spinbox = ttk.Spinbox(
            frame,
            from_=min_val,
            to=max_val,
            textvariable=var,
            width=10,
            format="%.2f",  # Format for decimal values
        )
        spinbox.pack(side=tk.RIGHT)
        self.inputs[input_id] = var

    def _on_submit(self):
        """Handler for the submit button."""
        if self.handler:
            # Get values from inputs
            input_values = []
            for key in sorted(self.inputs.keys()):
                widget = self.inputs[key]
                if isinstance(widget, tk.Text):
                    value = widget.get(
                        "1.0", tk.END
                    ).strip()  # Get all text from start to end
                elif isinstance(widget, ttk.Entry):
                    value = widget.get()
                elif isinstance(widget, (tk.BooleanVar, tk.DoubleVar)):
                    value = widget.get()
                elif isinstance(widget, ttk.Combobox):
                    value = widget.get()
                else:
                    value = widget
                input_values.append(value)

            # Call handler with inputs
            result = asyncio.run(self.handler(*input_values))

            # Update results output
            self.results_output.delete(1.0, tk.END)
            if result is not None:
                self.results_output.insert(tk.END, str(result))
            else:
                self.results_output.insert(tk.END, "Task completed with no output.")
