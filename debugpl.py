#! oa_py

import oapi, traceback, sys

class EXEC(oapi.Command) :
    def get_keyword() :
        return "exec"

    def process(self, *args) :
        if not args :
            return True
        
        r = None
        try :
            r = eval(" ".join(args))
        except Exception as e :
            try :
                r = exec(" ".join(args))
            except Exception as e :
                print("".join(traceback.format_exception(\
                    etype=type(e), value=e, tb=e.__traceback__)),
                    file=sys.stderr, end='')
            
        if r :
            print(r)
        return True

oapi.register_api("Debug Plugin",
                  "This plugin contains commands usefuls for debug",
                  "MRtecno98",
                  "1.0.0",
                  [EXEC])
