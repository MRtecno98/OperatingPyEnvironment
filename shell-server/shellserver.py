import threading
import socketserver
import kbhit
import sys
import io
import os

SHELL_PATH = r".."
ADDRESS = ("localhost", 9182)

sys.path.append(os.path.abspath(SHELL_PATH))
import operating_environment as oenv

def build_input_function(stream=sys.stdin, prompt_stream=sys.stdout) :
    def stream_input(prompt=None, stream=stream, prompt_stream=prompt_stream) :
        if prompt : print(prompt, end='', file=prompt_stream, flush=True)
        return stream.readline()[:-1]
    return stream_input

def build_print_function(stream=sys.stdout) :
    def stream_print(*value, sep='', end='\n', file=stream, flush=False) :
        return print(*value, sep=sep, end=end, file=file, flush=flush)
    return stream_print

class ThreadedShellRequestHandler(socketserver.BaseRequestHandler):
    def setup(self):
        request = self.request
        class INStream(io.TextIOBase) :
            def readline(self) :
                line = b''
                c = b''
                while c.decode() != "\n" :
                    c = request.recv(1)
                    line+=c
                return line.decode()

        class OUTStream(io.TextIOBase) :
            def write(self, str) :
                request.send(str.encode())
        
        self.instream = INStream()
        self.outstream = OUTStream()        
        self.console = oenv.Console()
        self.console.add_to_path(SHELL_PATH)
        
        print('\n{}:{} connected\n'.format(*self.client_address))
    
    def handle(self):
        print = build_print_function(stream=self.outstream)
        input = build_input_function(stream=self.instream,
                                     prompt_stream=self.outstream)

        oldstdin, oldstdout = sys.stdin, sys.stdout
        sys.stdin, sys.stdout = self.instream, self.outstream
        try :
            self.console.load_and_start()
        finally :
            sys.stdin, sys.stdout = oldstdin, oldstdout
        return

    def finish(self):
        self.request.sendall("connection_closed".encode())
        print('\n{}:{} disconnected\n'.format(*self.client_address))

class ThreadedShellServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, *args, **kwargs) :
        socketserver.TCPServer.__init__(self, *args, **kwargs)
        self.enabled = True
    
    def serve_forever(self) :
        while self.enabled :
            self.handle_request()
        return

    def serve_async(self) :
        t = threading.Thread(target=server.serve_forever)
        t.setDaemon(True) # don't hang on exit
        t.start()
        self.thread = t

    def stop(self) :
        self.enabled = False
        self.socket.close()

if __name__ == '__main__':
    import socket
    import threading
    
    server = ThreadedShellServer(ADDRESS, ThreadedShellRequestHandler)

    server.serve_async()
    print("Server started on %s:%s" % server.server_address)
    print('Server loop running in thread:', server.thread.getName())
    print()

    kb = kbhit.KBHit()

    command = ""
    while server.enabled :
        try :
            c = kb.getch()
        except :
            continue

        if ord(c) == 8 : # BACKSPACE
            print("\b \b", end='', flush=True)
            command = command[:-1]
            continue

        if ord(c) == 13 : # ENTER
            print("\n", end='', flush=True)

            if command == "stop" :
                server.stop()
                print("Server stopped")

            print()
            command = ""
            continue

        command+=chr(ord(c))
        print(chr(ord(c)), end='', flush=True)
