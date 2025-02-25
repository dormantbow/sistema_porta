from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


# Inicializa o WebDriver do Chrome
driver = webdriver.Chrome()

# Abre a página do login no Streamlit
driver.get("http://localhost:8501")  # Altere se precisar

time.sleep(3)  # Espera a página carregar

# Preenche o campo de usuário
campo_usuario = driver.find_element(By.XPATH, "//input[@aria-label='Usuário']")
campo_usuario.send_keys("Guarita")  # Substitua por um usuário válido

# Preenche o campo de senha
campo_senha = driver.find_element(By.XPATH, "//input[@aria-label='Senha']")
campo_senha.send_keys("Porta123@")

# Clica no botão de login
campo_senha.send_keys(Keys.RETURN)

time.sleep(3)  # Espera o login ser processado

# Verifica se o login foi bem-sucedido
if "Bem-vindo" in driver.page_source:
    print("✅ Login realizado com sucesso!")
else:
    print("❌ Falha no login!")

# Fecha o navegador
time.sleep(10)
driver.quit()
