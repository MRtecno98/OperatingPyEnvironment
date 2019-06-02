import os, platform, enum, mimetypes, directimport, wrappers, oapi

class Systems() :
    class System(enum.Enum) :
        WIN = 0
        LIN = 1
        MAC = 2

        def __repr__(self) :
            return "<System: " + self.name + ">"

    @staticmethod
    def get_sys_list(legacy=False) :
        return [e.name if e.name != "MAC" else "DAR" if legacy else "MAC"
                for e in Systems.get_sys_listSystem]
    
    @staticmethod
    def get_sys_map(legacy=False) :
        return {e.name if e.name != "MAC" else "DAR" if legacy else "MAC"
                : e for e in Systems.System}
    
    @staticmethod
    def get_current_sys() :
        return Systems.get_sys_map(legacy=True)[platform.system()[:3].upper()]

    @staticmethod
    def get_pathvar_sep() :
        return ";" if Systems.get_current_sys() is Systems.System.WIN else ":"

class Files() :
    @staticmethod
    def is_text(file) :
        type = mimetypes.guess_type(os.path.abspath(file))[0]
        return (type.split("/")[0] == "text") if type != None else False

class Shebang() :
    OA_SHEBANG = "oa_py"
    
    @staticmethod
    def parse_shebang(line) :
        split = line.replace("\n", "").split()
        if split[0] == "#!" :
            return " ".join(split[1:])

    @staticmethod
    def check_shebang(line) :
        return Shebang.parse_shebang(line) == Shebang.OA_SHEBANG
    

class Console() :
    def __init__(self) :
        self._wd = os.getcwd()
        self.path = os.environ['PATH'] + Systems.get_pathvar_sep() + self._wd
        self.commands = []
        self._vars = {"EXEC" : True, "ON" : True}

    def get_working_dir(self) :
        return self._wd

    def set_working_dir(self, d) :
        os.chdir(os.path.abspath(d))
        self._wd = d

    def get_var(self, name) :
        return self._vars[name]

    def set_var(self, name, value) :
        self._vars[name] = value

    def get_vars(self) :
        return self._vars.copy()

    def get_plug_files(self) :
        files = []
        cc = 0
        for direct in self.path.split(Systems.get_pathvar_sep()) :
            if os.path.exists(direct) :
                for fil in os.listdir(direct) :
                    cc+=1
                    filpath = direct + \
                              (os.sep if not direct.endswith(os.sep) else "") + \
                              fil
                    try :
                        if os.path.getsize(filpath) < \
                            500 * 1024 * 1024 * 1024 : #500 MB max size
                            if Files.is_text(filpath) :
                                if fil.endswith(".py") :
                                    with open(filpath, "r") as file :
                                        lines = file.readlines() + [""]
                                    if Shebang.check_shebang(lines[0]) :
                                        files.append(filpath)
                    except :
                        continue
        return files, cc

    def load_plugins(self, log=True) :
        if log : print("Loading plugins")
        files, count = self.get_plug_files()
        if log : print("Found {0} plugin with {1} files checked".format(len(files), count))
        for f in files :
           m = directimport.import_mod(os.path.dirname(f), \
                                       os.path.splitext(os.path.basename(f))[0])
           api_data = m.oapi.api_data

           count = 0
           for clazz in list(api_data.keys()) :
                if issubclass(clazz, oapi.Command) :
                    self.commands.append(wrappers.PluginClass(clazz, api_data[clazz]))
                count+=1
               
        if log : print("Loaded {0} class{1}".format(count,
                                                   ("es" if count > 1 else "")))

    def credits(self) :
        crd = "EoE Operative Environment [Version 1.2.035]\n" + \
              "(c) 2019 MRtecno98. MIT License (bit.ly/2Z5tcbT)"

        return crd

    def load_and_start(self) :
        self.load_plugins()
        self.start()

    def terminate(self) :
        self.set_var("ON", False)
    
    def start(self) :
        print()
        print(self.credits())
        print()

        while self.get_var("ON") :
            cmd = input(self.get_working_dir() + "> ")

            if cmd != "" :
                s_cmd = cmd.split()

                keyword = s_cmd[0].lower()
                for plcl in self.commands :
                    res = False
                    if keyword == plcl.clazz.get_keyword() :
                        inst = plcl.clazz(self)

                        res = inst.process(cmd[1:])
                        print()
                        break
                self.set_var("EXEC", bool(res))


if __name__ == "__main__" :
    Console().load_and_start()
            
                            
                            

    
