#! oa_py

import oapi, os, shutil, traceback

class TOUCH(oapi.Command) :
    def get_keyword() :
        return "touch"

    def help() :
        return "TOUCH Command, creates an empty file\n" + \
               "\nUsage: touch <filename>"

    def process(self, *args) :
        if not args :
            print("touch: illegal args")
            return False
        open(args[0], "w").close()
        return True

class MKDIR(oapi.Command) :
    def get_keyword() :
        return "mkdir"

    def help() :
        return "MKDIR Command, creates a directory path\n" + \
               "\nUsage: mkdir <path>"

    def process(self, *args) :
        if not args :
            print("mkdir: illegal args")
            return False
        os.makedirs(args[0], exist_ok=True)
        return True

class RM(oapi.Command) :
    def get_keyword() :
        return "rm"

    def help() :
        return "RM Command, deletes a file or a folder recursively\n" + \
               "\nUsage: rm <path>"

    def process(self, *args) :
        if not args or (not os.path.exists(args[0])) :
            print("rm: no such file or directory")
            return False
        try :
            path = os.path.abspath(args[0])
            if os.path.isfile(path) :
                os.remove(path)
            else :
                shutil.rmtree(path, ignore_errors=True,
                              onerror=lambda fnc, path, exc : \
                              print(path + ": " + ",".join(exc[1].args)))
            return True
        except Exception as e :
            print("".join(traceback.format_exception( \
                etype=type(e), value=e, tb=e.__traceback__)))
            return False

class CAT(oapi.Command) :
    def get_keyword() :
        return "cat"

    def help() :
        return "CAT Command, displays the content of a file\n" + \
               "\nUsage: cat <file>"

    def process(self, *args) :
        if not args or (not self.console.files.is_text(
                            os.path.abspath(args[0]))) :
            print("cat: no such file")
            return False
        with open(os.path.abspath(args[0])) as file :
            print(file.read())
        return True

oapi.register_api("EoE Files",
                  "EoE File operating plugin, contains commands for " +
                  "filesystem manipulation.",
                  "MRtecno98",
                  "1.0.0",
                  [TOUCH, MKDIR, RM, CAT])
