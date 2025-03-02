
import gradio as gr


TITLE = "test"

def test_context_manager():
    """Test the context manager."""

    class Builder:
        def __init__(self):
            self.interface:gr.Blocks = None


    builder = Builder()
       
            
    
    with gr.Blocks(title=TITLE) as interface:
        builder.interface = interface

    with builder.interface:
        gr.Markdown(f"# {TITLE}")
        gr.Markdown("this is a test")

    assert builder.interface.launch()


if __name__ == "__main__":
    test_context_manager()
