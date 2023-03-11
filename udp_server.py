import socket
import os
import hashlib  # needed to verify file hash


IP = '127.0.0.1'  # change to the IP address of the server
PORT = 12000  # change to a desired port number
BUFFER_SIZE = 1024  # change to a desired buffer size


def get_file_info(data: bytes) -> (str, int):
    return data[8:].decode(), int.from_bytes(data[:8], byteorder='big')



def upload_file(server_socket: socket, file_name: str, file_size: int):
    # create a SHA256 object to verify file hash

    m = hashlib.sha256(file_name)


    # create a new file to store the received data
    with open(file_name+'.temp', 'wb') as file:
        received_data = 0
        while received_data < file_size:
            received_data, client_side = server_socket.recvfrom(BUFFER_SIZE)
            if not received_data:
                return received_data

                file.write(received_data)
                m.update(received_data)
                server_socket.sendto(b'it was receieved', client_side)
                received += len(received_data)
                hashfrmclient, client_side = server_socket.recvfrom(BUFFER_SIZE)

    with open(file_name + '.temp', 'rb') as file:
        hashfromserver = hashlib.sha256(file.read()).hexdigest()

    if hashfrmclient.decode == hashfromserver:
        os.rename(file_name + '.temp', file_name)
        server_socket.sendto(b'success', client_side)

    else:
        os.remove(file_name + '.temp')
        server_socket.sendto(b'failed', client_side)


def start_server():
    # create a UDP socket and bind it to the specified IP and port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((IP, PORT))
    print(f'Server ready and listening on {IP}:{PORT}')

    try:
        while True:
            # expecting an 8-byte byte string for file size followed by file name
            received_data, client_side = server_socket.recvfrom(BUFFER_SIZE)
            file_name,file_size = get_file_info(received_data)
            server_socket.sendto(b'go  ahead', client_side)
            upload_file(server_socket, file_name, file_size)
    except KeyboardInterrupt as ki:
        pass
    except Exception as e:
        print(f'An error occurred while receiving the file:str {e}')
    finally:
        server_socket.close()


if __name__ == '__main__':
    start_server()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((IP, PORT))
    print(f"Server is live on {IP}:{PORT}")

