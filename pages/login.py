import streamlit as st
from utils.auth import check_credentials

def show():
    st.title("Login")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None

    if st.session_state.authenticated:
        st.success(f"Bem-vindo, {st.session_state.username} ({st.session_state.role})!")
        if st.button("Ir para Home"):
            st.session_state.current_page = "home"
            st.rerun()
        if st.button("Sair"):
            st.session_state.authenticated = False
            st.session_state.current_page = "login"
            st.rerun()
    else:
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            role = check_credentials(username, password)
            if role:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = role
                st.session_state.current_page = "home"  # Redireciona para a home
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos!")
