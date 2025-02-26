import streamlit as st
import requests
import json
import time

def get_doors():
    """Função para buscar dados da API"""
    
    # Verifique se o token está presente
    if "token" not in st.session_state:
        st.error("Você precisa estar logado para acessar essa página.")
        st.stop()  # Para a execução do código aqui
    
    api_url = "http://192.168.159.236:8080/api/room/listAll/"
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"  # Corrigido aqui
    }

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Retorna a lista de portas
        else:
            st.error(f"Erro ao buscar as portas: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Ocorreu um erro ao tentar se conectar à API: {e}")
        return None

def show():
    """Função chamada pelo main.py para exibir a tela"""
    
    st.markdown("<h2 style='text-align: center;'>Painel de Portas</h2>", unsafe_allow_html=True)

    # Atualização automática
    refresh_time = 10  # Tempo em segundos para atualizar
    placeholder = st.empty()  # Espaço reservado para atualização

    while True:
        with placeholder.container():
            doors = get_doors()

            if doors is None:
                st.warning("Não foi possível carregar os dados. Verifique sua conexão ou tente novamente.")
                if st.button("Tentar novamente 🔄"):
                    st.rerun()
                return

            if not doors:
                st.warning("Nenhuma porta encontrada.")
                return

            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                search_query = st.text_input("Buscar porta", placeholder="Digite o nome da porta...")

            with col2:
                categories = list(set(door["department"]["name"] for door in doors)) if doors else []
                selected_category = st.selectbox("Filtrar por Departamento", ["Todos"] + categories)
            
            with col3:
                with st.expander("Opções"):
                    if st.button("Informar erro"):
                        st.session_state.current_page = "report_error"
                        st.rerun()
                    if st.button("Sair"):
                        st.session_state.authenticated = False
                        st.switch_page("main.py")

            # Filtragem
            filtered_doors = [
                door for door in doors
                if (search_query.lower() in door["name"].lower()) and
                (selected_category == "Todos" or door["department"]["name"] == selected_category)
            ]

            if not filtered_doors:
                st.warning("Nenhuma porta encontrada com os filtros aplicados.")
                return

            st.write(f"Total de portas encontradas: {len(filtered_doors)}")
            cols = st.columns(min(4, len(filtered_doors)))

            for idx, door in enumerate(filtered_doors):
                with cols[idx % 4]:
                    iotobjects = door.get("iotobjects", [])
                    if iotobjects:
                        status = iotobjects[0].get("status", "Status não disponível")
                    st.markdown(
                        f"""
                        <div style="border: 1px solid #ddd; padding: 15px; border-radius: 10px; text-align: center; background: white;">
                            <h4 style="margin: 0; color: black;">{door["name"]}</h4>
                            <span style="color: {'green' if status == 'Disponível' else 'red'}; font-weight: bold; border: 1px solid; padding: 5px; border-radius: 5px;">
                                {status}
                            </span>
                        </div>
                        """, unsafe_allow_html=True
                    )
                    if st.button(f"Selecionar {door['name']}", key=f"btn_{door['id']}"):
                        st.session_state["selected_door_id"] = door["id"]
                        st.session_state["current_page"] = "info_porta"
                        st.rerun()

            st.markdown(
                '<p style="text-align:center; margin-top:30px; color:gray;">'
                '2025. Desenvolvido por EJ Turing Consultoria e Desenvolvimento.</p>',
                unsafe_allow_html=True
            )

        time.sleep(refresh_time)
        st.rerun()  # Força a atualização da página

