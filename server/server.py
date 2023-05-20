import random
import socket
import hashlib
import string
from datetime import datetime
from pymongo import MongoClient

# Server configuration
HOST = '0.0.0.0'
PORT = 65432

# Database Configuration
db_client = MongoClient("mongodb:27017")
db = db_client['database']
collection = db['hash']

file_name = str(datetime.now()) + '.txt'
file_path = f'serverdata/{file_name}'

def generate_random_text(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Insert file data into database
def insert_data(hash):
    data = {'hash': str(hash),
            'filename': file_path,
            }
    collection.insert_one(data)
    return print('Hash inserted in database successfully')

# Read data from database
def retrieve_data():
    result = []
    for hash in collection.find({}, {"_id": 0, 'filename':0}):
        result.append(hash)
    return result

# Create hash for checksum
def make_hash(data):
    h = hashlib.sha3_256()
    h.update(data)
    hash = h.hexdigest()
    return hash

# Check if the file is valid or not
def checksum(hash):
    if {'hash': hash} in retrieve_data():
        return 'The file is valid'
    else:
        return 'The file is not valid'

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))

    while True:
        server_socket.listen(1)
        print(f'Server listening on {HOST}:{PORT}')

            
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print('Connected to client:', client_address)

        # Create the file with 1K random text
        with open(file_path, 'w') as file:
            file.write(generate_random_text(1024))

        client_socket.send(file_name.encode())
        
        # Open and send the file to the client
        with open(file_path, 'rb') as file:
            data = file.read()
            file_hash = make_hash(data)
            insert_data(file_hash)
            client_socket.sendall(data)
            print(f'File "{file_name}" sent successfully')

        # Recieve the hash from the client
        client_hash = client_socket.recv(256).decode()
        if not client_hash:
            break
        
        # Response to the client for file verification
        message = checksum(client_hash)
        print(message)
        client_socket.send(message.encode())
        