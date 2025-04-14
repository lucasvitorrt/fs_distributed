# 🗂️ Servidor de Arquivos Distribuído (DFS)

Este é um projeto simples de servidor e cliente para transferência de arquivos via TCP em Python. Ele permite que o cliente liste, envie, baixe e remova arquivos no servidor de forma remota, usando comandos customizados.

## 🚀 Funcionalidades

- 📄 `ls`: Lista os arquivos disponíveis no diretório do servidor
- ❌ `rm <arquivo>`: Remove um arquivo ou diretório no servidor
- 📤 `cp <caminho_arquivo_local>`: Envia um arquivo do cliente para o servidor
- 📥 `get <arquivo_remoto>`: Baixa um arquivo do servidor para o cliente
- 🆘 `help`: Mostra os comandos disponíveis
- ❎ `exit`: Encerra a conexão com o servidor

## 📦 Estrutura do Projeto

```
.
├── client.py        # Código do cliente
├── server.py        # Código do servidor
└── storage/         # Pasta onde os arquivos são armazenados no servidor
```

## ▶️ Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio
```

### 2. Inicie o servidor

```bash
python server.py
```

O servidor ficará ouvindo conexões na porta `8080`.

### 3. Em outro terminal, inicie o cliente

```bash
python client.py
```

Você verá o prompt `DFS>` pronto para receber comandos.

## ✅ Requisitos

- Python 3.x
- Sistema operacional com suporte a sockets (Windows/Linux/Mac)

## 💡 Exemplos de Uso

```bash
DFS> ls
DFS> cp "C:\Users\User\Downloads\meuarquivo.txt"
DFS> get meuarquivo.txt
DFS> rm meuarquivo.txt
DFS> help
DFS> exit
```

## ⚠️ Observações

- Os arquivos transferidos pelo cliente são salvos na pasta `storage/` do servidor.
- O cliente salva os arquivos baixados com prefixo `baixado_` no diretório local atual.
- O projeto não possui autenticação ou criptografia — ideal apenas para fins educacionais.

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
