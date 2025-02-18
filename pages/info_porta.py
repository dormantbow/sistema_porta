import streamlit as st
import requests
from fpdf import FPDF
from datetime import datetime

API_URL = "https://313b-2804-16d8-c6fe-100-880a-58a-e138-cae0.ngrok-free.app/api/room/{id}/"
LOGS_API_URL = "https://ade4-2804-16d8-c6fe-100-880a-58a-e138-cae0.ngrok-free.app/api/logs/{id}/"

#função que gera o relatório com logs
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
        pdf.cell(200, 10, f"{log['timestamp']} - {log['event']} - {log['user']}", ln=True)

    # Criando o nome do arquivo com base no código da sala
    room_code = door_info['code'].replace(" ", "_")
    pdf_filename = f"relatorio_sala_{room_code}.pdf"

    pdf.output(pdf_filename)
    return pdf_filename

#exibe os logs
def show_logs(porta_id):
    try:
        response = requests.get(LOGS_API_URL.format(id=porta_id))
        if response.status_code == 200:
            logs = response.json()
            st.subheader("Logs da Sala")
            for log in logs:
                st.write(f"{log['timestamp']} - {log['event']} - {log['user']}")
            return logs
        else:
            st.error(f"Erro ao buscar logs. Código: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão com a API: {e}")
        return []
#estrutura da pagina
def show():
    st.title("Detalhes da Sala")

    if "selected_door_id" not in st.session_state or st.session_state.selected_door_id is None:
        st.warning("Nenhuma porta selecionada.")
        return

    porta_id = st.session_state.selected_door_id

    try:
        response = requests.get(API_URL.format(id=porta_id))
        if response.status_code == 200:
            door_info = response.json()

            st.subheader(f"Nome: {door_info['name']}")
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

            # Exibir logs
            logs = show_logs(porta_id)

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