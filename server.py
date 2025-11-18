import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

print("Server started... Waiting for connections...")

def handle_client(conn, addr):
    print(f"Client connected: {addr}")
    clients.append(conn)

    while True:
        try:
            message = conn.recv(1024)
            if not message:
                break

            # Broadcast to all connected clients
            for c in clients:
                if c != conn:
                    c.send(message)

        except:
            break

    conn.close()
    clients.remove(conn)
    print(f"Client disconnected: {addr}")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
    thread.start()
