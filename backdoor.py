import sys
import socket
import os
import subprocess, shlex

def receiver():
    # x = 1
    host = "127.0.0.1"
    port = int(sys.argv[2])

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)
    print("Server listening on {}:{}".format(host, port))
    
    # wait for first connection
    client_socket, client_address = server_socket.accept()

    while True:
        # receive data
        received_data = client_socket.recv(1024)
        if len(received_data) > 0:

            received_message = received_data.decode()

            # print("message :", received_message)
            
            args = shlex.split(received_message)
            # print(args)

            # special case because cd is a shell built-in
            if args[0] == 'cd':
                os.chdir(args[1])
            else:
                proc = subprocess.run(args, capture_output=True, text=True)

            if len(proc.stdout) > 0:
                client_socket.sendall(proc.stdout.encode())
            else:
                client_socket.sendall("\n".encode())
        else:
            # if no data was received, or if the client closed the connection,
            # reset the socket
            client_socket.close()
            client_socket, client_address = server_socket.accept()

        sys.stdout.flush()
    

def sender():
    ip = sys.argv[2]
    port = int(sys.argv[3])
    
    # create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to remote
        sock.connect((ip, port))

        while True:
            message = input(">>> ")
            if message == 'quit':
                break

            sock.sendall(message.encode())
            
            response = sock.recv(1024)
            response = response.decode()
            print(response)


    except Exception as e:
        print("whoops : ", e)
        sys.exit(1)

def main():
    # command line args
    # localhost = 127.0.0.1
    option = sys.argv[1]
    if option == "receiver":
        receiver()
    elif option == "sender":
        sender()

if __name__ == "__main__":
    main()