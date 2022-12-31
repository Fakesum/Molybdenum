from PyQt5.QtWidgets import QMainWindow as __QMainWindow
import multiprocess as __mp
from .stages import Stages

# QT Brower class
class Molybdenum(__QMainWindow, __mp.Process):
    """Molydenum

    Args:
        __QMainWindow (_type_): _description_
        __mp (_type_): _description_
    """
    from PyQt5.QtCore import QUrl as __QUrl

    IURL = "https://www.google.com"

    def __init__(self, headless=False, egar=False) -> None:
        from PyQt5.QtWebEngineWidgets import QWebEngineView as __QWebEngineView
        from PyQt5.QtWidgets import QApplication

        # config for QT application
        qt_options = ['--enable-smooth-scrolling']
        import os

        if os.name == 'posix':
            qt_options.extend(["--disable-gpu", "--no-sandbox"])
        
        self.qt_app: QApplication = QApplication(qt_options)
        self.qt_app.setApplicationName("QTSpider")

        if headless:
            if os.name != 'posix':
                raise RuntimeError("Headless Mode Not Supported For non-linux devices")
            from pyvirtualdisplay.display import Display
            display = Display()
            display.start()
        super(globals()["__QMainWindow"], self).__init__()
        super(globals()["__mp"].Process, self).__init__()
        self.daemon = True
        self.browser: __QWebEngineView = __QWebEngineView()
        
        self.stages = Stages()
        self.stages.egar = egar

        self.get(self.IURL)

        self.setCentralWidget(self.browser)
        self.show()
    
    def get(self, url) -> None:
        def wrapper():
            self.browser.setUrl(self.__QUrl(url))
        self.stages.register_func(wrapper)
    
    def start(self, wait=False):
        self.stages.browser_register(self.browser)
        super(globals()["__mp"].Process, self).start()
        if wait:
            import time
            while True:
                time.sleep(1)
        
    def javascript(self, script: str) -> None:
        def wrapper():
            self.browser.page().runJavaScript(script)
        self.stages.register_func(wrapper)
    
    def javascriptFromFile(self, script_file: str) -> None:
        def wrapper():
            self.browser.page().runJavaScript(open(script_file, "r").read())
        self.stages.register_func(wrapper)

    def run(self):
        self.qt_app.exec()