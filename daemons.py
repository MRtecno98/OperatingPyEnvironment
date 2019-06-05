import threading

class DaemonsController() :
    def __init__(self) :
        self.load_reg()

    def generate_pid(self) :
        i = 0
        while True :
            if i not in self._processes.keys() :
                return i
            i+=1
    
    def load_reg(self) :
        self._processes = {}
    
    def start_daemon(self, name, func, repeat=False, args=(), kwargs=None) :
        t = threading.Thread(target=func, name=name, args=args, kwargs=kwargs)
        t.setDaemon(True)
        pid = self.generate_pid()
        self._processes[pid] = t
        t.start()

    def get_daemon_thread(self, pid) :
        return self._processes[pid]

    def unreg_daemon(self, pid) :
        return self._processes.pop(pid, None)

    def clear_terminated_daemons(self) :
        for pid in self._processes.keys() :
            t = self.get_daemon_thread(pid)
            if not t.is_alive() :
                self.unreg_daemon(pid)
                
