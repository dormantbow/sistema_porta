import streamlit as st

# Simular Navbar Superior
def navbar(menu_items):
    # Cria botões para cada item do menu
    selected_page = st.radio(
        "",  # Título vazio para evitar rótulo desnecessário
        menu_items,
        horizontal=True,  # Dispor os botões horizontalmente
        key="navbar",
        label_visibility="collapsed",  # Remove o título visível
    )
    return selected_page


# Define os itens do menu
menu = ["Home", "Login", "Dashboard", "Configurações"]
page = navbar(menu)  # Exibe a navbar e retorna a página selecionada

# Conteúdo baseado na página selecionada
if page == "Home":
    st.title("Bem-vindo à Home!")
    st.write("Esta é a página inicial da sua aplicação.")
elif page == "Login":
    st.title("Login")
    st.write("Tela de login em desenvolvimento.")
elif page == "Dashboard":
    st.title("Dashboard")
    st.write("Bem-vindo ao painel de controle.")
elif page == "Configurações":
    st.title("Configurações")
    st.write("Aqui você pode ajustar suas preferências.")
    
    

# CSS para remover a barra lateral padrão
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
