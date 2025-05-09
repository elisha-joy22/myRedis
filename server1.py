import socket
from mapper.mapper import command_handlers


def main():
    server_socket = socket.create_server(("localhost",5379),reuse_port=True)
    print("Listening on port 5379")
    while True:
        client_socket,client_addr = server_socket.accept()
        print(f"Client connected: {client_addr}")
        handle_client(client_socket)

def handle_client(sock):
    with sock:
        while True:
            data = sock.recv(1024)
            if not data:
                print("Client disconnected")
                break    
            print("Received data: {data}")
            response = check_commands(data)
            sock.sendall(f"{response}\r\n".encode())


def check_commands(command):
    # Clean command input
    if isinstance(command, bytes):
        command = command.decode()
    command = command.strip()
    
    # Split command into components
    parts = command.split()
    if not parts:
        return "-ERR Empty command"

    cmd = parts[0].upper()

    # Call corresponding handler function
    if cmd in command_handlers:
        return command_handlers[cmd](parts)
    
    return "-ERR Unknown command"



if __name__=="__main__":
    main()