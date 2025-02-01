import socket

HOST = "127.0.0.1"  # Houdini's IP (local machine)
PORT = 5000  # Must match the port used in Houdini

def send_to_houdini(script_path):
    """Send a Python file to Houdini via socket."""
    try:
        # Open the Python file and read its contents
        with open(script_path, 'r') as file:
            script = file.read()

        # Create a socket connection to Houdini
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))

        # Send the script to Houdini
        client.send(script.encode())
        response = client.recv(1024).decode()  # Get response from Houdini
        print(f"Houdini Response: {response}")
        client.close()
        return response
    except ConnectionRefusedError:
        print("Error: Unable to connect to Houdini. Make sure the server is running.")
    except Exception as e:
        print(f"Error: {e}")