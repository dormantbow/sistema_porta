import streamlit as st
from pages import home, info_porta, login  # Certifique-se de que as páginas estão corretamente configuradas
from utils.auth import check_credentials  # Importa a função de verificação do auth.py

st.set_page_config(page_title="Portal Fácil", layout="wide")

# Inicializa as variáveis de sessão
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False  # Usuário não autenticado por padrão
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"  # Página inicial padrão

# Verifica o estado de autenticação
if not st.session_state.authenticated:
    st.session_state.current_page = "login"

# Redireciona para a página correta
if st.session_state.current_page == "login":
    login.show()  # Chama a função de exibição do login
elif st.session_state.current_page == "home":
    home.show()
elif st.session_state.current_page == "door_info":
    info_porta.show()
