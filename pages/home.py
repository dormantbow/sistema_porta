# pages/home.py
import streamlit as st



def show():
    st.title("Bem-vindo à Página Home!")
    st.write("Você está logado com sucesso.")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.experimental_rerun()  # Recarrega o app para voltar à tela de login
def home():
    st.title("Bem-vindo à Página Home!")
    
    if st.session_state.role == "admin":
        st.write("Você é um administrador e tem acesso total.")
    elif st.session_state.role == "editor":
        st.write("Você é um editor e pode criar e editar conteúdo.")
    elif st.session_state.role == "viewer":
        st.write("Você é um visualizador e pode apenas ver o conteúdo.")
    
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.role = None
        st.experimental_rerun()  # Recarrega o app para voltar à tela de login
        
        
        
# CSS para remover a barra lateral padrão
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)