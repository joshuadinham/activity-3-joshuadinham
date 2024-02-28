import socket
import threading
import pickle

# Task execution function
def execute_task(task):
    try:
        function_to_execute = task['function']
        arguments_to_pass = task['args']
        result = function_to_execute(*arguments_to_pass)
        return {'status': 'success', 'result': result}
    except Exception as e:
        return {'status': 'error', 'error_message': str(e)}

# Thread function for handling a client connection
def handle_client(client_socket, tasks):
    try:
        while True:
            # Receive a pickled task from the client
            pickled_task = b""
            while True:
                if pickled_task[-5:] == b"<END>":
                    break
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                pickled_task += chunk

            # Unpickle the task
            tasks_to_execute = pickle.loads(pickled_task)

            # Execute the task and send back the result
            results = []
            for task in tasks_to_execute:
                result = execute_task(task)
                results.append(result)

            client_socket.sendall(pickle.dumps(result))
            client_socket.send(b"<END>")
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
server.bind((host, 5555))
server.listen()

print("Server is listening...")

# Shared task list (for simplicity; in a production scenario, you'd use a task queue)
tasks = []

while True:
    client_socket, address = server.accept()
    print(f"Accepted connection from {address}")

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, tasks))
    client_thread.start()
