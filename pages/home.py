import streamlit as st
import requests

def get_doors():
    """Função para buscar dados da API"""
    api_url = "https://c886-2804-16d8-c6fe-100-3c79-9e2b-5b62-8a35.ngrok-free.app/api/room/listAll/"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()  # Retorna os dados como JSON
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar dados da API: {e}")
        return None  # Retorna None em caso de erro

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
            if st.button("Modificar Senha"):
                st.write("Funcionalidade em construção.")
            if st.button("Sair"):
                st.session_state.authenticated = False  # Controla o estado do login
                st.switch_page("main.py")  # Redireciona para a página de login

    # Adicionando o botão "Acessar Página do Porteiro" para administradores
    if st.session_state.role == 1:  # Verifica se o usuário é admin (role = 1)
        if st.button("Acessar Página do Porteiro"):
            st.session_state.current_page = "porteiro"
            st.rerun()

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
            status = "Ativo" if door["admin"] else "Inativo"  # Define status baseado na presença de admins
            
            st.markdown(
                f"""
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 10px; text-align: center; background: white;">
                    <h4 style="margin: 0; color: black;">{door["name"]}</h4>
                    <span style="color: {'green' if status == 'Ativo' else 'red'}; font-weight: bold; border: 1px solid; padding: 5px; border-radius: 5px;">
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