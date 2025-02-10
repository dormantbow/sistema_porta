import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/portas/{porta_id}"  # URL da API local

def show():
    st.title("Detalhes da Porta")

    # Verifica se há um ID de porta armazenado na sessão
    if "selected_door_id" not in st.session_state or st.session_state.selected_door_id is None:
        st.warning("Nenhuma porta selecionada.")
        return

    porta_id = st.session_state.selected_door_id  # Obtém o ID salvo na sessão

    # Tenta buscar os detalhes da porta na API
    try:
        response = requests.get(API_URL.format(porta_id=porta_id))
        st.write(f"Debug: Resposta da API = {response.text}")  # Log para depuração
        if response.status_code == 200:
            door_info = response.json()

            if "erro" not in door_info:
                st.subheader(f"Nome: {door_info['nome']}")
                st.write(f"**Status:** {door_info['status']}")
                st.write(f"**Categoria:** {door_info['categoria']}")

                # Exibir localização, se existir
                if "localizacao" in door_info:
                    st.write(f"**Localização:** {door_info['localizacao']}")

                # Exibir responsáveis, se existir
                if "responsaveis" in door_info and isinstance(door_info["responsaveis"], list):
                    st.write(f"**Responsáveis:** {', '.join(door_info['responsaveis'])}")

            else:
                st.error("Porta não encontrada.")

        else:
            st.error(f"Erro ao buscar dados da API. Código: {response.status_code}")

    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão com a API: {e}")

    # Botão para voltar à home
    if st.button("Voltar"):
        st.session_state.current_page = "home"
        st.rerun()
