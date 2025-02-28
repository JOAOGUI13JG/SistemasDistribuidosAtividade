import socket
import bcrypt


#def connect_to_server(ip, port):
    
   # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #try:
      
    #    print(f"Tentando conectar ao servidor no endereço {ip}:{port}...")
      #  client_socket.connect((ip, port))
       
      #  print("Conexão estabelecida com sucesso. Serviço Disponível.")
      #  return client_socket
 #   except Exception as e:
        
     #   print(f"Erro ao conectar ao servidor: {e}")
     #   print("Verifique se o servidor está rodando e se o IP e a porta estão corretos.")
       # return None
def connect_to_server(ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print(f"Tentando conectar ao servidor no endereço {ip}:{port}...")
        client_socket.connect((ip, port))
        print("Conexão estabelecida com sucesso. Serviço Disponível.")
        return client_socket
    except Exception as e:
        print(f"Erro ao conectar ao servidor: {e}")
        print("Verifique se o servidor está rodando e se o IP e a porta estão corretos.")
        return None


# def register_account(client_socket):
    
#     print("\n--- Cadastro de Nova Conta ---")
#     name = input("Digite seu nome completo: ")
#     username = input("Escolha um nome de usuário (sem espaços): ")
#     password = input("Escolha uma senha: ")


#     print("Enviando dados de cadastro para o servidor...")
#     client_socket.send(f"REGISTER {username} {name} {password}".encode())

   
#     response = client_socket.recv(1024).decode()
#     print("Resposta do servidor:", response)

def register_account(client_socket):
    print("\n--- Cadastro de Nova Conta ---")
    name = input("Digite seu nome completo: ")
    username = input("Escolha um nome de usuário (sem espaços): ")
    password = input("Escolha uma senha: ")

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    print("Enviando dados de cadastro para o servidor...")
    client_socket.send(f"REGISTER {username} {name} {hashed_password}".encode())

    response = client_socket.recv(1024).decode()
    print("Resposta do servidor:", response)

# def login(client_socket):
#     print("\n--- Login ---")
#     username = input("Digite seu nome de usuário: ")
#     password = input("Digite sua senha: ")

#     print("Enviando credenciais para o servidor...")
#     client_socket.send(f"LOGIN {username} {password}".encode())

#     response = client_socket.recv(1024).decode()
#     print("Resposta do servidor:", response)

#     return response == "Autenticação bem-sucedida."


def login(client_socket):
   
    print("\n--- Login ---")
    username = input("Digite seu nome de usuário: ")
    password = input("Digite sua senha: ")

    
    print("Enviando credenciais para o servidor...")
    client_socket.send(f"LOGIN {username} {password}".encode())

  
    response = client_socket.recv(1024).decode()
    print("Resposta do servidor:", response)

    
    return response == "Autenticação bem-sucedida."


def send_email(client_socket, from_user):
   
    print("\n--- Enviar E-mail ---")
    to_user = input("Digite o nome de usuário do destinatário: ")
    subject = input("Digite o assunto do e-mail: ")
    body = input("Digite o corpo do e-mail: ")

    
    print("Enviando e-mail para o servidor...")
    client_socket.send(f"SEND {from_user} {to_user} {subject} {body}".encode())


    response = client_socket.recv(1024).decode()
    print("Resposta do servidor:", response)


def receive_emails(client_socket, username):
  
    print("\n--- Receber E-mails ---")
    print("Solicitando e-mails ao servidor...")
    client_socket.send(f"RECEIVE {username}".encode())


    emails = eval(client_socket.recv(1024).decode())  
    print(f"Você tem {len(emails)} e-mail(s) recebido(s).")

  
    for i, email in enumerate(emails):
        print(f"[{i+1}] De: {email['from']} - Assunto: {email['subject']}")

   
    if emails:
        choice = int(input("Digite o número do e-mail que deseja ler: ")) - 1
        print(f"\nDe: {emails[choice]['from']}")
        print(f"Assunto: {emails[choice]['subject']}")
        print(f"Corpo: {emails[choice]['body']}")
        print(f"Data/Hora: {emails[choice]['timestamp']}")
    else:
        print("Nenhum e-mail para exibir.")


def main():
    client_socket = None
    logged_in = False
    username = ""

    while True:
       
        print("\n--- MENU PRINCIPAL ---")
        print("1) Apontar Servidor")
        print("2) Cadastrar Conta")
        print("3) Acessar E-mail")
        if logged_in:
            print("4) Enviar E-mail")
            print("5) Receber E-mails")
            print("6) Logout")
        choice = input("Escolha uma opção: ")

        if choice == "1":
           
            ip = input("Digite o IP do servidor: ")
            port = int(input("Digite a porta do servidor: "))
            client_socket = connect_to_server(ip, port)
        elif choice == "2" and client_socket:
            
            register_account(client_socket)
        elif choice == "3" and client_socket:
          
            if login(client_socket):
                logged_in = True
                username = input("Digite seu nome de usuário: ")
                while logged_in:
                    
                    print("\n--- MENU DO USUÁRIO ---")
                    print(f"Bem-vindo, {username}!")
                    print("4) Enviar E-mail")
                    print("5) Receber E-mails")
                    print("6) Logout")
                    sub_choice = input("Escolha uma opção: ")

                    if sub_choice == "4":
                      
                        send_email(client_socket, username)
                    elif sub_choice == "5":
                    
                        receive_emails(client_socket, username)
                    elif sub_choice == "6":
                    
                        logged_in = False
                        print("Logout realizado com sucesso.")
                    else:
                        print("Opção inválida.")
        else:
            print("Opção inválida ou servidor não conectado.")


if __name__ == "__main__":
    print("Iniciando cliente de e-mail...")
    main()
