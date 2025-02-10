import streamlit as st
import requests

def get_doors():
    """Função para buscar dados da API"""
    api_url = "http://de2b-2804-1b1-a940-f79a-682b-4a2b-6135-5068.ngrok-free.app/api/room/listAll/"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        try:
            return response.json()  # Retorna os dados como JSON
        except ValueError:
            st.error("Erro: A resposta da API não é um JSON válido.")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar dados: {e}")
        return []

def show():
    """Função chamada pelo main.py para exibir a tela"""

    # Buscar dados da API
    doors = get_doors()

    # Verifica se há portas carregadas antes de tentar filtrá-las
    if not doors:
        st.warning("Nenhuma porta encontrada.")
        return

    # Barra superior com busca e filtros
    st.markdown("<h2 style='text-align: center;'>Painel de Portas</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2])

    with col1:
        search_query = st.text_input("Buscar porta", placeholder="Digite o nome da porta...")

    with col2:
        categories = list(set(door["department"]["name"] for door in doors)) if doors else []
        selected_category = st.selectbox("Filtrar por Departamento", ["Todos"] + categories)

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
