import socket

host = "127.0.0.1"  # Houdini's IP
port = 5000  # Must match the port used in Houdini

def send_to_houdini(command):
    """Send a Python command to Houdini via socket."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))  # Connect to Houdini
    client.send(command.encode())  # Send Python command
    response = client.recv(1024).decode()  # Get response from Houdini
    print(f"Houdini Response: {response}")  # Print response
    client.close()