import streamlit as st
import requests

def get_doors():
    """Função para buscar dados da API"""
    api_url = "http://127.0.0.1:4040/portas"  # Substitua pela URL real da API
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
    col1, col2, col3 = st.columns([3, 2, 1])

    with col1:
        search_query = st.text_input("Buscar porta", placeholder="Digite o nome da porta...")

    with col2:
        categories = list(set(door["categoria"] for door in doors)) if doors else []
        selected_category = st.selectbox("Filtrar", ["Todas"] + categories)

    with col3:
<<<<<<< Updated upstream
        with st.expander("Opções"):
            if st.button("Informar erro"):
                st.write("Funcionalidade em construção.")

            if st.button("Modificar Senha"):
                st.write("Funcionalidade em construção.")
                
            if st.button("Sair"):
                st.session_state.authenticated = False # Controla o estado do login
                st.switch_page("main.py") # Redireciona para a página de login
=======
        with st.expander("⚙️ Opções"):
            option = st.radio("Escolha uma opção:", ["Informar erro", "Modificar senha", "Sair"])

            if option == "Informar erro":
                st.warning("Você selecionou 'Informar erro'. Aqui você pode adicionar um formulário futuramente.")

            elif option == "Modificar senha":
                st.info("Você selecionou 'Modificar senha'. Redirecionando...")  

            elif option == "Sair":
                st.session_state.authenticated = False
                st.switch_page("main.py")
                
>>>>>>> Stashed changes

    # Filtrar portas conforme a busca e categoria
    filtered_doors = [
        door for door in doors
        if (search_query.lower() in door["nome"].lower()) and
           (selected_category == "Todas" or door["categoria"] == selected_category)
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
            st.markdown(
                f"""
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 10px; text-align: center; background: white;">
                    <h4 style="margin: 0; color: black;">{door["nome"]}</h4>
                    <span style="color: {'red' if door['status'] == 'ABERTO' else 'green'}; font-weight: bold; border: 1px solid; padding: 5px; border-radius: 5px;">
                        {door["status"]}
                    </span>
                </div>
                """, unsafe_allow_html=True
            )
            if st.button(f"Selecionar {door['nome']}", key=f"btn_{door['id']}"):
                st.session_state["selected_door_id"] = door["id"]
                st.session_state["current_page"] = "door_info"
                st.rerun()

    # Rodapé
    st.markdown(
        '<p style="text-align:center; margin-top:30px; color:gray;">'
        '2025. Desenvolvido por EJ Turing Consultoria e Desenvolvimento.</p>',
        unsafe_allow_html=True
    )
