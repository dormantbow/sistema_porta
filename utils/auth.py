# utils/auth.py

import streamlit as st
import mysql.connector
import sqlite3
import bcrypt
from validate_docbr import CPF
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
    if username in USERS and USERS[username]["senha"] == password:
        comando = f'SELECT role FROM usuario WHERE cpf = "{username}"'
        cursor.execute(comando)
        resultado = cursor.fetchall() # sempre que for ler o banco de dados
        #logger.warning(resultado[0][0])
        if resultado:
            return resultado[0][0]  # Retorna o papel do usuário
    return None  # Retorna None se as credenciais estiverem incorretas

def reset_password(username, new_password):
    """
    Redefine a senha de um usuário, se ele existir.
    Retorna True se a redefinição for bem-sucedida, False caso contrário.
    """
    if username in USERS:
        USERS[username]["senha"] = new_password
        
        senha = new_password
        comando = f'UPDATE usuario SET senha = "{senha}" WHERE cpf = "{username}"'
        cursor.execute(comando)
        conexao.commit() # sempre que for  alterar o banco de dados
        return True
    return False