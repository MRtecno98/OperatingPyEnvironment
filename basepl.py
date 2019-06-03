#! oa_py

import oapi, os

def bytesize_to_formatted_string(size) :
    units = {0 : "B",
             1 : "KB",
             2 : "MB",
             3 : "GB",
             4 : "TB"}
    unit = 0
    while size > 1024 :
        if unit == 4 :
            break
        unit+=1
        size = size / 1024
    return str(round(size)) + units[unit]
    

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
        
        print("\nTotal Size: {0}".format(bytesize_to_formatted_string(totalsize)))
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

class SIZE(oapi.Command) :
    def get_keyword() :
        return "size"

    def process(self, *args) :
        path = "."
        if args :
            path = args[0]
        if not os.path.exists(path) :
            print(path + ": No such file or directory")
            return False
        path = os.path.abspath(path)
        size = 0
        if os.path.isfile(path) :
            size = os.path.getsize(path)
            print("{0} {1}".format("File", os.path.basename(path)))
        else :
            for i in os.listdir(path) :
                size += os.path.getsize(path + \
                                        (os.sep if not path.endswith(os.sep) else "") \
                                        + i)
            print("{0} {1}".format("Directory", os.path.basename(path)))
        print("Size: {0}".format(bytesize_to_formatted_string(size)))
        return True

class RELOAD(oapi.Command) :
    def get_keyword() :
        return "reload"

    def process(self, *args) :
        self.console.reload()

class SET(oapi.Command) :
    def get_keyword() :
        return "set"

    def process(self, *args) :
        if not args :
            print("set: variable not found")
            return False
        if len(args) == 1 :
            if not self.console
            .del_var(args[0]) :
                print(args[0] + ": no such variable")
                return False
        else :
            self.console.set_var(args[0], args[1])
        return True

class GET(oapi.Command) :
    def get_keyword() :
        return "get"

    def process(self, *args) :
        if not args :
            print("\n".join(
                [str(k) + ": " + str(v)
                 for k,v in self.console.get_vars().items()]))
            return True
        if not self.console.exists_var(args[0]) :
            print(args[0] + ": no such variable")
            return False
        print(self.console.get_var(args[0]))
        return True
        
oapi.register_api("Base plugin",
                  "This plugins contains basic commands for the system",
                  "MRtecno98",
                  "1.1.1",
                  [LS, EXIT, CD, SIZE, RELOAD, GET, SET])
