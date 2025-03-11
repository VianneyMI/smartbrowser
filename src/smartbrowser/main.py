"""`smartbrowser.main` module.
Entry point of the Gradio and Browser Use powered SmartBrowser.
Used to launch the app.
"""

from smartbrowser.handler import handle_task
from smartbrowser.ui import UIBuilder


def main():
    """Launches the SmartBrowser app."""

    ui = UIBuilder(handler=handle_task).build()
    ui.launch(debug=True)


if __name__ == "__main__":
    main()
