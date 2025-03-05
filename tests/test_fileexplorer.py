import gradio as gr
import os


def handle_file_selection(file_path):
    """Handle when a file is selected in the explorer"""
    if file_path:
        return f"Selected file: {file_path}"
    return "No file selected"


def handle_folder_selection(folder_path):
    """Handle when a folder is selected in the explorer"""
    if folder_path:
        return f"Selected folder: {folder_path}"
    return "No folder selected"


# Create demo app
with gr.Blocks() as demo:
    gr.Markdown("## File Explorer Test")

    # Create file explorer component
    file_explorer = gr.FileExplorer()

    # Output text components
    file_output = gr.Textbox(label="File Selection Output")
    folder_output = gr.Textbox(label="Folder Selection Output")

    # # Handle file/folder selection events
    # file_explorer.select(
    #     handle_file_selection, inputs=[file_explorer], outputs=[file_output]
    # )

    # file_explorer.change(
    #     handle_folder_selection, inputs=[file_explorer], outputs=[folder_output]
    # )

if __name__ == "__main__":
    demo.launch()
