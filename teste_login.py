from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def esperar_elemento(driver, by, valor, timeout=10):
    """Aguarda um elemento aparecer na página antes de continuar."""
    for _ in range(timeout):
        try:
            elemento = driver.find_element(by, valor)
            if elemento.is_displayed():
                return elemento
        except:
            pass
        time.sleep(1)
    raise Exception(f"Elemento {valor} não encontrado!")

# Inicializa o WebDriver
driver = webdriver.Chrome()
driver.get("http://localhost:8501")  # Ajuste conforme necessário
time.sleep(5)  # Aguarda a página carregar

# Preenche os campos de login
campo_usuario = esperar_elemento(driver, By.XPATH, "//input[@aria-label='Usuário']")
campo_usuario.send_keys("Guarita")  

campo_senha = esperar_elemento(driver, By.XPATH, "//input[@aria-label='Senha']")
campo_senha.send_keys("Porta123@", Keys.RETURN)  # Envia a senha e confirma com Enter

time.sleep(5)  # Aguarda a página processar o login

# Verifica se o login foi bem-sucedido
if "Bem-vindo" not in driver.page_source:
    print("✅ Login realizado com sucesso!")
else:
    print("❌ Falha no login!")
    driver.quit()
    exit()

# Aguarda o painel de portas carregar
esperar_elemento(driver, By.XPATH, "//h2[contains(text(), 'Painel de Portas')]")
print("✅ Painel de Portas carregado!")

# Teste de busca e reset de filtro
def testar_busca_portas(driver, termo_busca):
    """Testa a funcionalidade de busca de portas e depois limpa a busca."""
    search_input = esperar_elemento(driver, By.XPATH, "//input[@placeholder='Digite o nome da porta...']")
    
    # Buscar um termo específico
    search_input.clear()
    search_input.send_keys(termo_busca, Keys.ENTER)
    time.sleep(5)  # Aguarda os resultados aparecerem

    if termo_busca in driver.page_source:
        print(f"✅ Busca por '{termo_busca}' funcionou corretamente!")
    else:
        print(f"❌ A busca por '{termo_busca}' falhou!")
    
    # Limpar o campo de busca corretamente
    search_input.send_keys(Keys.CONTROL + "a")  # Seleciona tudo
    search_input.send_keys(Keys.BACKSPACE)  # Apaga completamente

    time.sleep(5)  # Aguarda um pouco antes de confirmar que limpou
    
    # Verifica se o campo está realmente vazio antes de continuar
    if search_input.get_attribute("value") == "":
        print("✅ Campo de busca foi completamente limpo!")
    else:
        print("❌ Falha ao limpar campo de busca!")

    # Aguarda a lista de portas ser restaurada após a limpeza
    time.sleep(5)  # Tempo para a lista ser restaurada
    search_input.send_keys(Keys.ENTER)  # Aciona a busca vazia para resetar a lista
    time.sleep(5)  # Tempo para a lista ser restaurada

    # Verificar se a lista completa foi restaurada
    todas_as_portas = driver.find_elements(By.XPATH, "//div[contains(@class, 'stButton')]")
    if len(todas_as_portas) > 0:
        print(f"✅ Lista de portas recarregada com sucesso! ({len(todas_as_portas)} portas encontradas)")
    else:
        print("❌ Erro ao recarregar a lista de portas!")

# Executa o teste de busca
testar_busca_portas(driver, "Latin")

# Aguarda a lista de portas ser restaurada após a limpeza
time.sleep(5)  # Tempo para a lista ser restaurada

# Depuração: Exibe o HTML da lista de portas
lista_portas = driver.find_element(By.XPATH, "//div[contains(@class, 'stButton')]")
print("HTML da lista de portas:")
print(lista_portas.get_attribute("innerHTML"))

# Encontra todos os botões de seleção de portas
botoes_selecionar = driver.find_elements(By.XPATH, "//button[contains(@class, 'stButton') and contains(text(), 'Selecionar')]")

if len(botoes_selecionar) > 0:
    print(f"✅ Botões de seleção encontrados! ({len(botoes_selecionar)} botões)")
    
    # Itera sobre cada botão de seleção
    for botao in botoes_selecionar:
        try:
            # Clica no botão "Selecionar [Nome da Porta]"
            nome_porta = botao.text.replace("Selecionar ", "")  # Extrai o nome da porta do texto do botão
            botao.click()
            print(f"✅ Botão 'Selecionar {nome_porta}' clicado com sucesso!")
            
            # Aguarda um pouco para a ação ser processada
            time.sleep(3)
            
            # Verifica se a página de informações foi carregada corretamente
            if "Informações da Porta" in driver.page_source:
                print(f"✅ Página de informações da porta '{nome_porta}' carregada com sucesso!")
            else:
                print(f"❌ Falha ao carregar a página de informações da porta '{nome_porta}'!")
            
            # Volta para a lista de portas (ajuste o seletor conforme necessário)
            botao_voltar = esperar_elemento(driver, By.XPATH, "//button[contains(text(), 'Voltar')]")
            botao_voltar.click()
            print("✅ Volta para a lista de portas realizada com sucesso!")
            
            # Aguarda a lista de portas ser recarregada
            time.sleep(3)
            
        except Exception as e:
            print(f"❌ Erro ao interagir com o botão de seleção: {e}")
else:
    print("❌ Nenhum botão de seleção encontrado!")
# Mantém o navegador aberto por mais tempo para verificação manual
time.sleep(10)

# Fecha o navegador
driver.quit()