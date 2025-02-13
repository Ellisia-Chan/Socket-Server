import socket
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 12346)) # Connect to middleware instead of server
    message = "Hello World!"
    client.send(message.encode()) # Send message to middleware
    response = client.recv(1024).decode() # Receive server response
    print(f"Response from server: {response}")
    client.close()
start_client()