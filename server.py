import os
import socket
import shutil
import threading

HOST = 'localhost'
PORT = 8080
STORAGE_DIR = 'storage'

def handle_client(conn, addr):
    print(f"[+] Cliente conectado: {addr}")
    with conn:
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    break

                args = data.strip().split()
                if not args:
                    conn.sendall("Comando vazio.".encode())
                    continue

                command = args[0]

                if command == 'exit':
                    print(f"[-] Cliente {addr} solicitou encerramento.")
                    break  # Encerra a comunicação com o cliente

                if command == 'ls':
                    path = os.path.join(STORAGE_DIR, *args[1:])
                    if os.path.exists(path):
                        if os.path.isfile(path):
                            response = f"Arquivo: {os.path.basename(path)}"
                        else:
                            files = os.listdir(path)
                            response = "\n".join(files) if files else "Diretório vazio."
                    else:
                        response = "Caminho não encontrado."

                elif command == 'rm':
                    if len(args) < 2:
                        conn.sendall("Nome do arquivo ausente.".encode())
                        continue
                    
                    path = os.path.join(STORAGE_DIR, *args[1:])
                    try:
                        if os.path.isfile(path):
                            os.remove(path)
                        elif os.path.isdir(path):
                            shutil.rmtree(path)
                        response = "Remoção concluída."
                    except Exception as e:
                        response = f"Erro: {str(e)}"

                elif command == 'cp':
                    if len(args) < 2:
                        conn.sendall("Nome do arquivo ausente.".encode())
                        continue

                    filename = args[1]
                    filepath = os.path.join(STORAGE_DIR, filename)

                    # Recebe o tamanho do arquivo
                    file_size_raw = conn.recv(1024)
                    try:
                        file_size = int(file_size_raw.decode())
                    except ValueError:
                        conn.sendall("Tamanho de arquivo inválido.".encode())
                        continue

                    conn.sendall("ACK".encode())  # Confirma recebimento do tamanho

                    # Recebe os dados do arquivo
                    received = b""
                    while len(received) < file_size:
                        chunk = conn.recv(8192)
                        if not chunk:
                            break
                        received += chunk

                    # Salva o arquivo na pasta de armazenamento
                    with open(filepath, 'wb') as f:
                        f.write(received)

                    response = f"📤 Arquivo '{filename}' salvo no servidor."

                elif command == 'get':
                    path = os.path.join(STORAGE_DIR, *args[1:])
                    if os.path.exists(path) and os.path.isfile(path):
                        file_size = os.path.getsize(path)
                        conn.sendall(str(file_size).encode())
                        ack = conn.recv(1024)
                        if ack.decode() == "ACK":
                            with open(path, 'rb') as f:
                                while chunk := f.read(8192):
                                    conn.sendall(chunk)
                        continue
                    else:
                        response = "Arquivo não encontrado ou é um diretório."

                else:
                    response = "Comando inválido."

                conn.sendall(response.encode())

            except ConnectionResetError:
                print(f"[-] Cliente desconectado: {addr}")
                break
            except Exception as e:
                print(f"[Erro] {e}")
                break

def start_server():
    os.makedirs(STORAGE_DIR, exist_ok=True)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"🚀 Servidor ouvindo em {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()

if __name__ == '__main__':
    start_server()
