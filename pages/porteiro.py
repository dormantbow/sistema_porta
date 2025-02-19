import streamlit as st
import mysql.connector
import sqlite3
import bcrypt
from validate_docbr import CPF

def show():
    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'root',
        database = 'bdporteiros',
    )

    cursor = conexao.cursor()


    def validar_cpf(cpf):
        cpf_validator = CPF()
        return cpf_validator.validate(cpf)

    def create(nome, cpf, senha):
        

        # Query parametrizada para evitar SQL Injection
        comando = f'INSERT INTO usuario (nomeCompleto, cpf, senha, role) VALUES ("{nome}", {cpf}, "{senha}", 0)'
        cursor.execute(comando)
        conexao.commit() # edita o banco de dados
        conexao.close()

    with st.form("my_form"):
        st.write("Cadastrar novo porteiro")
        nome = st.text_input("Nome completo:")
        cpf = st.text_input("CPF:")

        
        st.warning("⚠️ Digite um CPF válido com 11 números.")


        senha = st.text_input("Senha:", type="password")
        
        # Every form must have a submit button.
        submitted = st.form_submit_button("Enviar")
        if submitted:
            if cpf.isdigit() and len(cpf) == 11:
                if validar_cpf(cpf):
                    create(nome, cpf, senha)
                    st.success('Porteiro adicionado com sucesso', icon="✅")
                else:
                    st.error("❌ CPF Inválido!")
            else:
                st.warning("⚠️ Digite um CPF válido com 11 números.")
            
            





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