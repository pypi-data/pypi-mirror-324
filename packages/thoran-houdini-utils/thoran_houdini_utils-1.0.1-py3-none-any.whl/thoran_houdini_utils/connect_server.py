import socket

HOST = "127.0.0.1"  # Houdini's IP (local machine)
PORT = 5000  # Must match the port used in Houdini

# Global variable to store the client socket
client_socket = None

def create_client_connection():
    """Create a socket connection if one doesn't already exist."""
    global client_socket
    if client_socket is None:  # If no connection exists
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        print("Connection established.")
    else:
        print("Connection already established, skipping.")

    return client_socket

def send_to_houdini(script_path, client_socket):
    """Send a Python file to Houdini via an open socket."""
    try:
        # Open the Python file and read its contents
        with open(script_path, 'r') as file:
            script = file.read()

        # Send the script to Houdini
        client_socket.send(script.encode())
        response = client_socket.recv(1024).decode()  # Get response from Houdini
        print(f"Houdini Response: {response}")

    except ConnectionRefusedError:
        print("Error: Unable to connect to Houdini. Make sure the server is running.")
    except Exception as e:
        print(f"Error: {e}")

def stop_connection():
    """Send stop command and close the socket."""
    global client_socket
    if client_socket:
        client_socket.send("STOP_SERVER".encode())  # Send stop command to server
        client_socket.close()
        client_socket = None  # Reset the socket to None after closing
        print("Connection closed.")
    else:
        print("No active connection to close.")