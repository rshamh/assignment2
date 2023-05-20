import hashlib
import socket

# Server Configurations
HOST = 'server' 
PORT = 65432
file_path = 'clientdata/'

# Create hash for checksum
def make_hash(data):
    h = hashlib.sha3_256()
    h.update(data)
    hash = h.hexdigest()
    return hash

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

    # Connect to the server
    client_socket.connect((HOST, PORT))
    print('Connected to server')

    while True:
        file_name = client_socket.recv(1024).decode()
        if not file_name:
            break
        with open(file_path + file_name, 'wb') as file:

            # Receive the file from the server
            data = client_socket.recv(1024)
            if not data:
                break

            file.write(data)
            print(f'File "{file_name}" received successfully') 
            
            # Send hash to server for checksum
            file_hash = make_hash(data)
            client_socket.send(file_hash.encode())
            response = client_socket.recv(1024).decode()
            print(f'Server Response: {response}')
            break
