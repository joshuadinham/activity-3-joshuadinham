import socket
import pickle
import os
import threading


def save_unpickle_data_to_file(unpickled_data, directory, file_name):

    os.makedirs(directory, exist_ok=True)
    file_name = "received_" + file_name
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'wb') as file:
        file.write(unpickled_data)

def handle_client(client_socket, save_directory):
    try:
        # receive pickled file content
        pickled_data = b""
        while True:
            
            if pickled_data[-5:] == b"<END>":
                break
            chunk = client_socket.recv(1024)
            
            
            print(f"received chunk {chunk}")
            pickled_data += chunk
        
        #unpickle the received data
        print(f"unpickling data")
        data = pickle.loads(pickled_data)

        #extract the original filename and file content

        original_file_name = data['file_name']
        file_content = data['file_content']
        print(f"File name is {original_file_name}. saving data to \n {save_directory}")
        
        #save the unpickled data to directory
        save_unpickle_data_to_file(file_content, save_directory, original_file_name)
        response_message = f"File saved as: {os.path.join(save_directory, original_file_name)}"
        print(response_message)
        client_socket.sendall(response_message.encode('utf-8'))
    except Exception as e:
        error_message = f"Error handling client: {e}"
        print(error_message)
        client_socket.sendall(error_message.encode('utf-8'))
    finally:
        client_socket.close()

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 27000  # initiate port no above 1024

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance

    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen()

    print("Server is listening...")
    

    save_directory = input("Enter the directory to save files: ")

    while not os.path.exists(save_directory):
        print(f"Error: Directory '{save_directory} does not exist")
        save_directory = input("Enter the directory to save files: ")

    
    
    print(f"Waiting for client to connect")
    client_socket, address = server_socket.accept()
    print(f"Client connected")
    handle_client(client_socket, save_directory)
    


if __name__ == '__main__':
    server_program()