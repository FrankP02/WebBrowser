import sys
import os
#from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QLineEdit
#from PyQt5.QtWebEngineWidgets import QWebEngineView
#from PyQt5.QtCore import QUrl
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtWebEngineWidgets import * 
from PyQt5.QtPrintSupport import * 

#todo: better visuals

class BrowserTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.layout.addWidget(self.browser)
        self.setLayout(self.layout)
class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Browser")
        #todo: change into default resolution
        self.setGeometry(0,0,1920, 1200)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.setCentralWidget(self.browser)

        # Navigation bar
        nav_bar = QToolBar()
        self.addToolBar(nav_bar)

        # Back button
        back_btn = QAction("◀", self)
        back_btn.triggered.connect(self.browser.back)
        nav_bar.addAction(back_btn)

        # Forward button
        forward_btn = QAction("▶", self)
        forward_btn.triggered.connect(self.browser.forward)
        nav_bar.addAction(forward_btn)

        # adding stop action to the tool bar
        stop_btn = QAction("X", self)
        stop_btn.setStatusTip("Stop loading current page")
        # adding action to the stop button
        # making browser to stop
        stop_btn.triggered.connect(self.browser.stop)
        nav_bar.addAction(stop_btn)

        # Reload button
        reload_btn = QAction("⟳", self)
        reload_btn.triggered.connect(self.browser.reload)
        nav_bar.addAction(reload_btn)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
