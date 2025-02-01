import socket

HOST = "127.0.0.1"  # Houdini's IP (local machine)
PORT = 5000  # Must match the port used in Houdini

def send_to_houdini(command):
    """Send a Python command to Houdini via socket."""
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        client.send(command.encode())  # Send Python command
        response = client.recv(1024).decode()  # Get response from Houdini
        print(f"Houdini Response: {response}")  # Print response
        client.close()
        return response
    except ConnectionRefusedError:
        print("Error: Unable to connect to Houdini. Make sure the server is running.")
    except Exception as e:
        print(f"Error: {e}")