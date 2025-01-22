import tkinter as tk
from tkinter import ttk, messagebox

def sair():
    if messagebox.askyesno("Sair", "Deseja realmente sair?"):
        dashboard.destroy()

# Função para criar abas na dashboard
def criar_dashboard(usuario):
    global dashboard

    # Configuração inicial da janela
    dashboard = tk.Tk()
    dashboard.title("Dashboard - Sistema de Monitoramento")
    dashboard.geometry("800x600")

    # Cabeçalho
    frame_topo = tk.Frame(dashboard, bg="lightblue", height=50)
    frame_topo.pack(fill=tk.X)

    tk.Label(frame_topo, text=f"Bem-vindo, {usuario}", bg="lightblue", font=("Arial", 14)).pack(side=tk.LEFT, padx=10)
    btn_sair = tk.Button(frame_topo, text="Sair", command=sair, bg="red", fg="white")
    btn_sair.pack(side=tk.RIGHT, padx=10, pady=10)

    # Criar um Notebook para as abas
    notebook = ttk.Notebook(dashboard)
    notebook.pack(expand=True, fill="both")

    # Aba: Histórico das Portas
    frame_historico = tk.Frame(notebook)
    notebook.add(frame_historico, text="Histórico das Portas")

    # Tabela de histórico
    colunas = ("Porta", "Status", "Usuário", "Data", "Hora")
    tabela_historico = ttk.Treeview(frame_historico, columns=colunas, show="headings")

    for col in colunas:
        tabela_historico.heading(col, text=col)
        tabela_historico.column(col, width=100)

    tabela_historico.pack(expand=True, fill="both")
    
    # Botão para exportar
    btn_exportar = ttk.Button(frame_historico, text="Exportar Histórico", command=lambda: messagebox.showinfo("Exportar", "Funcionalidade de exportação não implementada."))
    btn_exportar.pack(pady=5)

    # Aba: Monitoramento em Tempo Real
    frame_monitoramento = tk.Frame(notebook)
    notebook.add(frame_monitoramento, text="Monitoramento em Tempo Real")

    tk.Label(frame_monitoramento, text="Portas abertas", fg="red", font=("Arial", 12)).pack(pady=5)
    lbl_abertas = tk.Label(frame_monitoramento, text="0", fg="red", font=("Arial", 16))
    lbl_abertas.pack()

    tk.Label(frame_monitoramento, text="Portas fechadas", fg="green", font=("Arial", 12)).pack(pady=5)
    lbl_fechadas = tk.Label(frame_monitoramento, text="0", fg="green", font=("Arial", 16))
    lbl_fechadas.pack()

    btn_atualizar = ttk.Button(frame_monitoramento, text="Atualizar", command=lambda: messagebox.showinfo("Atualizar", "Funcionalidade de atualização não implementada."))
    btn_atualizar.pack(pady=10)

    # Aba: Gerenciar Agendamentos
    frame_agendamentos = tk.Frame(notebook)
    notebook.add(frame_agendamentos, text="Gerenciar Agendamentos")

    tk.Label(frame_agendamentos, text="Portas disponíveis para agendamento:", font=("Arial", 12)).pack(pady=5)

    lista_portas = tk.Listbox(frame_agendamentos)
    lista_portas.pack(expand=True, fill="both", pady=5)

    # Adicionar portas exemplo
    portas_exemplo = ["Porta 1", "Porta 2", "Porta 3"]
    for porta in portas_exemplo:
        lista_portas.insert(tk.END, porta)

    btn_agendar = ttk.Button(frame_agendamentos, text="Agendar", command=lambda: messagebox.showinfo("Agendar", "Funcionalidade de agendamento não implementada."))
    btn_agendar.pack(pady=5)

    # Rodapé
    frame_rodape = tk.Frame(dashboard, bg="lightgray", height=30)
    frame_rodape.pack(fill=tk.X, side=tk.BOTTOM)

    tk.Label(frame_rodape, text="Sistema de Monitoramento de Portas - Todos os direitos reservados", bg="lightgray", font=("Arial", 10)).pack()

    dashboard.mainloop()

# Simulação de chamada após login
if __name__ == "__main__":
    criar_dashboard("Usuario Exemplo")
