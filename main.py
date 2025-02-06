import streamlit as st
from pages import login, home
#from components import navbar

st.set_page_config(page_title="Meu App", layout="wide")




# Chamar a navbar
#menu = ["Home", "Login", "Dashboard", "Configurações"]
#navbar.navbar(menu) 

# Criando uma variável de sessão para controle do login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Se não estiver autenticado, mostrar a tela de login
if not st.session_state.authenticated:
    login.show()
else:
    home.show()



