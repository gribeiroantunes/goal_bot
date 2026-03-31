import requests

API_KEY = "bee849666197a131bdd4b4b1ced8f51374b78fcd"
BASE_URL = "https://sports.bzzoiro.com/api"

# Endpoint de eventos (próximos jogos)
url = f"{BASE_URL}/events/"
headers = {"Authorization": f"Token {API_KEY}"}

response = requests.get(url, headers=headers)

# Mostra o status da requisição
print("Status code:", response.status_code)

# Mostra os dados recebidos
try:
    data = response.json()
    print(data)
except Exception as e:
    print("Erro ao ler JSON:", e)