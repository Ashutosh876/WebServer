import socket


def handle_request(client_socket):
    # Receive data from the client
    request_data = client_socket.recv(1024).decode()

    # Split the request data into lines
    lines = request_data.split("\r\n")

    # Extract the first line which contains the request method, path, and HTTP version
    first_line = lines[0]

    # Parse the first line to extract the request method and path
    method, path, _ = first_line.split(" ")

    # Create the HTTP response with the requested path
    response = f"HTTP/1.1 200 OK\r\n\r\nRequested path: {path}\r\n"

    # Send the HTTP response back to the client
    client_socket.send(response.encode())

    # Close the client socket
    client_socket.close()


def main():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the server address (127.0.0.1) and port 80
    server_socket.bind(('127.0.0.1', 80))

    # Listen for incoming connections
    server_socket.listen(1)
    print("Server listening on port 80...")

    while True:
        # Accept incoming connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Handle the client's request
        handle_request(client_socket)


if __name__ == "__main__":
    main()
