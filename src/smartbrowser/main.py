"""`smartbrowser.main` module.
Entry point of the Browser Use powered SmartBrowser.
Used to launch the app.
"""

from smartbrowser.handler import handle_task
from smartbrowser.ui import UIBuilder


def main():
    """Launches the SmartBrowser app."""
    ui = UIBuilder(handler=handle_task)
    root = ui.build()
    root.mainloop()


if __name__ == "__main__":
    main()
