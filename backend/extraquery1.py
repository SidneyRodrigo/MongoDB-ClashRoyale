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

start_time = datetime(2021, 1, 1)
end_time = datetime(2021, 12, 31)

# Converta start_time e end_time para o formato correto
start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S%z")
end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S%z")

def listar_cartas_mais_usadas_em_vitorias(start_time_str, end_time_str, limite=10):
    pipeline = [
        {"$match": {"battle_time": {"$gte": start_time_str, "$lte": end_time_str}}},
        {"$unwind": "$winner.deck"},
        {"$group": {"_id": "$winner.deck", "frequencia": {"$sum": 1}}},
        {"$sort": {"frequencia": -1}},
        {"$limit": limite}
    ]
    
    result = list(batalhas_collection.aggregate(pipeline))
    return result

# Exemplo de parâmetros
limite = 10  # Exibir as 10 cartas mais usadas
cartas_mais_usadas = listar_cartas_mais_usadas_em_vitorias(start_time_str, end_time_str, limite)
print(f"Cartas mais usadas em vitórias: {cartas_mais_usadas}")