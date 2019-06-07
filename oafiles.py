#! oa_py

import oapi

class TOUCH(oapi.Command) :
    def get_keyword() :
        return "touch"

    def process(self, *args) :
        if not args :
            print("touch: illegal args")
            return False
        else :
            open(args[0], "w").close()
            return True

oapi.register_api("EoE Files",
                  "EoE File operating plugin, contains commands for " +
                  "filesystem manipulation.",
                  "MRtecno98",
                  "1.0.0",
                  [TOUCH])
