from PyQt5.QtWidgets import QMainWindow as __QMainWindow
# Webengine for QT in order to make a browser
from PyQt5.QtWebEngineWidgets import QWebEngineView as __QWebEngineView
# import QUrl type
from PyQt5.QtCore import QUrl as __QUrl

import typing as __typing
import multiprocess as __mp

# QT Brower class
class QTSpider(__QMainWindow, __mp.Process):
    import typing as __typing

    IURI = "https://www.google.com"
    __stages: list[__typing.Callable] = []
    __cstage: int = 0

    def __init__(self):
        from PyQt5.QtWidgets import QApplication

        # config for QT application
        options = ['--enable-smooth-scrolling']
        import os

        if os.name == 'posix':
            options.extend(["--disable-gpu", "--no-sandbox"])
        
        self.qt_app: QApplication = QApplication(options)
        self.qt_app.setApplicationName("QTSpider")

        # from pyvirtualdisplay.display import Display
        # display = Display()
        # display.start()
        super(globals()["__QMainWindow"], self).__init__()
        super(globals()["__mp"].Process, self).__init__()
        self.browser = globals()["__QWebEngineView"]()

        self.get(self.IURI)

        self.setCentralWidget(self.browser)
        self.show()
    
    def get(self, url):
        self.browser.setUrl(globals()["__QUrl"](url))
    
    def javascript(self, script: str) -> None:
        self.browser.page().runJavaScript(script)
    
    def javascriptFromFile(self, script_file: str) -> None:
        self.browser.page().runJavaScript(open(script_file, "r").read())

    def register_stage(self, stage:__typing.Callable) -> None:
        def wrapper():
            nurl = stage()
            
            self.browser.loadFinished.disconnect(self.__stages[self.__cstage])

            self.__cstage += 1

            try:
                self.browser.loadFinished.connect(self.__stages[self.__cstage])
            except IndexError:
                pass
            (self.get(nurl) if nurl != None else None)
        if self.__stages.__len__() == 1:
            self.browser.loadFinished.connect(self.__stages[0])
        self.__stages.append(wrapper)
    
    class Extensions:
        class Recaptcha:
            @staticmethod
            def solve(self):
                self.javascript("""console.log(document.querySelector("[title='reCAPTCHA']").contentDocument.querySelector(".recaptcha-checkbox-border").click())""")

    def run(self):
        self.qt_app.exec()

if __name__ == "__main__":
    class YTSpider(QTSpider):
        IURI = "https://www.youtube.com/"

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            self.register_stage(self.stage0)
            self.register_stage(self.stage1)

        def stage0(self):
            print("REACHED")
            return "https://www.google.com"
        
        def stage1(self):
            print("SUPER REACHED")
    YTSpider().start()
    
    import time
    while True:
        time.sleep(1)