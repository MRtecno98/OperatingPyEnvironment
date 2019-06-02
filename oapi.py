from abc import ABC, abstractmethod

OAPI_META = {"version" : "1.3.0",
             "author" : "MRtecno98"}

api_data = {}

class Command(ABC) :
    def __init__(self, console) :
        self.console = console
    
    @staticmethod
    @abstractmethod
    def get_keyword() :
        pass
    
    @abstractmethod
    def process(self, *args) :
        pass

    def tooltip(self) :
        return 

def register_api(plugin_name , #string
                 plugin_desc , #string
                 author      , #string
                 version     , #string
                 classes     ) : #list of classes
    global api_data
    for clazz in classes :
        api_data[clazz] = {"pl_name" : plugin_name,
                           "pl_desc" : plugin_desc,
                           "author"  : author,
                           "version" : version}
    
