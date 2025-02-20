# utils/auth.py

import streamlit as st
import mysql.connector
import sqlite3
import bcrypt
from validate_docbr import CPF
import smtplib
from email.mime.text import MIMEText


def check_credentials(username, password):
    print(f"Debug: Verificando credenciais para o usuário: {username}")  # Debug
    print(f"Debug: Senha recebida: {password}")  # Debug

    # Conecta ao banco de dados
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='bdporteiros',
    )
    cursor = conexao.cursor()

    # Consulta o banco de dados para verificar o usuário e a senha
    comando = f'SELECT senha, role FROM usuario WHERE cpf = "{username}"'
    print(f"Debug: Comando SQL executado: {comando}")  # Debug

    cursor.execute(comando)
    resultado = cursor.fetchone()  # Obtém a primeira linha do resultado

    if resultado:
        senha_banco = resultado[0]  # Senha armazenada no banco de dados
        role = resultado[1]  # Role do usuário
        print(f"Debug: Senha no banco: {senha_banco}")  # Debug
        print(f"Debug: Role no banco: {role}")  # Debug

        if password == senha_banco:  # Comparação direta (substitua por bcrypt em produção)
            print("Debug: Senha correta! Usuário autenticado.")  # Debug
            cursor.close()
            conexao.close()
            return role  # Retorna o role (1 para admin, 0 para porteiro)
        else:
            print("Debug: Senha incorreta!")  # Debug
    else:
        print("Debug: Usuário não encontrado no banco de dados.")  # Debug

    cursor.close()
    conexao.close()
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