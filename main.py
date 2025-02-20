import streamlit as st
from pages import home, info_porta, login, report_error, porteiro# Certifique-se de que os arquivos existem!
from utils import auth

st.set_page_config(
    page_title="Sistema de Portas",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"  # Oculta a barra lateral
)

# Inicializa variáveis de sessão
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"
if "role" not in st.session_state:
    st.session_state.role = None  # Adiciona uma variável para o role

# Se não estiver autenticado, garante que a página de login seja mostrada
if not st.session_state.authenticated:
    print("Debug: Usuário não autenticado. Redirecionando para a página de login.")  # Debug
    st.session_state.current_page = "login"
    login.show()
else:
    print(f"Debug: Usuário autenticado. Página atual: {st.session_state.current_page}")  # Debug
    if st.session_state.current_page == "login":
        login.show()
    elif st.session_state.current_page == "home":
        home.show()
    elif st.session_state.current_page == "info_porta":
        info_porta.show()
    elif st.session_state.current_page == "report_error":
        report_error.show()
    elif st.session_state.current_page == "porteiro":
        if st.session_state.role == 1:  # Verifica se o usuário é admin (role = 1)
            print("Debug: Usuário é admin. Acessando página do porteiro.")  # Debug
            porteiro.show()
        else:
            print("Debug: Usuário não tem permissão para acessar a página do porteiro.")  # Debug
            st.error("Você não tem permissão para acessar esta página. Apenas administradores podem acessá-la.")
            st.session_state.current_page = "home"  # Redireciona para a página inicial
            st.rerun()