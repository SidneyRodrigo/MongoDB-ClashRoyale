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

# Consulta 5
def listar_combos_com_vitorias(tamanho_combo, min_porcentagem, start_time, end_time):
    pipeline = [
        {"$match": {"battle_time": {"$gte": start_time, "$lte": end_time}}},
        {"$project": {"combo": {"$slice": ["$winner.deck", tamanho_combo]}, "vitorias": 1}},
        {"$group": {"_id": "$combo", "total_vitorias": {"$sum": 1}}},
        {"$match": {"total_vitorias": {"$gte": 1100}}},
        {"$addFields": {"porcentagem_vitorias": {"$multiply": [{"$divide": ["$total_vitorias", {"$sum": "$total_vitorias"}]}, 100]}}},
        {"$match": {"porcentagem_vitorias": {"$gte": min_porcentagem}}}
    ]
    result = list(batalhas_collection.aggregate(pipeline))
    return result

# parâmetros
tamanho_combo = 3  # tamanho do combo
min_porcentagem = 80.0  # porcentagem mínima de vitórias

start_time = "2021-01-01 00:00:00"
end_time = "2021-12-31 23:59:59"

combos = listar_combos_com_vitorias(tamanho_combo, min_porcentagem, start_time, end_time)

print(f"Combos de cartas com mais de {min_porcentagem}% de vitórias: {combos}")