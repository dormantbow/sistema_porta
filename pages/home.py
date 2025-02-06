import streamlit as st
import requests

def get_doors():
    """Função para buscar dados da API"""
    api_url = "http://127.0.0.1:8000/portas"  # Substitua pela URL real da API
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()  # Retorna os dados como JSON
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar dados: {e}")
        return []

def show():
    """Função chamada pelo main.py para exibir a tela"""

    # Buscar dados da API
    doors = get_doors()

    # Barra superior com busca e filtros
    st.markdown("<h2 style='text-align: center;'>Painel de Portas</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([3, 2, 1])

    with col1:
        search_query = st.text_input("Buscar porta", placeholder="Digite o nome da porta...")

    with col2:
        categories = list(set(door["categoria"] for door in doors)) if doors else []
        selected_category = st.selectbox("Filtrar", ["Todas"] + categories)

    with col3:
        st.button("Opções", key="options")

    # Filtrar portas conforme a busca e categoria
    filtered_doors = [
        door for door in doors
        if (search_query.lower() in door["nome"].lower()) and
           (selected_category == "Todas" or door["categoria"] == selected_category)
    ]

    # Exibir as portas
    st.write("")
    cols = st.columns(4)

    for idx, door in enumerate(filtered_doors):
        with cols[idx % 4]:
            st.markdown(
                f"""
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 10px; text-align: center; background: white;">
                    <h4 style="margin: 0;">{door["nome"]}</h4>
                    <span style="color: {'red' if door['status'] == 'ABERTO' else 'green'}; font-weight: bold; border: 1px solid; padding: 5px; border-radius: 5px;">
                        {door["status"]}
                    </span>
                </div>
                """, unsafe_allow_html=True
            )

    # Rodapé
    st.markdown(
        '<p style="text-align:center; margin-top:30px; color:gray;">'
        '2025. Desenvolvido por EJ Turing Consultoria e Desenvolvimento.</p>',
        unsafe_allow_html=True
    )
