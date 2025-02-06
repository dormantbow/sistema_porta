# utils/auth.py

import smtplib
from email.mime.text import MIMEText
# Lista de usuários com informações adicionais
USERS = {
    "usuario1": {"password": "senha1", "role": "admin"},
    "usuario2": {"password": "senha2", "role": "editor"},
    "usuario3": {"password": "senha3", "role": "viewer"},
    "usuario4": {"password": "senha4", "role": "editor"},
    "usuario5": {"password": "senha5", "role": "viewer"},
    "usuario6": {"password": "senha6", "role": "admin"},
}

def check_credentials(username, password):
    """
    Verifica se o usuário e a senha estão na lista de usuários válidos.
    Retorna o papel do usuário (role) se as credenciais estiverem corretas.
    """
    if username in USERS and USERS[username]["password"] == password:
        return USERS[username]["role"]  # Retorna o papel do usuário
    return None  # Retorna None se as credenciais estiverem incorretas


def send_reset_email(email):
    # Verifica se o e-mail existe no banco de dados
    if not email_in_database(email):  # Função para verificar o e-mail no BD
        return False

    # Configurações de e-mail
    sender_email = "melquessedequipedro@gmail.com"
    sender_password = "sua_senha"
    reset_link = f"https://seu-app/redefinir_senha?email={email}"

    msg = MIMEText(f"Clique no link para redefinir sua senha: {reset_link}")
    msg["Subject"] = "Redefinição de Senha"
    msg["From"] = sender_email
    msg["To"] = email

    # Envia o e-mail
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
    
    return True
