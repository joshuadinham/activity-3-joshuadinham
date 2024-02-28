import socket
import pickle
from task_module import add, multiply
# Task definition


# Create a task dictionary
tasks = [
    {'function': add, 'args': (3, 4)},
    {'function': multiply, 'args':(5,5)}
]

# Connect to the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    host = socket.gethostname()
    client_socket.connect((host, 5555))

    # Send the pickled task to the server
    client_socket.sendall(pickle.dumps(tasks))
    client_socket.send(b"<END>")

    # Receive the result from the server
    result = b""
    while True:
        if result[-5:] == b"<END>":
            break
        chunk = client_socket.recv(1024)
        result += chunk

    # Unpickle the result
    result = pickle.loads(result)

    print(f"Result received from the server: {result}")
