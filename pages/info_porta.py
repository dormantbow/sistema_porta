import streamlit as st
import requests

API_URL = "http://de2b-2804-1b1-a940-f79a-682b-4a2b-6135-5068.ngrok-free.app/api/room/{id}/"

def show():
    st.title("Detalhes da Sala")

    # Verifica se há um ID de porta armazenado na sessão
    if "selected_door_id" not in st.session_state or st.session_state.selected_door_id is None:
        st.warning("Nenhuma porta selecionada.")
        return

    porta_id = st.session_state.selected_door_id  # Obtém o ID salvo na sessão

    # Tenta buscar os detalhes da porta na API
    try:
        response = requests.get(API_URL.format(id=porta_id))  # Corrigido aqui
        st.write(f"Debug: Resposta da API = {response.text}")  # Log para depuração

        if response.status_code == 200:
            door_info = response.json()

            st.subheader(f"Nome: {door_info['name']}")  # Corrigindo a chave do JSON
            st.write(f"**Código:** {door_info['code']}")
            st.write(f"**Departamento:** {door_info['department']['name']}")

            # Exibir coordenadores do departamento
            if door_info["department"]["coordinators"]:
                coordinators = ", ".join(coord["user"] for coord in door_info["department"]["coordinators"])
                st.write(f"**Coordenadores:** {coordinators}")
            else:
                st.write("**Coordenadores:** Nenhum")

            # Exibir administradores
            if door_info["admin"]:
                admins = ", ".join(admin["user"] for admin in door_info["admin"])
                st.write(f"**Administradores:** {admins}")
            else:
                st.write("**Administradores:** Nenhum")

        else:
            st.error(f"Erro ao buscar dados da API. Código: {response.status_code}")

    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão com a API: {e}")

    # Botão para voltar à home
    if st.button("Voltar"):
        st.session_state.current_page = "home"
        st.rerun()
