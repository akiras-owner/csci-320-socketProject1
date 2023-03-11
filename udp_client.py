import socket
import hashlib  # needed to calculate the SHA256 hash of the file
import sys  # needed to get cmd line parameters
import os.path as path  # needed to get size of file in bytes


IP = '127.0.0.1'  # change to the IP address of the server
PORT = 12000  # change to a desired port number
BUFFER_SIZE = 1024  # change to a desired buffer size


def get_file_size(file_name: str) -> int:
    size = 0
    try:
        size = path.getsize(file_name)
    except FileNotFoundError as fnfe:
        print(fnfe)
        sys.exit(1)
    return size


def send_file(filename: str):
    # get the file size in bytes

    file_size = get_file_size(filename)

    # convert the file size to an 8-byte byte string using big endian
    size = len(filename).to_bytes(8, byteorder='big')


    # create a SHA256 object to generate hash of file
    m = hashlib.sha256()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        client_socket.sendto(size + filename.encode(), (IP, PORT))
        response, address = client_socket.recvfrom(BUFFER_SIZE)
        if response != b'go ahead':
            raise Exception('Bad server response - was not go ahead!')

        # open the file to be transferred
        with open(file_name, 'rb') as file:

            data_chunks = file.read(BUFFER_SIZE)
            if len(data_chunks) == 0:
                return data_chunks
            m.update(data_chunks)
            client_socket.sendto(data_chunks, (IP,PORT))
            server_response, address = client_socket.recvfrom(BUFFER_SIZE)
            if server_response != b'received':
                raise Exception('Failure to transfer')



        client_socket.sendto(m.digest(), (IP, PORT))
        response, address = client_socket.recvfrom(BUFFER_SIZE)
        if response != b'failed':
            raise Exception('Bad server response - was not go ahead!')
        else:
            print('Transfer was successful')

    except Exception as e:
        print(f'An error occurred while sending the file: {e}')
    finally:
        client_socket.close()


if __name__ == "__main__":
    # get filename from cmd line
    if len(sys.argv) < 2:
        print(f'SYNOPSIS: {sys.argv[0]} <filename>')
        sys.exit(1)
    file_name = sys.argv[1]  # filename from cmdline argument
    send_file(file_name)
