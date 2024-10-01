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

# start_time = datetime(2021, 1, 1)
# end_time = datetime(2021, 12, 31)
# min_porcentagem = 80.0

# result = list(batalhas_collection.find({"battle_time": {"$gte": start_time, "$lte": end_time}}))
# print(result)


### Consulta 2: Listar decks completos com mais de X% de vitórias
def listar_decks_com_vitorias(min_porcentagem, start_time, end_time):
    # Converte os tempos para strings no mesmo formato
    start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S+00:00')
    end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S+00:00')

    pipeline = [
        {"$match": {"battle_time": {"$gte": start_time_str, "$lte": end_time_str}}},
        {"$group": {"_id": "$winner.deck", "total_vitorias": {"$sum": 1}}},
        {"$match": {"total_vitorias": {"$gte": min_vitorias}}},
        {"$project": {"_id": 1, "total_vitorias": 1}},
        {"$addFields": {"porcentagem_vitorias": {"$multiply": [{"$divide": ["$total_vitorias", {"$sum": "$total_vitorias"}]}, 100]}}},
        {"$match": {"porcentagem_vitorias": {"$gte": min_porcentagem}}}
    ]
    
    result = list(batalhas_collection.aggregate(pipeline))
    return result

# Exemplo de uso
min_vitorias = 100
start_time = datetime(2021, 1, 1)
end_time = datetime(2021, 12, 31)
min_porcentagem = 100.0

decks = listar_decks_com_vitorias(min_porcentagem, start_time, end_time)
print(f"Decks com mais de {min_porcentagem}% de vitórias: {decks}")
