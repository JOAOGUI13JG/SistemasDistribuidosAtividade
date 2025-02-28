import socket
import threading
import bcrypt
from datetime import datetime


users = {}  
emails = []  


# def register_user(username, name, password):
#     print(f"Tentando cadastrar o usuário: {username}...")
#     if username in users:
#         print(f"Erro: O username '{username}' já está em uso.")
#         return "Username já existe."
  
#     password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
   
#     users[username] = {"name": name, "password_hash": password_hash}
#     print(f"Usuário '{username}' cadastrado com sucesso.")
#     return "Conta cadastrada com sucesso."
def register_user(username, name, password_hash):
    print(f"Tentando cadastrar o usuário: {username}...")
    if username in users:
        print(f"Erro: O username '{username}' já está em uso.")
        return "Username já existe."

    users[username] = {"name": name, "password_hash": password_hash.encode()}
    print(f"Usuário '{username}' cadastrado com sucesso.")
    return "Conta cadastrada com sucesso."


# def authenticate_user(username, password):
#     print(f"Tentando autenticar o usuário: {username}...")
#     if username not in users:
#         print(f"Erro: O username '{username}' não foi encontrado.")
#         return "Usuário não encontrado."
   
#     if bcrypt.checkpw(password.encode(), users[username]["password_hash"]):
#         print(f"Usuário '{username}' autenticado com sucesso.")
#         return "Autenticação bem-sucedida."
#     print(f"Erro: Senha incorreta para o usuário '{username}'.")
#     return "Senha incorreta."
def authenticate_user(username, password):
    print(f"Tentando autenticar o usuário: {username}...")
    if username not in users:
        print(f"Erro: O username '{username}' não foi encontrado.")
        return "Usuário não encontrado."

    if bcrypt.checkpw(password.encode(), users[username]["password_hash"]):
        print(f"Usuário '{username}' autenticado com sucesso.")
        return "Autenticação bem-sucedida."
    print(f"Erro: Senha incorreta para o usuário '{username}'.")
    return "Senha incorreta."

def send_email(from_user, to_user, subject, body):
    print(f"Tentando enviar e-mail de '{from_user}' para '{to_user}'...")
    if to_user not in users:
        print(f"Erro: O destinatário '{to_user}' não existe.")
        return "Destinatário inexistente."
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    email = {"from": from_user, "to": to_user, "subject": subject, "body": body, "timestamp": timestamp}
    emails.append(email)
    print(f"E-mail de '{from_user}' para '{to_user}' enviado com sucesso.")
    return "E-mail enviado com sucesso."

def receive_emails(username):
    print(f"Buscando e-mails para o usuário: {username}...")
    user_emails = [email for email in emails if email["to"] == username]
    emails[:] = [email for email in emails if email["to"] != username]
    print(f"{len(user_emails)} e-mail(s) encontrado(s) para '{username}'.")
    return user_emails

def handle_client(client_socket):
    print("Nova conexão de cliente estabelecida.")
    while True:
        try:
            request = client_socket.recv(1024).decode()
            if not request:
                print("Conexão com o cliente encerrada.")
                break

            print(f"Requisição recebida: {request}")
            parts = request.split(maxsplit=4)
            command = parts[0]

            if command == "REGISTER":
                response = register_user(parts[1], parts[2], parts[3])
            elif command == "LOGIN":
                response = authenticate_user(parts[1], parts[2])
            elif command == "SEND":
                response = send_email(parts[1], parts[2], parts[3], parts[4])
            elif command == "RECEIVE":
                user_emails = receive_emails(parts[1])
                response = str(user_emails)
            else:
                response = "Comando inválido."
                print(f"Comando inválido recebido: {command}")

            print(f"Enviando resposta: {response}")
            client_socket.send(response.encode())
        except Exception as e:
            print(f"Erro ao processar requisição: {e}")
            break

    client_socket.close()
    print("Conexão com o cliente fechada.")

def start_server():
    print("Iniciando servidor...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 12345))
    server.listen(5)
    print("Servidor iniciado. Aguardando conexões na porta 12345...")

    while True:
        client_socket, addr = server.accept()
        print(f"Conexão estabelecida com {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
