import streamlit as st
import requests
import json
def get_doors():
    """Função para buscar dados da API"""
    
    # Verifique se o token está presente
    if "token" not in st.session_state:
        st.error("Você precisa estar logado para acessar essa página.")
        st.stop()  # Para a execução do código aqui
    
    api_url = "http://localhost:8000/api/room/listAll/"
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"  # Corrigido aqui
    }
    #st.write(f"Headers enviados: {headers}")  # Debug
    #st.write(f"Token armazenado: {st.session_state.token}")

    try:
        #st.write("Headers enviados:", json.dumps(headers, indent=2))  # Debug
        # Faz a requisição à API
        response = requests.get(api_url, headers=headers)
        
        # Verifica o status da resposta
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

    # Buscar dados da API
    doors = get_doors()

    # Se houver erro ao carregar as portas, exibir botão de tentativa
    if doors is None:
        st.warning("Não foi possível carregar os dados. Verifique sua conexão ou tente novamente.")
        if st.button("Tentar novamente 🔄"):
            st.rerun()
        return

    # Verifica se há portas carregadas antes de tentar filtrá-las
    if not doors:
        st.warning("Nenhuma porta encontrada.")
        return

    # Barra superior com busca e filtros
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
                st.session_state.authenticated = False  # Controla o estado do login
                st.switch_page("main.py")  # Redireciona para a página de login

    if st.session_state.authenticated:
        portas = get_doors()
        #if portas:
            #st.write("Lista de Portas:")
            #st.json(portas)  # Exibe o JSON das portas

    # Filtrar portas conforme a busca e categoria
    filtered_doors = [
        door for door in doors
        if (search_query.lower() in door["name"].lower()) and
           (selected_category == "Todos" or door["department"]["name"] == selected_category)
    ]

    # Verifica se há portas após o filtro
    if not filtered_doors:
        st.warning("Nenhuma porta encontrada com os filtros aplicados.")
        return

    # Exibir as portas no layout correto
    st.write(f"Total de portas encontradas: {len(filtered_doors)}")
    cols = st.columns(min(4, len(filtered_doors)))

    for idx, door in enumerate(filtered_doors):
        with cols[idx % 4]:
            status = "Disponível" if door["admin"] else "Indisponível"  # Define status baseado na presença de admins
            
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

    # Rodapé
    st.markdown(
        '<p style="text-align:center; margin-top:30px; color:gray;">'
        '2025. Desenvolvido por EJ Turing Consultoria e Desenvolvimento.</p>',
        unsafe_allow_html=True
    )
