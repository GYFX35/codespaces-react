import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtWebEngineWidgets import (
    QWebEngineView,
    QWebEngineProfile,
    QWebEngineSettings,
)


class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- Basic Window Setup ---
        self.setWindowTitle("Simple Browser - Loading...")
        self.setGeometry(100, 100, 1024, 768)  # x, y, width, height

        # --- Web Engine View ---
        self.browser = QWebEngineView()
        # Set a default blank page or simple HTML content initially
        self.browser.setHtml(
            """
            <html>
                <head><title>Blank Page</title></head>
                <body style='font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 90vh; font-size: 1.2em; color: #777;'>
                    <p>Enter a URL above to start browsing.</p>
                </body>
            </html>
        """
        )
        self.browser.urlChanged.connect(self.update_url_bar)
        self.browser.titleChanged.connect(self.update_window_title)
        self.browser.loadFinished.connect(self.on_load_finished)

        # --- Toolbar for Navigation ---
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setMovable(False)  # Keep it simple, not movable
        self.addToolBar(self.toolbar)

        # Back Button
        self.back_button = QPushButton("< Back")
        self.back_button.clicked.connect(self.browser.back)
        self.toolbar.addWidget(self.back_button)

        # Forward Button
        self.forward_button = QPushButton("Forward >")
        self.forward_button.clicked.connect(self.browser.forward)
        self.toolbar.addWidget(self.forward_button)

        # Reload Button
        self.reload_button = QPushButton("Reload")
        self.reload_button.clicked.connect(self.browser.reload)
        self.toolbar.addWidget(self.reload_button)

        # Home Button (simple placeholder action for now)
        self.home_button = QPushButton("Home")
        self.home_button.clicked.connect(self.navigate_home)
        self.toolbar.addWidget(self.home_button)

        # URL Bar (QLineEdit)
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL and press Enter")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)

        # --- Central Widget and Layout ---
        # QWebEngineView will be the central widget
        self.setCentralWidget(self.browser)

        # Initial button states
        self.update_nav_buttons_state()

    def navigate_to_url(self):
        """Navigates to the URL entered in the URL bar."""
        url_text = self.url_bar.text().strip()
        if not url_text:
            return

        # Add http:// prefix if missing for convenience
        if not url_text.startswith(("http://", "https://")):
            url_text = "http://" + url_text

        self.browser.setUrl(QUrl(url_text))

    def navigate_home(self):
        """Navigates to a predefined home page (blank for now)."""
        self.browser.setHtml(
            """
            <html>
                <head><title>Blank Page</title></head>
                <body style='font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 90vh; font-size: 1.2em; color: #777;'>
                    <p>Welcome! Enter a URL above to start browsing.</p>
                </body>
            </html>
        """
        )
        self.url_bar.setText("")  # Clear URL bar for home

    def update_url_bar(self, qurl):
        """Updates the URL bar with the current URL of the browser view."""
        # Only update if it's different, to avoid cursor jumping during typing
        if qurl.toString() != self.url_bar.text():
            self.url_bar.setText(qurl.toString())

    def update_window_title(self, title):
        """Updates the main window title."""
        if title:
            self.setWindowTitle(f"{title} - Simple Browser")
        else:
            self.setWindowTitle("Simple Browser")

    def on_load_finished(self, success):
        """Called when a page load is finished."""
        self.update_nav_buttons_state()
        if not success:
            # Basic error page
            self.browser.setHtml(
                f"""
                <html><head><title>Error Loading Page</title></head>
                <body style='font-family: sans-serif; padding: 20px;'>
                    <h2>Error Loading Page</h2>
                    <p>Could not load the requested page: {self.url_bar.text()}</p>
                    <p>Please check the URL and your internet connection.</p>
                </body></html>
            """
            )

    def update_nav_buttons_state(self):
        """Enables/disables back/forward buttons based on browser history."""
        self.back_button.setEnabled(self.browser.history().canGoBack())
        self.forward_button.setEnabled(self.browser.history().canGoForward())


if __name__ == "__main__":
    # --- Application Setup ---
    # Enable High DPI scaling for better visuals on some systems
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # --- Configure WebEngine Profile & Settings for Distraction-Free ---
    # Get the default profile
    profile = QWebEngineProfile.defaultProfile()

    # Attempt to disable JavaScript opening new windows (pop-ups)
    # These settings are hints; behavior can vary based on web content.
    settings = profile.settings()
    settings.setAttribute(
        QWebEngineSettings.JavascriptCanOpenWindows, False
    )  # Key for pop-ups
    settings.setAttribute(
        QWebEngineSettings.PluginsEnabled, False
    )  # Disable plugins like Flash (mostly obsolete but good for minimal)
    settings.setAttribute(
        QWebEngineSettings.FullScreenSupportEnabled, True
    )  # Allow full screen if page requests
    # settings.setAttribute(QWebEngineSettings.AutoLoadImages, True) # Keep images by default
    # settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True) # Keep JS for modern sites

    window = SimpleBrowser()
    window.show()

    sys.exit(app.exec_())
