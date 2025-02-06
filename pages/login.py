import streamlit as st
from utils import auth

def show():
    st.title("Login")
    username = st.text_input("R.A/CPF")
    password = st.text_input("Senha", type="password")
    
    col1, col2 = st.columns([2, 1])  # Cria duas colunas para alinhar os botões
    
    with col1:
        if st.button("Entrar"):
            role = auth.check_credentials(username, password)
            if role:
                st.session_state.authenticated = True
                st.session_state.role = role  # Armazena o papel do usuário
                st.experimental_rerun()  # Recarrega o app para mudar de tela
            else:
                st.error("Usuário ou senha incorretos")
    
    with col2:
        if st.button("Esqueci minha senha"):
            st.session_state.show_reset_password = True  # Marca que a tela de redefinição deve ser exibida
            st.experimental_rerun()

    # Exibe o formulário de redefinição de senha, se ativado
    if st.session_state.get("show_reset_password", False):
        show_reset_password()


def show_reset_password():
    st.title("Redefinição de Senha")
    email = st.text_input("Digite seu e-mail registrado")
    
    if st.button("Enviar link de redefinição"):
        # Lógica para enviar e-mail com link de redefinição
        # Aqui você pode usar uma função, como `auth.send_reset_email(email)`
        if auth.send_reset_email(email):  # Supondo que esta função já existe
            st.success("E-mail de redefinição enviado! Verifique sua caixa de entrada.")
        else:
            st.error("E-mail não encontrado. Verifique os dados.")
    
    if st.button("Voltar ao login"):
        st.session_state.show_reset_password = False
        st.experimental_rerun()


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

