import socket
import os
import threading


def validate_path(requested_path, www_dir):
    # Get the absolute path of the requested file
    abs_path = os.path.abspath(os.path.join(www_dir, requested_path.lstrip("/")))
    print(abs_path, www_dir)
    # Check if the absolute path is within the www directory
    if os.path.commonpath([abs_path, www_dir]) != www_dir:
        return None
    else:
        return abs_path


def handle_request(client_socket, www_dir):
    # Receive data from the client
    request_data = client_socket.recv(1024).decode()

    # Split the request data into lines
    lines = request_data.split("\r\n")

    # Extract the first line which contains the request method, path, and HTTP version
    first_line = lines[0]

    # Parse the first line to extract the request method and path
    method, path, _ = first_line.split(" ")

    # Validate the requested path
    abs_path = validate_path(path, www_dir)

    # If the requested path is not valid, return a 404 Not Found response
    if not abs_path:
        response = "HTTP/1.1 404 Not Found\r\n\r\n404 Not Found\r\n"
    else:
        # Open the requested file
        try:
            # if abs_path[:-1] == '/':
            #     abs_path.__add__('index.html')
            with open(abs_path, 'r') as f:
                # Read the contents of the file
                content = f.read()
            # Create the HTTP response with the content of the requested file
            response = f"HTTP/1.1 200 OK\r\n\r\n{content}\r\n"
        except FileNotFoundError:
            # If the requested file is not found, return a 404 Not Found response
            response = "HTTP/1.1 404 Not Found\r\n\r\n404 Not Found\r\n"

    # Send the HTTP response back to the client
    client_socket.send(response.encode())

    # Close the client socket
    client_socket.close()


def main(www_dir):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the server address (127.0.0.1) and port 80
    server_socket.bind(('127.0.0.1', 80))

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server listening on port 80, serving files from {www_dir} directory...")

    while True:
        # Accept incoming connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Create a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_request, args=(client_socket, www_dir))
        client_thread.start()


if __name__ == "__main__":
    # Specify the location of the www folder on startup
    www_directory = input("Enter the absolute path of the www folder: ")

    # Check if the specified directory exists
    if not os.path.exists(www_directory):
        print("Error: Specified www directory does not exist.")
    else:
        main(www_directory)
