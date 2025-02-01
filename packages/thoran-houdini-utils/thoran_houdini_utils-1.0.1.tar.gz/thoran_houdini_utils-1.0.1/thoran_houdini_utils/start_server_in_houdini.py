# THIS CODE IS MEANT TO BE PASTED INSIDE OF HOUDINI!

import socket
import threading

# Flag to stop the server
server_running = True  

def houdini_server():
    global server_running

    host = "127.0.0.1"
    port = 5000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow address reuse
    server.bind((host, port))
    server.listen(1)
    print("Houdini server is waiting for a connection...")

    conn, addr = server.accept()  # Wait for VSCode to connect
    print(f"Connected to {addr}")

    while server_running:  # Only run when flag is True
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            if data.strip() == "STOP_SERVER":  # Special shutdown command
                server_running = False
                break

            exec(data, globals())  # Execute the Python command in Houdini
            conn.send("Success".encode())
            
        except Exception as e:
            conn.send(str(e).encode())

    conn.close()
    server.close()
    
    # if the server was stopped but not by the STOP command this will restart it
    if server_running:
        thread = threading.Thread(target=houdini_server, daemon=True)
        thread.start()
        print("Restarting server...")
    else:
        print("Houdini server stopped.")
            
# Run the server in a background thread
thread = threading.Thread(target=houdini_server, daemon=True)
thread.start()

print("Houdini Python server started in the background.")