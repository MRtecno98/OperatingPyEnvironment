import threading, time

def delay_func(func, delay) :
    def delayed(*args, **kwargs) :
        time.sleep(delay)
        return func(*args, **kwargs)
    return delayed

class DaemonsController() :
    def __init__(self) :
        self.load_reg()

    def generate_pid(self) :
        i = 0
        while True :
            if i not in self.get_registered_pids() :
                return i
            i+=1
    
    def load_reg(self) :
        self._processes = {}
    
    def start_daemon(self, name, func, repeat=False, delay=3, args=(), kwargs=None) :
        t = threading.Thread(target=delay_func(func, delay), name=name, args=args, kwargs=kwargs)
        t.setDaemon(True)
        pid = self.generate_pid()
        self._processes[pid] = t
        t.start()
        return pid

    def get_daemon_thread(self, pid) :
        return self._processes[pid]

    def get_daemons(self) :
        return self._processes.copy()

    def get_registered_pids(self) :
        return list(self._processes.keys())

    def unreg_daemon(self, pid) :
        return self._processes.pop(pid, None)

    def clear_terminated_daemons(self) :
        for pid in list(self._processes.keys()) :
            t = self.get_daemon_thread(pid)
            if not t.is_alive() :
                self.unreg_daemon(pid)
                
