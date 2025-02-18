# utils/auth.py

import smtplib
from email.mime.text import MIMEText

# Lista de usuários com informações adicionais
USERS = {
    "porteiro": {"password": "1234", "role": "porteiro"},  # Exemplo de um porteiro
    "admin": {"password": "admin123", "role": "admin"},
    "usuario1": {"password": "senha1", "role": "viewer"},
}

def check_credentials(username, password):
    """
    Verifica se o usuário e a senha estão na lista de usuários válidos.
    Retorna o papel do usuário (role) se as credenciais estiverem corretas.
    """
    if username in USERS and USERS[username]["password"] == password:
        return USERS[username]["role"]  # Retorna o papel do usuário
    return None  # Retorna None se as credenciais estiverem incorretas

def reset_password(username, new_password):
    """
    Redefine a senha de um usuário, se ele existir.
    Retorna True se a redefinição for bem-sucedida, False caso contrário.
    """
    if username in USERS:
        USERS[username]["password"] = new_password
        return True
    return False
