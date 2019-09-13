from abc import ABC, abstractmethod

OAPI_META = {"version" : "1.5.0",
             "author" : "MRtecno98"}

api_data = {}

class NULL() :
    pass

class Addon(ABC) :
    def __init__(self, console) :
        self.console = console

class Command(Addon) :
    @staticmethod
    @abstractmethod
    def get_keyword() :
        pass
    
    @abstractmethod
    def process(self, *args) :
        pass

    @staticmethod
    def help() :
        return "Generic command\n" + \
               "\nUsage: command <args>"

class Listener(Addon) :
    pass

class Event() :
    pass

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
    
