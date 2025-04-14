import socket
import os

HOST = 'localhost'
PORT = 8080

def print_help():
    print("""
Comandos disponíveis:
  ls                                Lista arquivos no diretório remoto
  rm <nome_arquivo.ext>             Remove arquivo ou diretório remoto - Ex: rm copy.ext
  cp <caminho_arquivo>              Copia arquivo local para o diretorio do servidor - Ex: cp C:\\Users\\User\\Downloads\\copy.ext
  get <arquivo_remoto.ext>          Baixa arquivo do servidor para o cliente
  help                              Mostra esta ajuda
  exit                              Sai do shell
""")

def main():
    print("🔗 Tentando conectar ao servidor de arquivos distribuído...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print("✅ Conectado ao servidor! Digite 'help' para ver os comandos.")
            
            while True:
                cmd = input("DFS> ").strip()
                if not cmd:
                    continue
                if cmd.lower() == 'exit':
                    s.sendall(cmd.encode())  # Envia 'exit' para o servidor
                    print("⛔ Encerrando conexão.")
                    break
                if cmd.lower() == 'help':
                    print_help()
                    continue

                if cmd.startswith("cp "):
                    try:
                        # Pega o caminho completo (pode conter espaços)
                        filepath = cmd[3:].strip().strip('"')
                        if not os.path.exists(filepath):
                            print("❌ Arquivo local não encontrado.")
                            continue

                        filename = os.path.basename(filepath)  # Apenas o nome do arquivo

                        # Envia o comando 'cp <nome_do_arquivo>'
                        s.sendall(f"cp {filename}".encode())

                        with open(filepath, 'rb') as f:
                            file_data = f.read()

                        s.sendall(str(len(file_data)).encode())
                        ack = s.recv(1024).decode()
                        if ack != "ACK":
                            print("Erro: não recebeu ACK do servidor.")
                            continue

                        s.sendall(file_data)
                        response = s.recv(4096).decode()
                        print(response)
                    except Exception as e:
                        print(f"Erro ao enviar arquivo: {e}")

                elif cmd.startswith("get "):
                    try:
                        s.sendall(cmd.encode())
                        filename = cmd.split()[1]

                        file_size_raw = s.recv(1024)
                        try:
                            file_size = int(file_size_raw.decode())
                        except ValueError:
                            print(file_size_raw.decode())
                            continue

                        s.sendall(b"ACK")

                        data = b""
                        while len(data) < file_size:
                            part = s.recv(8192)
                            if not part:
                                break
                            data += part

                        with open(f"baixado_{filename}", "wb") as f:
                            f.write(data)

                        print(f"📥 Arquivo '{filename}' baixado com sucesso como 'baixado_{filename}'")
                    except Exception as e:
                        print(f"Erro ao baixar: {e}")

                else:
                    try:
                        s.sendall(cmd.encode())
                        response = s.recv(4096).decode()
                        print(response)
                    except Exception as e:
                        print(f"Erro na comunicação: {e}")

    except (ConnectionRefusedError, socket.error) as e:
        print(f"❌ Não foi possível conectar ao servidor. Erro: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == '__main__':
    main()
