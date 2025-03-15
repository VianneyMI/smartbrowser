"""`smartbrowser.main` module.
Entry point of the Gradio and Browser Use powered SmartBrowser.
Used to launch the app.
"""

import time
from smartbrowser.handler import handle_task
from smartbrowser.ui import UIBuilder


def main():
    """Launches the SmartBrowser app."""

    ui = UIBuilder(handler=handle_task).build()
    ui.launch()
    time.sleep(1000)


if __name__ == "__main__":
    main()
