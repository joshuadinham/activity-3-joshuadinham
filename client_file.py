import socket
import os
import pickle

def pickle_and_send(file_path, server_address):
    try:
        print(f"Initializing pickle_and_send")
        #open file and put the contents of it into an object
        with open(file_path, 'rb') as file:
            file_content = file.read()

        #create a dictionary containing the original file_name and the contents
            
        data = {'file_name': file_path.split('/')[-1], 'file_content': file_content}

        # Pickle the file content
        pickled_data = pickle.dumps(data)
        print(f"Pickled data successfully")
        # Create a socket connection to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            print(f"Creating connection socket")
            client_socket.connect(server_address)

            # Send the pickled file content
            print(f"Sending file: {file_path}")
            client_socket.sendall(pickled_data)
            client_socket.send(b"<END>")
            response = client_socket.recv(1024).decode('utf-8');
            print(f"Server Response: {response}")
            
        client_socket.close()
        print(f"File '{file_path}' sent to the server.")
    except Exception as e:
        print(f"Error sending file: {e}")

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 27000  # socket server port number

    
    file_path_str = input("What is the absolute file_path of the file? (Not including file name, ending with '/')")
    file_name_str = input("What is the name of the file (including extension)")
    file_path = os.path.join(file_path_str, file_name_str)
    
    while not os.path.exists(file_path):
    
        print(f"File and/or path specified does not exist")
        file_path_str = input("What is the absolute file_path of the file? (Not including file name, ending with '/')")
        file_name_str = input("What is the name of the file (including extension)")
        file_path = os.path.join(file_path_str, file_name_str)
    
    
    if os.path.exists(file_path): 
        
        pickle_and_send(file_path, (host, port))

    


if __name__ == '__main__':
    client_program()