#! oa_py

import oapi

class LS(oapi.Command) :
    def get_keyword(self) :
        return "ls"

    def process(self, args) :
        print("LS Executed!")
        return 0

oapi.register_api("Base plugin",
                  "This plugins contains basic commands for the system",
                  "MRtecno98",
                  "1.0.0",
                  [LS])
