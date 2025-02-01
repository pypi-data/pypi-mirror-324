# THIS CODE IS MEANT TO BE PASTED INSIDE OF HOUDINI!

import socket

host = "127.0.0.1"
port = 5000

def stop_houdini_server():
    """Sends a stop command to the Houdini socket server."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send("STOP_SERVER".encode())  # Special shutdown command
    client.close()

stop_houdini_server()