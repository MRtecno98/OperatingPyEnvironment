from abc import ABC, abstractmethod

api_data = {}

class Command(ABC) :
    @abstractmethod
    def get_keyword(self) :
        pass

    @abstractmethod
    def process(self, args) :
        pass


def register_api(plugin_name : str,
                 plugin_desc : str,
                 author      : str,
                 version     : str,
                 classes     : list) :
    global api_data
    for clazz in classes :
        api_data[clazz] = {"pl_name" : plugin_name,
                           "pl_desc" : plugin_desc,
                           "author"  : author,
                           "version" : version}
    
