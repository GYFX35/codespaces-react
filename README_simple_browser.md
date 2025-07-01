# Simple Browser - Distraction-Free Web Viewer

Simple Browser is a minimalist web browser built with Python and PyQt5. It's designed for users who need a distraction-free environment for focused reading, research, or browsing. The emphasis is on maximizing content display and minimizing UI clutter.

## Features (MVP)

*   **Minimalist Interface:** A clean and simple UI with only essential controls visible.
*   **URL Navigation:** Enter a web address in the URL bar to navigate.
*   **Core Navigation Controls:**
    *   Back
    *   Forward
    *   Reload
    *   Home (navigates to a simple, clean start page)
*   **Content-Focused Display:** Web pages are rendered by the QWebEngineView (based on Chromium's engine), aiming for good compatibility with modern web standards (HTML, CSS, basic JavaScript).
*   **Dynamic Window Title:** The browser window title updates to reflect the title of the current webpage.
*   **Basic Pop-up Control:** Attempts to suppress pop-up windows opened by JavaScript.
*   **Plugin-Free:** Common browser plugins are disabled to maintain a lean environment.
*   **Basic Error Page:** Displays a simple error message if a page fails to load.

## Prerequisites

*   **Python 3.x**
*   **PyQt5 and PyQtWebEngine:** These Python bindings for the Qt framework are essential.

## Installation

1.  **Ensure Python 3 is installed.**

2.  **Install PyQt5 and PyQtWebEngine:**
    Open your terminal or command prompt and run:
    ```bash
    pip install PyQt5 PyQtWebEngine
    ```
    *   **Note for Linux users:** On some Linux distributions, you might need to install additional Qt development packages if `pip` doesn't fully set them up. For example, on Debian/Ubuntu based systems:
        ```bash
        sudo apt-get install python3-pyqt5.qtwebengine
        ```
        However, try the `pip install` command first as it often works directly.
    *   **Note for Windows/macOS users:** `pip` usually installs pre-compiled binaries that include the necessary Qt components.

3.  **Download the Code:**
    *   Place the `simple_browser` directory (containing `browser.py` and `__init__.py`) into your desired project location.

## How to Run

1.  Open your terminal or command prompt.
2.  Navigate to the directory **containing** the `simple_browser` folder. For example, if `simple_browser` is in `/path/to/project/`, you should be in `/path/to/project/`.
3.  Run the browser application using:
    ```bash
    python -m simple_browser.browser
    ```
    Alternatively, if your `simple_browser` directory contains a `main.py` or similar entry script that imports and runs the browser, you would run that. (The current structure assumes direct execution of `browser.py` as the main script).

    If you are inside the `simple_browser` directory itself, you can run:
    ```bash
    python browser.py
    ```

## Usage

*   The browser window will open, displaying a simple start page.
*   **URL Bar:** Type or paste a web address into the text field at the top and press `Enter` to navigate.
*   **Buttons:**
    *   `< Back`: Navigates to the previous page in your history.
    *   `Forward >`: Navigates to the next page in your history (if you've gone back).
    *   `Reload`: Refreshes the current page.
    *   `Home`: Returns to the initial simple start page.

## Known Limitations & Considerations

*   **Highly Simplified:** This browser intentionally lacks many features found in modern commercial browsers, such as:
    *   Bookmarks
    *   Detailed history management
    *   Extensions / Add-ons
    *   Advanced developer tools
    *   Complex settings and preferences
    *   Downloads management (files linked for download might behave unpredictably or try to open externally depending on OS and QtWebEngine defaults).
*   **JavaScript Pop-ups:** While `JavascriptCanOpenWindows` is set to `false`, very persistent or creatively coded JavaScript might still find ways to show overlays or alerts within the page. True immunity is hard.
*   **Ad Blocking:** No built-in ad-blocking is implemented in this MVP.
*   **Security:** QWebEngine is based on Chromium and receives security updates, but a custom browser application built on top of it is only as secure as its weakest link and the diligence of its developer. This PoC is not hardened for use in high-risk environments without further security auditing.
*   **Single Process (Typically):** QtWebEngine may use multiple processes under the hood for rendering, but the Python application itself is single-threaded unless explicitly coded otherwise. Very heavy pages could make the UI feel sluggish during load.

## File Structure
```
your_project_directory/
└── simple_browser/
    ├── __init__.py     # Makes 'simple_browser' a Python package
    └── browser.py      # The main application script for the browser
└── README_simple_browser.md # This documentation file
```

## Future Enhancements (Potential)

*   User-configurable home page.
*   Basic bookmarking system.
*   Tabbed browsing (would increase complexity).
*   A dedicated full-screen/content-only mode that hides all UI chrome.
*   More robust ad/tracker blocking via request interception.
*   Customizable blocklists.
*   Basic history accessible via a simple dropdown.
```
