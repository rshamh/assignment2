This application is a soloution for [CS 378: Assignment 2 - Dockers and Containers](https://www.cs.utexas.edu/~vijay/cs378-f17/projects/assignment2.htm). You can check the assignment in the previous link.

# How It Works
This application create 3 containers - server, client, and mongodb - that simulate a server-client newtork with Docker. 
It create images for server and client base on *python:alpine3.18*, and for database base on *mongo:4.2.24*.
## Server
Server container has a server.py. It use socket library to create a low-level server through Docker network. It will do this tasks respectively:
- Generate random text with 1024 charecters to create a file of size 1 KB.
- It creates a hash with SHA3_256 to use in validation and checksum function
- It connects to MongoDB database in order to store filename and its hash into collection.
- It use two method insert and retrieve based on CRUD concept to creat and read data from database.
- With creation of a socket object with predefined HOST and PORT starts to listen on network to makes connection with possible client.
- After the connection was accepted it will send the file to client and wait for response from client, which is the file's hash to check the validation.
- Then it responses to clinet that if the file is valid or not.

## Client
Client container has a client.py. It use the socket library to connect the server through docker network. It will do this tasks respectively:
- It uses socket object with server's HOST and PORT to connect to the server.
- After that the connection is accepted by server, it waits to recieve the file data, the write it to the /clientdata directory.
- It creates a hash with SHA3_256 then sends it to server to get the validation response.

# How To Use It
This application use Docker containers, network, and volumes. To store file's name and its hash MongoDB is used.
To make containers and run application two ways are considerd:
## 1 - docker-compose (*recommended*)
In root folder where the `docker-compose.yml` is in, run this command to build images and run containers automatically:

```
$ docker-compose up --build
```
For next tryings when you want just run the containers omit `--build`.
This command will run three containers - server, client, and mongodb - by uing Dockerfiles in their folders, then create network automatically and add containers to it. Based on the configuration in the `docker-compose.yml` it creates `servervol` and `clientcol`, then mount them to `\serverdata` and `clientdata`.

After a couple of seconds when the containers are run, you need to execute a command to enter the client container manually.
```
$ docker exec -it <CONTAINER_NAME> sh
```
You can find the `CONTAINER_NAME` for clinet by running the folloing command:
```
$ docker ps
```
After `sh` command was run for client you are in the interactive mode. To connect client with server and recive the file and its validation run this command in the client container shell:
```
/app # python client.py
```
it will recieve the file and response message for its validation from server.
You can check the list of files and their contents with this commands:
```
/app # ls /clientdata
/app # cat /clientdata/<FILE_NAME>
```
Bye running `python client.py` you can recieve another file from server as while as the server is still running.

## 2- Use `fileserver.sh` and `clientserver.sh`
To run commands manually to build images, create network, create volume, add them to containers, and run containers, two executable files with required commands that embedded in are prepared.
First you need to make them executable by running these two command:
```
$ chmod a+x fileserver.sh
$ chmod a+x fileclient.sh
```
Then you need to run `fileserver.sh` first and after that `fileclient.sh`
```
$ bash fileserver.sh
$ bash fileclient.sh
```
It will execute all commands that we need to make images, run containers with volume and network setup for all three containers.
After that you need to execute `python client.py` in client container like previous method.
```
/app # python client.py
```
```
/app # ls /clientdata
/app # cat /clientdata/<FILE_NAME>
```
