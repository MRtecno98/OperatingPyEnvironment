#! oa_py

import oapi, os, sys

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
            if not self.console \
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

class ECHO(oapi.Command) :
    def get_keyword() :
        return "echo"

    def process(self, *args) :
        if not args :
            print("echo")
        else :
            print(" ".join(args))
        return True

class CLEAR(oapi.Command) :
    def get_keyword() :
        return "clear"

    def process(self, *args) :
        systems = self.console.systems
        syst = systems.get_current_sys()

        if systems.is_running_idle() :
            print("clear: Clear screen not supported in IDLE")
            return False
        
        print("clear: Clear screen is not supported on your shell")
        
        if syst == systems.System.WIN :
            os.system("cls")
        elif syst in (systems.System.MAC, systems.System.LIN) :
            os.system("clear && printf '\e[3J'")

        return True

class VERSION(oapi.Command) :
    def get_keyword() :
        return "version"

    def process(self, *args) :
        print()
        print(self.console.title())

        return True

class PLUGINS(oapi.Command) :
    DESCRIPTION_MAX_WORDS = 8
    
    def get_keyword() :
        return "plugins"

    def process(self, *args) :
        verbose = "--verbose" in args
        
        for i in self.console.plugins :
            desc = i["pl_desc"].split()
            desc_max = self.DESCRIPTION_MAX_WORDS
            desc_reorg = [" ".join(desc[i:i+desc_max])
                          for i in range(0, len(desc), desc_max)]

            if not verbose :
                print(i["pl_name"] + " [v." + i["version"] + "]")
            else :
                print(i["pl_name"] + ":")
                print("    Description: " +
                     ("\n" + (" " * 17)).join(desc_reorg))
                print("    Version: " + i["version"])
                print("    Author: " + i["author"])
                print()
                
        return True
        
oapi.register_api("Base plugin",
                  "This plugins contains basic commands for the system",
                  "MRtecno98",
                  "1.3.4",
                  [LS, EXIT, CD, SIZE, RELOAD, GET, SET, ECHO, CLEAR, VERSION,
                   PLUGINS])
