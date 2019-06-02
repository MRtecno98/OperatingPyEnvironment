#! oa_py

import oapi, os

class LS(oapi.Command) :
    def get_keyword() :
        return "ls"

    def process(self, *args) :
        if args :
            if os.path.isdir(args[0]) :
                path = args[0]
            else :
                print(args[0] + ": No such directory")
                return False  
        else : path = "."
        
        files = os.listdir(os.path.abspath(path))
        totalsize = 0
        print(".\n..")
        for file in files :
            if os.path.isfile(os.path.abspath(path) + os.sep + file) :
                print(file)
            else :
                print(file + os.sep)
            totalsize += os.path.getsize(os.path.abspath(path) + os.sep + file)
        print("\nTotal Size: " + str(totalsize) + "B")
        return True

class CD(oapi.Command) :
    def get_keyword() :
        return "cd"

    def process(self, *args) :
        if not args :
            print(self.console.get_working_dir())
            return True
        path = args[0]
        if os.path.isdir(path) :
            self.console.set_working_dir(path)
            return True
        elif os.path.isfile(path) :
            print(path + ": Not a directory")
        else :
            print(path + ": No such file or directory")

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
                  [LS, EXIT, CD])
