"""Entry point of the Gradio and Browser Use powered SmartBrowser.

Basically, it is used to launch the script.
"""

from smartbrowser.handler import handle_task
from smartbrowser.ui import UIBuilder


def main():
    """Main function."""

    ui = UIBuilder(handler=handle_task).build()
    ui.launch(debug=True)


if __name__ == "__main__":
    main()
