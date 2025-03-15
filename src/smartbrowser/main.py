"""`smartbrowser.main` module.
Entry point of the Gradio and Browser Use powered SmartBrowser.
Used to launch the app.
"""

from smartbrowser.handler import handle_task
from smartbrowser.ui import UIBuilder


def main():
    """Launches the SmartBrowser app."""

    ui = UIBuilder(handler=handle_task).build()
    _, local_url, _ = ui.launch(debug=True)

    message = f"""
    SmartBrowser is running on {local_url}

    You can now start using the SmartBrowser.
    Copy and paste the url above in a browser other than Google Chrome.

    """.strip()

    input(message)


if __name__ == "__main__":
    main()
