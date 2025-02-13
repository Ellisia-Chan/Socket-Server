import socket
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 12345)) # Listen on all network interfaces
    server.listen(1)

    print("Server is waiting for connections...")

    while True:
        conn, addr = server.accept()
        print(f"Connection received from {addr}")
        message = conn.recv(1024).decode()
        print(f"Processed Message from Middleware: {message}")
        conn.send("Message received by the server".encode()) # Send response
        conn.close()
start_server()