# 定义浅色 QSS样式表
LIGHT_THEME = """
QWidget {
    background-color: #F5F5F5; /* Light grey background */
    color: #212121; /* Dark text color */
    font-family: "Roboto", "Segoe UI";
    font-size: 10pt; /* Adjusted font size to match ACID_THEME */
}

QPushButton {
    background-color: #FFFFFF; /* White buttons */
    border: 1px solid #CCCCCC; /* Subtle border */
    border-radius: 4px;
    padding: 5px;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #F0F0F0; /* Light grey on hover */
}

QPushButton:pressed {
    background-color: #E0E0E0; /* Darker grey on press */
}

QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #CCCCCC;
    border-radius: 4px;
    padding: 5px;
}

QLineEdit {
    background-color: #FFFFFF;
    border: 1px solid #CCCCCC;
    border-radius: 4px;
    padding: 5px;
}

QStatusBar {
    background-color: #E0E0E0; /* Darker grey status bar */
    color: #212121;
}

QWebEngineView {
    background-color: #FFFFFF; /* White background for web view */
}
"""


# 定义深色 QSS样式表
DARK_THEME = """
QWidget {
    background-color: #333333;
    color: #ffffff;
    font-family: "Segoe UI";
    font-size: 9pt;
}

QPushButton {
    background-color: #555555;
    border: 2px solid #555555;
    border-radius: 5px;
    padding: 5px;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #777777;
}

QPushButton:pressed {
    background-color: #999999;
}

QComboBox {
    background-color: #555555;
    border: 2px solid #555555;
    border-radius: 5px;
    padding: 5px;
}

QLineEdit {
    background-color: #555555;
    border: 2px solid #555555;
    border-radius: 5px;
    padding: 5px;
}

QStatusBar {
    background-color: #222222;
    color: #ffffff;
}

QWebEngineView {
    background-color: #222222;
}
"""

BLUE_THEME = """QWidget {
    background-color: #EAF6FD; /* Light blue background */
    color: #1A3C6D; /* Dark blue text color */
    font-family: "Segoe UI", "Arial";
    font-size: 10pt;
}

QPushButton {
    background-color: #1A75BB; /* Blue buttons */
    border: 1px solid #14639E; /* Darker blue border */
    border-radius: 6px;
    padding: 7px;
    min-width: 100px;
    color: white;
}

QPushButton:hover {
    background-color: #1369A3; /* Darker blue on hover */
}

QPushButton:pressed {
    background-color: #115E99; /* Even darker blue on press */
}

QComboBox,
QLineEdit {
    background-color: #FFFFFF;
    border: 1px solid #B2CCD6; /* Light blue border */
    border-radius: 6px;
    padding: 6px;
    selection-background-color: #C6E2EE; /* Lighter blue selection */
}

QStatusBar {
    background-color: #B2CCD6; /* Light blue status bar */
}

QWebEngineView {
    background-color: #F0F8FF; /* Light blue background for web view */
}
"""


BRET_THEME = """
QWidget {
    background-color: #FFE5B4; /* Light peach background */
    color: #9C451F; /* Dark orange text color */
    font-family: "Copperplate", "Times New Roman";
    font-size: 11pt;
}

QPushButton {
    background-color: #FF8C00; /* Dark orange buttons */
    border: 1px solid #E65C00; /* Slightly darker orange border */
    border-radius: 5px;
    padding: 6px;
    min-width: 95px;
    color: white;
}

QPushButton:hover {
    background-color: #E65C00; /* Slightly darker on hover */
}

QPushButton:pressed {
    background-color: #D35400; /* Even darker on press */
}

QComboBox,
QLineEdit {
    background-color: #FFFFFF;
    border: 1px solid #FFB266; /* Light orange border */
    border-radius: 5px;
    padding: 5px;
    selection-background-color: #FFCC99; /* Light orange selection */
}

QStatusBar {
    background-color: #FFB266; /* Light orange status bar */
}

QWebEngineView {
    background-color: #FFFAF0; /* Creamy background for web view */
}
"""

ACID_THEME = """
QWidget {
    background-color: #E0FFFF; /* Light cyan background */
    color: #008080; /* Teal text color */
    font-family: "Verdana", sans-serif;
    font-size: 10pt;
}

QPushButton {
    background-color: #20B2AA; /* Dark cyan buttons */
    border: 1px solid #008B8B; /* Teal border */
    border-radius: 5px;
    padding: 6px;
    min-width: 95px;
    color: white;
}

QPushButton:hover {
    background-color: #008B8B; /* Teal on hover */
}

QPushButton:pressed {
    background-color: #5F9EA0; /* Darker teal on press */
}

QComboBox,
QLineEdit {
    background-color: #F0FFFF; /* Azure background */
    border: 1px solid #4682B4; /* Steel blue border */
    border-radius: 5px;
    padding: 5px;
    selection-background-color: #87CEFA; /* Light sky blue selection */
}

QStatusBar {
    background-color: #4682B4; /* Steel blue status bar */
}

QWebEngineView {
    background-color: #F0F8FF; /* Alice blue web view background */
}
"""