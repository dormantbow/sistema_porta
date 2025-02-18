import streamlit as st
from pages import home, info_porta, login, modificar_senha  # Certifique-se de que os arquivos existem!

st.set_page_config(page_title="Portal Fácil", layout="wide")

# Inicializa variáveis de sessão
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"

# Se não estiver autenticado, garante que a página de login seja mostrada
if not st.session_state.authenticated:
    st.session_state.current_page = "login"

# Renderiza a página com base na sessão
if st.session_state.current_page == "login":
    login.show()
elif st.session_state.current_page == "home":
    home.show()
elif st.session_state.current_page == "info_porta":
    info_porta.show()
elif st.session_state.current_page == "modificar_senha":
    modificar_senha.show()
