#! oa_py

import oapi

class LS(oapi.Command) :
    def get_keyword() :
        return "ls"

    def process(self, *args) :
        print("LS Executed!")
        return True

class EXIT(oapi.Command) :
    def get_keyword() :
        return "exit"

    def process(self, *args) :
        self.console.terminate()
        return True

oapi.register_api("Base plugin",
                  "This plugins contains basic commands for the system",
                  "MRtecno98",
                  "1.1.1",
                  [LS, EXIT])
