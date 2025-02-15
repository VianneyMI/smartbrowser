"""Defines the Gradio interface."""

from typing import Callable
import gradio as gr


def build_ui(fn:Callable)->gr.Interface:
    """Builds the Gradio interface."""

    inputs = create_inputs()
    outputs = create_outputs()

    return gr.Interface(fn=fn, inputs=inputs, outputs=outputs)



def create_inputs()->list[str]:
    """Creates the inputs for the Gradio interface."""


def create_outputs()->list[str]:
    """Creates the outputs for the Gradio interface."""





