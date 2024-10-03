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

start_time_str = datetime(2021, 1, 1)
end_time_str = datetime(2021, 12, 31)

# Converta start_time_str e end_time_str para o formato correto
start_time_str_str = start_time_str.strftime("%Y-%m-%d %H:%M:%S%z")
end_time_str_str = end_time_str.strftime("%Y-%m-%d %H:%M:%S%z")

def comparar_taxa_vitoria_cartas(carta1_id, carta2_id, start_time_str, end_time_str):
    # Contar as batalhas em que a carta 1 estava no deck vencedor
    vitorias_carta1 = batalhas_collection.count_documents({
        "battle_time": {"$gte": start_time_str, "$lte": end_time_str},
        "winner.deck": carta1_id
    })

    # Contar as batalhas em que a carta 2 estava no deck vencedor
    vitorias_carta2 = batalhas_collection.count_documents({
        "battle_time": {"$gte": start_time_str, "$lte": end_time_str},
        "winner.deck": carta2_id
    })

    # Total de batalhas no período
    total_batalhas = batalhas_collection.count_documents({
        "battle_time": {"$gte": start_time_str, "$lte": end_time_str}
    })

    # Calcular as taxas de vitória de cada carta
    taxa_vitoria_carta1 = (vitorias_carta1 / total_batalhas) * 100 if total_batalhas > 0 else 0
    taxa_vitoria_carta2 = (vitorias_carta2 / total_batalhas) * 100 if total_batalhas > 0 else 0

    return {
        "carta1": {"id": carta1_id, "vitorias": vitorias_carta1, "taxa_vitoria": taxa_vitoria_carta1},
        "carta2": {"id": carta2_id, "vitorias": vitorias_carta2, "taxa_vitoria": taxa_vitoria_carta2}
    }
