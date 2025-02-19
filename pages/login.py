import streamlit as st
from utils.auth import check_credentials, reset_password

def show():
    st.title("Login")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None

    if st.session_state.authenticated:
        st.success(f"Bem-vindo, {st.session_state.username}!")
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
            if check_credentials(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.current_page = "home"
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos!")

        # Botão de "Esqueceu a senha?"
        if st.button("Esqueceu a senha?"):
            st.session_state.reset_password = True
            st.rerun()

        # Lógica para redefinição de senha
        if "reset_password" in st.session_state and st.session_state.reset_password:
            st.subheader("Redefinir Senha")

            reset_user = st.text_input("Usuário do porteiro")  # O porteiro insere seu usuário
            new_password = st.text_input("Nova Senha", type="password")
            confirm_password = st.text_input("Confirmar Nova Senha", type="password")

            if st.button("Confirmar Nova Senha"):
                if new_password != confirm_password:
                    st.error("As senhas não coincidem!")
                else:
                    success = reset_password(reset_user, new_password)
                    if success:
                        st.success("Senha redefinida com sucesso! Faça login novamente.")
                        del st.session_state["reset_password"]
                        st.rerun()
                    else:   
                        st.error("Usuário não encontrado ou erro ao redefinir a senha.")
