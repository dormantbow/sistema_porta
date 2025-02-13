import streamlit as st
import mysql.connector
import sqlite3
import bcrypt

conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'admin123',
    database = 'bdporteiros',
)

cursor = conexao.cursor()

import streamlit as st

def create(nome, cpf, senha):
    

    # Query parametrizada para evitar SQL Injection
    comando = f'INSERT INTO porteiros (nomeCompleto, cpf, senha) VALUES ("{nome}", {cpf}, "{senha}")'
    cursor.execute(comando)
    conexao.commit() # edita o banco de dados
    conexao.close()

with st.form("my_form"):
    st.write("Cadastrar novo porteiro")
    nome = st.text_input("Nome completo:")
    cpf = st.text_input("CPF:")
    senha = st.text_input("Senha:", type="password")
    
    # Every form must have a submit button.
    submitted = st.form_submit_button("Enviar")
    if submitted:
        create(nome, cpf, senha)
        st.success('Porteiro adicionado com sucesso', icon="✅")
        





#read
# comando = f'SELECT * FROM vendas '
# cursor.execute(comando)
# resultado = cursor.fetchall() #ler o banco de dados
# print(resultado)


#update
# nomeProduto = "todynho"
# valor = 6
# comando = f'UPDATE vendas SET valor = {valor} WHERE nomeProduto = "{nomeProduto}"'
# cursor.execute(comando)
# conexao.commit() # edita o banco de dados



#delete
# nomeProduto = "todynho"
# comando = f'DELETE from vendas WHERE nomeProduto = "{nomeProduto}"'
# cursor.execute(comando)
# conexao.commit() # edita o banco de dados

cursor.close()
conexao.close()