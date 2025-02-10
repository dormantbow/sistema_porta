import streamlit as st
from utils.auth import check_credentials  # Importa a função de autenticação

def show():
    st.title("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        role = check_credentials(username, password)  # Verifica as credenciais
        if role:
            st.session_state.authenticated = True  # Marca o usuário como autenticado
            st.session_state.user_role = role  # Armazena o papel do usuário
            st.session_state.current_page = "home"  # Redireciona para a página inicial
            st.experimental_rerun()  # Recarrega a aplicação
        else:
            st.error("Usuário ou senha inválidos.")
