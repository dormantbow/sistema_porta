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

