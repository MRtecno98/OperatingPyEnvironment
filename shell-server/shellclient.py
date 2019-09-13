import socket, kbhit, threading, sys

DEFAULT_PORT = 9182
MAX_HISTORY = 10

splitted = input("Insert address: ").split(":")
ip, port = splitted[0], (int(splitted[1])
                          if len(splitted) > 1 else DEFAULT_PORT)

kb = kbhit.KBHit()

# Connect to the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s :
    s.connect((ip, port))
    
    connected = True

    def receiver() :
        global connected
        while connected :
            try :
                response = s.recv(1024).decode()

                if response == "connection_closed" :
                    print("Connection succesfully closed")
                    print("Press ENTER to terminate")
                    connected = False
                    return
            
                if response != "" : print(response, end='', flush=True)
            
            except ConnectionAbortedError :
                print("RECEIVER: Connection remotely closed")
                connected = False
                sys.exit(0)
                break
            except KeyboardInterrupt :
                print("Closing")
                connected = False
                sys.exit(0)
                break

    recvthread = threading.Thread(target=receiver)
    recvthread.setDaemon(True)
    recvthread.start()

    history = []
    offset = 0
    command = ""
    try :
        while connected :
            try :
                c = kb.getch()
            except :
                """
                try :
                    a = kb.getarrow()
                    print("ARROW: " + str(a))
                except :
                    continue

                if a == 0 :
                    offset+=1
                elif a == 2 :
                    offset-=1
                if offset < 0 : offset = 0

                hist = list(history) + ""
                hist.reverse()
                res = hist[offset] if offset < len(hist) else hist[-1]

                print("\b \b"*len(command), end='', flush=True)
                command = res
                print(command, end='', flush=True)
                """
                continue

            if ord(c) == 8 : # BACKSPACE
                if not len(command) < 1 :
                    print("\b \b", end='', flush=True)
                    command = command[:-1]
                continue

            if ord(c) == 13 : # ENTER
                print("\n", end='', flush=True)

                s.sendall((command + "\n").encode())

                # if len(history) == 0 or history[-1] != command :
                #     history.append(command)
                # if len(history) > MAX_HISTORY : history = history[-MAX_HISTORY:]
                command = ""
                continue

            command+=chr(ord(c))
            print(chr(ord(c)), end='', flush=True)
    except ConnectionAbortedError :
        print("Connection remotely closed")
        connected = False
        sys.exit(0)
    except KeyboardInterrupt :
        print("Closing")
        connected = False
        sys.exit(0)
        
