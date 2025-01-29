import requests
import getpass

# URL correta para autenticação no SUAP
SUAP_AUTH_URL = "https://suap.ifsuldeminas.edu.br/api/v2/autenticacao/token/"

def login_suap(username, password):
    """Realiza o login no SUAP e retorna os tokens de acesso e refresh."""
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "username": username,
        "password": password,
        "grant_type": "password"
    }

    response = requests.post(SUAP_AUTH_URL, json=payload, headers=headers)

    print("Status Code:", response.status_code)  # Para depuração
    #print("Response Text:", response.text)  # Para ver a resposta da API

    if response.status_code == 200:
        try:
            data = response.json()
            access_token = data.get("access")   # Obtém o token de acesso
            refresh_token = data.get("refresh") # Obtém o refresh token

            if access_token and refresh_token:
                return access_token, refresh_token
            else:
                print("Erro: Tokens não encontrados na resposta.")
                return None, None
        except requests.exceptions.JSONDecodeError:
            print("Erro: A resposta da API não está no formato JSON válido.")
            return None, None
    else:
        print("❌ Erro ao autenticar. Código:", response.status_code)
        return None, None

def main():
    """Solicita credenciais do usuário e tenta autenticar no SUAP."""
    username = input("Digite seu usuário: ")
    password = getpass.getpass("Digite sua senha: ")

    access_token, refresh_token = login_suap(username, password)

    if access_token:
        print("✅ Login bem-sucedido!")
        print("🔑 Access Token:", access_token)
        print("🔄 Refresh Token:", refresh_token)
    else:
        print("❌ Falha no login. Verifique suas credenciais.")

if __name__ == "__main__":
    main()
