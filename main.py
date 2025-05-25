import sys
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
        self.setGeometry(0,0,420, 420)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.create_navbar()
        self.add_new_tab(QUrl("https://google.com"), "New Tab")

    def create_navbar(self):
        # Navigation bar
        nav_bar = QToolBar()
        self.addToolBar(nav_bar)

        # Back button
        back_btn = QAction("◀", self)
        back_btn.triggered.connect(self.navigate_back)
        nav_bar.addAction(back_btn)

        # Forward button
        forward_btn = QAction("▶", self)
        forward_btn.triggered.connect(self.navigate_forward)
        nav_bar.addAction(forward_btn)

        # adding stop action to the tool bar
        #stop_btn = QAction("X", self)
        #stop_btn.setStatusTip("Stop loading current page")
        # adding action to the stop button
        # making browser to stop
        #stop_btn.triggered.connect(self.browser.stop)
        #nav_bar.addAction(stop_btn)

        # Reload button
        reload_btn = QAction("⟳", self)
        reload_btn.triggered.connect(self.reload_page)
        nav_bar.addAction(reload_btn)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

        #New Tab
        new_tab_btn = QAction("+",self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab(QUrl("https://www.google.com"), "New Tab"))
        nav_bar.addAction(new_tab_btn)

        self.tabs.currentChanged.connect(self.update_url_bar)

    def add_new_tab(self, qurl, label):
        new_tab = BrowserTab()
        new_tab.browser.setUrl(qurl)
        index = self.tabs.addTab(new_tab, label)
        self.tabs.setCurrentIndex(index)
        new_tab.browser.urlChanged.connect(lambda qurl, browser=new_tab.browser: self.update_tab_title(browser))

    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        current_browser = self.current_browser()
        current_browser.setUrl(QUrl(url))

    def update_url_bar(self, i):
        q = self.current_browser().url()
        self.url_bar.setText(q.toString())
    
    def update_tab_title(self, browser):
        index = self.tabs.indexOf(browser.parent())
        if index != -1:
            self.tabs.setTabText(index, browser.page().title())
    
    def navigate_back(self):
        self.current_browser().back()

    def navigate_forward(self):
        self.current_browser().forward()

    def reload_page(self):
        self.current_browser().reload()

    def current_browser(self):
        return self.tabs.currentWidget().browser


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
