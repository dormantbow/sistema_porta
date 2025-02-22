import streamlit as st
import requests

# Corrigindo a URL base sem barra no final
API_BASE_URL = "http://localhost:8000/api/auth/"

def authenticate_user(username, password):
    """ Faz requisição para o backend e retorna o token JWT """
    url = f"{API_BASE_URL}login/" # Agora está correto
    data = {"username": username, "password": password}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.json()  # Retorna o token e as infos do usuário
    else:
        return None

def show():
    st.title("Login")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.token = None

    if st.session_state.authenticated:
        st.success(f"Bem-vindo, {st.session_state.username}!")

        if st.button("Ir para Home"):
            st.session_state.current_page = "home"
            st.rerun()

        if st.button("Sair"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.token = None  # Apaga o token ao sair
            st.session_state.current_page = "login"
            st.rerun()
    else:
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            user_data = authenticate_user(username, password)

            if user_data:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.token = user_data["access_token"]
                st.success("Login bem-sucedido!")
                st.session_state.current_page = "home"
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos!")
