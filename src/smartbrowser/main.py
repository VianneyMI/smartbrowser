"""Entry point of the Gradio and Browser Use powered SmartBrowser.

Basically, it is used to launch the script.
"""

from smartbrowser.handler import work, dummy_work
from smartbrowser.ui import build_ui


def main()->None:
    """Launches the application."""

    ui = build_ui(work)
    ui.launch(debug=True)


if __name__ == "__main__":
    main()
