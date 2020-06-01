#!/usr/bin/env python3
import sys, signal, time
from socket import socket, AF_INET, SOCK_STREAM
import connection

sock = None
client = None

def exit_gracefully(signal, frame):
    if client is not None:
        print("Stopping client thread...")
        client.stop()
        try:
            print("Waiting for client to quit...")
            client.join()
        except:
            pass
    if sock is not None:
        sock.close()
    print("All finished.")    
    sys.exit(0)


signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(("192.168.1.147", 2327))
sock.settimeout(300)

# Listen for incoming connections
sock.listen(1)
print("Listening on 192.168.1.147:2327")

# Wait for inbound connection requests.
while 1:
    # Wait to accept a connection - blocking call.
    try:
        conn, addr = sock.accept()
    except OSError:
        continue
    hostname = "unknown"
    try:
        hostname = gethostbyaddr(addr[0])[0]
    except:
        # Reverse DNS failed.
        pass

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time, 'Connected: ' + addr[0] + " (" + hostname + ")")
    
    # Start new thread for the connection.
    try:
        client = connection.ClientConnection(conn)
        client.run()
    except Exception as e:
        print(e)
    finally:
        conn.close()
        client = None
        print("-------------------------------------------------------------")
