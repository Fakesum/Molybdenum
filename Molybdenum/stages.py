class Stages():
    """A Class to track all the stages
        of the Molybdenum Program
    """
    import typing as __typing
    from PyQt5.QtWebEngineWidgets import QWebEngineView as __QWebEngineView

    __stages: list[list[__typing.Callable]] = [[]]
    __final_stages: list[__typing.Callable] = list()
    __cstage: int = int()
    egar: bool = False

    def register_func(self, stage: __typing.Callable) -> None:
        self.__stages[self.__cstage].append(stage)
    
    def next(self) -> None:
        self.__cstage += 1
    
    def browser_register(self, browser: __QWebEngineView) -> None:
        register = (browser.loadStarted if self.egar else browser.loadFinished)

        amalgmated_stages: list[self.__typing.Callable] = list()
        for stage in self.__stages:
            def wrapper():
                for sub_stage in stage:
                    sub_stage()
            amalgmated_stages.append(wrapper)
        
        for stage in enumerate(amalgmated_stages):
            def wrapper():
                stage[1]()
                
                register.disconnect(stage[1])

                if (stage[0]+1) < self.__final_stages.__len__():
                    register.connect(self.__final_stages[stage[0]+1])
                
            if stage[0] == 0:
                browser.loadFinished.connect(wrapper)
            
            self.__final_stages.append(wrapper)