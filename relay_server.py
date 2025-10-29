import socket
import threading

HOST = "0.0.0.0"
PORT_VIDEO = 8080
PORT_INPUT = 9090

def handle_client(client_socket, other_socket):
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                break
            other_socket.sendall(data)
        except:
            break
    client_socket.close()
    other_socket.close()

def start_relay():
    video_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    video_server.bind((HOST, PORT_VIDEO))
    video_server.listen(1)
    print(f"Relay Video server listening on port {PORT_VIDEO}")

    input_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    input_server.bind((HOST, PORT_INPUT))
    input_server.listen(1)
    print(f"Relay Input server listening on port {PORT_INPUT}")

    while True:
        print("Waiting for host (laptop)...")
        host_video, _ = video_server.accept()
        print("Host connected for video")
        host_input, _ = input_server.accept()
        print("Host connected for input")

        print("Waiting for client (phone)...")
        client_video, _ = video_server.accept()
        print("Client connected for video")
        client_input, _ = input_server.accept()
        print("Client connected for input")

        threading.Thread(target=handle_client, args=(host_video, client_video)).start()
        threading.Thread(target=handle_client, args=(client_video, host_video)).start()
        threading.Thread(target=handle_client, args=(host_input, client_input)).start()
        threading.Thread(target=handle_client, args=(client_input, host_input)).start()

if __name__ == "__main__":
    start_relay()
