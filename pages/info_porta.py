import streamlit as st
import requests
from fpdf import FPDF
from datetime import datetime

API_URL = "http://192.168.159.236:8080/api/room/{id}/"

# Função para extrair logs do JSON retornado pela API
def fetch_logs(door_info):
    logs = []
    if "iotobjects" in door_info and door_info["iotobjects"]:
        first_iot_object = door_info["iotobjects"][0]  # Pega o primeiro objeto IoT
        if "log" in first_iot_object:
            logs = first_iot_object["log"]
    return logs

# Função que gera o relatório com logs
def generate_pdf_with_logs(door_info, logs, start_date, end_date):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Relatório da Sala", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Nome: {door_info['name']}", ln=True)
    pdf.cell(200, 10, f"Código: {door_info['code']}", ln=True)
    pdf.cell(200, 10, f"Departamento: {door_info['department']['name']}", ln=True)

    # Coordenadores
    coordinators = ", ".join(coord["user"] for coord in door_info["department"].get("coordinators", [])) or "Nenhum"
    pdf.cell(200, 10, f"Coordenadores: {coordinators}", ln=True)

    # Administradores
    admins = ", ".join(admin["user"] for admin in door_info.get("admin", [])) or "Nenhum"
    pdf.cell(200, 10, f"Administradores: {admins}", ln=True)

    pdf.ln(10)

    # Formatando as datas para o padrão brasileiro
    start_date_br = start_date.strftime("%d/%m/%Y")
    end_date_br = end_date.strftime("%d/%m/%Y")

    pdf.cell(200, 10, f"Período: {start_date_br} - {end_date_br}", ln=True)

    # Logs da Sala
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Logs de Acesso", ln=True)
    pdf.set_font("Arial", size=10)
    
    for log in logs:
        timestamp = log.get("date", "Data desconhecida")
        event = log.get("command", "Evento desconhecido")
        user = log.get("user", "Usuário desconhecido")
        pdf.cell(200, 10, f"{timestamp} - {event} - {user}", ln=True)

    # Criando o nome do arquivo com base no código da sala
    room_code = door_info['code'].replace(" ", "_")
    pdf_filename = f"relatorio_sala_{room_code}.pdf"

    pdf.output(pdf_filename)
    return pdf_filename

# Estrutura da página
def show():
    st.title("Detalhes da Sala")

    if "selected_door_id" not in st.session_state or st.session_state.selected_door_id is None:
        st.warning("Nenhuma porta selecionada.")
        return

    if "token" not in st.session_state:
        st.error("Você precisa estar logado para acessar essa página.")
        return

    porta_id = st.session_state.selected_door_id
    token = st.session_state.token

    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(API_URL.format(id=porta_id), headers=headers)
        
        if response.status_code == 200:
            door_info = response.json()

            st.subheader(f"Nome: {door_info['name']}")
            st.write(f"**Código:** {door_info['code']}")
            st.write(f"**Departamento:** {door_info['department']['name']}")

            # Exibir coordenadores do departamento
            if door_info["department"].get("coordinators"):
                coordinators = ", ".join(coord["user"] for coord in door_info["department"]["coordinators"])
                st.write(f"**Coordenadores:** {coordinators}")
            else:
                st.write("**Coordenadores:** Nenhum")

            # Exibir administradores
            if door_info.get("admin"):
                admins = ", ".join(admin["user"] for admin in door_info["admin"])
                st.write(f"**Administradores:** {admins}")
            else:
                st.write("**Administradores:** Nenhum")

            # Buscar logs dentro de door_info
            logs = fetch_logs(door_info)

            # Gerar relatório PDF com logs e filtro por data
            st.subheader("Gerar Relatório PDF com Logs")
            start_date = st.date_input("Data Inicial", datetime.today())
            end_date = st.date_input("Data Final", datetime.today())

            if st.button("Gerar PDF com Logs"):
                pdf_filename = generate_pdf_with_logs(door_info, logs, start_date, end_date)
                with open(pdf_filename, "rb") as file:
                    st.download_button("Baixar Relatório PDF com Logs", file, file_name=pdf_filename, mime="application/pdf")
        else:
            st.error(f"Erro ao buscar dados da API. Código: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão com a API: {e}")

    if st.button("Voltar"):
        st.session_state.current_page = "home"
        st.rerun()

    # Rodapé
    st.markdown(
        '<p style="text-align:center; margin-top:30px; color:gray;">'
        '2025. Desenvolvido por EJ Turing Consultoria e Desenvolvimento.</p>',
        unsafe_allow_html=True
    )
