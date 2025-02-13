import socket

def contains_sql_injection(message):
    # List of SQL keywords to check for possible SQL injection
    keywords = ["SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER"]
    
    # Iterate over each keyword
    for keyword in keywords:
        # Check if the keyword is present in the message
        if keyword in message:
            # Return True if a keyword is found
            return True
    
    # Return False if no keywords are found
    return False

def start_middleware():
    middleware = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    middleware.bind(("0.0.0.0", 12346))
    middleware.listen(1)
    print("Middleware is running...")

    while True:
        client_conn, client_addr = middleware.accept()
        print(f"Request received from client: {client_addr}")
        client_message = client_conn.recv(1024).decode()

        # Check if message is empty or whitespace
        if not client_message or client_message.isspace():
            client_conn.send("Cannot Send Empty Message".encode())  # Notify client of empty message
            client_conn.close()  # Close client connection

        # Check for SQL injection attempt
        elif contains_sql_injection(client_message):
            client_conn.send("SQL Injection Attempt Detected".encode())  # Notify client of SQL injection
            client_conn.close()  # Close client connection
        else:
            modified_message = f"[Modified by Middleware]: {client_message}"
            with open("middleware_log.txt", "a") as log_file:
                log_file.write(f"Client {client_addr} sent: {client_message}\n")

            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            server.connect(("127.0.0.1", 12345))
            server.send(modified_message.encode())

            server_response = server.recv(1024)
            client_conn.send(server_response)

            server.close()
        
start_middleware()