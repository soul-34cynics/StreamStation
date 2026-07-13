import socket
import threading
import os
import json

SONG_FOLDER = 'static/songs'
PORT = 6000

def handle_client(conn, addr):
    print(f"[+] Connected by {addr}")
    try:
        data = conn.recv(1024).decode()
        if data == 'GET_SONG_LIST':
            songs = [f for f in os.listdir(SONG_FOLDER) if f.endswith('.mp3')]
            conn.send(json.dumps(songs).encode())
        elif data.startswith('REQUEST_SONG:'):
            song_name = data.split(':', 1)[1]
            path = os.path.join(SONG_FOLDER, song_name)
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    chunk = f.read(4096)
                    while chunk:
                        conn.send(chunk)
                        chunk = f.read(4096)
            else:
                conn.send(b'NOT_FOUND')
    finally:
        conn.close()

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', PORT))
    s.listen(5)
    print(f"🎶 Peer server listening on port {PORT}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == '__main__':
    start_server()
