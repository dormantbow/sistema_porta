import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.email_sender import send_error_report

def show():
    """Tela para relatar erros no sistema."""

    st.write("Carregando página de relatório de erros...")  # Debug

    # NÃO CHAME `st.set_page_config()` AQUI SE JÁ FOI CHAMADO EM `main.py`
    
    st.title("📩 Informar Erro")

    user_email = st.text_input("Seu e-mail", placeholder="Digite seu e-mail para contato...")

    error_description = st.text_area("Descrição do erro ", placeholder="Descreva o erro encontrado...")

    if st.button("Enviar"):
        if not user_email or not error_description:
            st.warning("Por favor, preencha todos os campos.")
        else:
            success = send_error_report(user_email, error_description)
            if success:
                st.success("Erro relatado com sucesso! Nossa equipe entrará em contato em breve.")
            else:
                st.error("Falha ao enviar o erro. Tente novamente mais tarde.")

    if st.button("Voltar"):
        st.session_state.current_page = "home"
        st.rerun()

    # Rodapé
    st.markdown(
        '<p style="text-align:center; margin-top:30px; color:gray;">'
        '2025. Desenvolvido por EJ Turing Consultoria e Desenvolvimento.</p>',
        unsafe_allow_html=True
    )