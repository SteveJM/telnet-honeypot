import threading
import tftpy, wget, hashlib, os, re
from time import time
from responses import responses

# Class for handling connections. This will be used to create threads
class ClientConnection(threading.Thread):
    def __init__(self, conn):
        super(ClientConnection, self).__init__()
        self.conn = conn
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def isStopped(self):
        return self._stop_event.is_set()

    def run(self):
        # Output for captured file
        if os.path.isfile("/tmp/out"):
            os.remove("/tmp/out")
        # Force a number of Login attempts
        attempts = 5
        print("[+] Performing login loop.")
        while attempts > 0 and not self.isStopped():
            #Sending message to connected client
            self.conn.send(bytearray('Login: ', 'utf-8')) #send only takes string
            user = self.conn.recv(1024).decode('utf-8').strip()
            self.conn.send(bytearray('Password: ', 'utf-8')) #send only takes string
            password = self.conn.recv(1024).decode('utf-8').strip()
            print("    User:" + user + " Password:" + password)
            attempts -= 1
        
        if len(user) == 0:
            return    # We've just got newlines.

        # The user has successfully loggin in ;-)
        sequence = 0
        prompt = "/ # "
        buffer = ""
        datafile = False
        startConn = int(time() * 1000)
        left = ""    # Tail from previous receive buffer

        # Now interact with the logged in user
        while not self._stop_event.isSet():
            if sequence == 4:
                elapsed = int(time() * 1000) - startConn
                if elapsed > 2000:
                    print("[+] Human Detected (" + str(elapsed) + ")")
                    break
                else:
                    print("[+] Bot Detected (" + str(elapsed) + ")")
            self.conn.send(bytearray(user + prompt, 'utf-8'))
            response = left + self.conn.recv(10000).decode()
            cmds1 = response.split("\n")    # Commands are line delimited
            if response[-1:] != '\n':
                left = cmds1.pop()
            else:
                left = ""
            for cmd1 in cmds1:
                cmds2 = cmd1.split(";")      # Multiple commands on a single line
                for cmd2 in cmds2:
                    cmd3 = cmd2.strip(";\t \r\n")
                    if len(cmd3) == 0:
                        continue
                    if cmd3 == "sh":
                        continue
                    if cmd3.startswith("exit"):
                        self.stop()
                        break
                    elif cmd3 == "cat /proc/mounts":
                        self.conn.send(bytearray(responses["mounts"], 'utf-8'))
                        print("[+] Sent mounts")
                    elif cmd3.startswith("cd "):
                        opts = cmd3.split()
                        prompt = opts[1] + " # "
                    elif cmd3.startswith("/bin/busybox"):
                        opts = cmd3.split()
                        self.conn.send(bytearray(opts[1] + ": applet not found\n", 'utf-8'))
                        print("[+] Sent applet error")
                    elif cmd3.startswith("dd "):
                        buffer = responses["dd"]
                    elif cmd3.startswith("do echo"):
                        self.conn.send(buffer)
                        print("[+] Sent data")
                        buffer = b''
                    elif cmd3 == "tftp":
                        self.conn.send(bytearray(responses["tftp"], 'utf-8'))
                        print("[+] Sent tftp usage")
                    elif cmd3 == "wget":
                        self.conn.send(bytearray(responses["wget"], 'utf-8'))
                        print("[+] Sent wget usage")
                    elif cmd3.startswith("tftp "):
                        opts = cmd3.split()
                        for opt in opts[1:]:
                            if opt.startswith("-r"):
                                remote = opt[2:]
                            elif not opt.startswith("-"):
                                parts = opt.split(":")
                                host = parts[0]
                                port = int(parts[1])
                        tc = tftpy.TftpClient(host, port)
                        tc.download(remote, "/tmp/out")
                        datafile = True
                        print("[+] tftp: " + host + ":" + str(port) + "/" + remote)
                    elif cmd3.startswith("wget "):
                        opts = cmd3.split()
                        url = opts[1]
                        wget.download(url, out="/tmp/out")
                        datafile = True
                        print("[+] wget: " + url + " to /tmp/out")
                    elif cmd3.startswith("echo -ne "):
                        # An attempt to echo the data to a file.
                        # Currently ignored as we don't seem t get all of the
                        # Data echo'd
                        data = re.search("\"([^\"]*)", cmd3)
                        b = data.group(1)
                        with open("/tmp/echo", "ab") as f:
                            for v in b:
                                f.write(bytes[ord(v)])
                    elif cmd3.startswith("chmod") and datafile:
                        hasher = hashlib.sha1()
                        with open("/tmp/out", "rb") as f:
                            buf = f.read()
                            hasher.update(buf)
                        outfile = hasher.hexdigest()
                        if not os.path.isfile("samples/" + outfile):
                            os.rename("/tmp/out", "samples/" + outfile)
                            print("[+] New Sample: ", outfile)
                        else:
                            print("[-] Sample exists!")
                        datafile = False
                    else:
                        print("[-] Ignored command: " + cmd3)
                sequence += 1
                if sequence == 10:
                    break
        
