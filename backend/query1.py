# imports
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

# dados para conexão
senha = input("Insira a senha do banco de dados: ")
uri = f"mongodb+srv://ioshuan:{senha}@cluster0.azdlm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# conexão em sí
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['clash_royale']
batalhas_collection = db['batalhas']

# Ajuste na função para calcular vitórias
def calcular_vitorias_por_carta(carta_id, start_time, end_time):
    # Converta start_time e end_time para o formato correto
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S%z")
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S%z")

    total_batalhas = batalhas_collection.count_documents({
        "battle_time": {"$gte": start_time_str, "$lte": end_time_str}
    })
    vitorias_com_carta = batalhas_collection.count_documents({
        "battle_time": {"$gte": start_time_str, "$lte": end_time_str},
        "winner.deck": carta_id
    })

    if total_batalhas > 0:
        porcentagem = (vitorias_com_carta / total_batalhas) * 100
    else:
        porcentagem = 0

    return porcentagem

# parâmetros
carta_id = 26000003  # ID da carta

start_time = datetime(2020, 1, 1)
end_time = datetime(2022, 12, 31)

print(f"Porcentagem de vitórias com a carta {carta_id}: {calcular_vitorias_por_carta(carta_id, start_time, end_time)}%")