# utils/auth.py

import streamlit as st
import mysql.connector
import sqlite3
import bcrypt
from validate_docbr import CPF
import smtplib
from email.mime.text import MIMEText

conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'admin123',
    database = 'bdporteiros',
)
cursor = conexao.cursor()
# Lista de usuários com informações adicionais
comando = 'SELECT * FROM porteiros'
cursor.execute(comando)
resultados = cursor.fetchall()

# Obtendo os nomes das colunas
colunas = [desc[0] for desc in cursor.description]

# Convertendo os resultados para um dicionário
USERS = [dict(zip(colunas, linha)) for linha in resultados]

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
