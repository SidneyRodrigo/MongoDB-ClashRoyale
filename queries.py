from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

# Conectar ao MongoDB
senha = input("Insira a senha do banco de dados: ")
uri = f"mongodb+srv://ioshuan:{senha}@cluster0.azdlm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['clash_royale']
batalhas_collection = db['batalhas']

# Função para converter string em data (caso necessário)
def str_to_datetime(date_str):
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")

### Consulta 1: Calcular a porcentagem de vitórias usando uma carta X em um intervalo de tempo
def calcular_vitorias_por_carta(carta_id, start_time, end_time):
    total_batalhas = batalhas_collection.count_documents({
        "battle_time": {"$gte": start_time, "$lte": end_time}
    })
    vitorias_com_carta = batalhas_collection.count_documents({
        "battle_time": {"$gte": start_time, "$lte": end_time},
        "winner.deck": carta_id
    })
    if total_batalhas > 0:
        porcentagem = (vitorias_com_carta / total_batalhas) * 100
    else:
        porcentagem = 0
    return porcentagem

# Exemplo de parâmetros
carta_id = 26000000  # ID da carta
start_time = str_to_datetime("2021-01-01T00:00:00+00:00")
end_time = str_to_datetime("2021-12-31T23:59:59+00:00")

print(f"Porcentagem de vitórias com a carta {carta_id}: {calcular_vitorias_por_carta(carta_id, start_time, end_time)}%")


### Consulta 2: Listar decks completos com mais de X% de vitórias
def listar_decks_com_vitorias(min_porcentagem, start_time, end_time):
    pipeline = [
        {"$match": {"battle_time": {"$gte": start_time, "$lte": end_time}}},
        {"$group": {"_id": "$winner.deck", "total_vitorias": {"$sum": 1}}},
        {"$project": {"_id": 1, "total_vitorias": 1}},
        {"$addFields": {"porcentagem_vitorias": {"$multiply": [{"$divide": ["$total_vitorias", {"$sum": "$total_vitorias"}]}, 100]}}},
        {"$match": {"porcentagem_vitorias": {"$gte": min_porcentagem}}}
    ]
    result = list(batalhas_collection.aggregate(pipeline))
    return result

# Exemplo de parâmetros
min_porcentagem = 50.0
decks = listar_decks_com_vitorias(min_porcentagem, start_time, end_time)
print(f"Decks com mais de {min_porcentagem}% de vitórias: {decks}")


### Consulta 3: Calcular derrotas com combo de cartas (X1, X2, ...) em um intervalo de tempo
def calcular_derrotas_com_combo(combo_cartas, start_time, end_time):
    derrotas_com_combo = batalhas_collection.count_documents({
        "battle_time": {"$gte": start_time, "$lte": end_time},
        "loser.deck": {"$all": combo_cartas}
    })
    return derrotas_com_combo

# Exemplo de parâmetros
combo_cartas = [26000000, 26000010]  # IDs do combo de cartas
print(f"Quantidade de derrotas com o combo de cartas {combo_cartas}: {calcular_derrotas_com_combo(combo_cartas, start_time, end_time)}")


### Consulta 4: Vitórias com Z% menos troféus, menos de 2 minutos de duração, e 2 torres derrubadas
def calcular_vitorias_com_condicoes(carta_id, trofeus_percentual, start_time, end_time):
    vitorias_condicionais = batalhas_collection.count_documents({
        "battle_time": {"$gte": start_time, "$lte": end_time},
        "winner.deck": carta_id,
        "$expr": {
            "$and": [
                {"$lt": ["$winner.starting_trophies", {"$multiply": ["$loser.starting_trophies", (1 - trofeus_percentual / 100)]}]},
                {"$lt": [{"$subtract": ["$battle_time", "$battle_time"]}, 120]},  # Duração da batalha < 120 segundos
                {"$gte": ["$loser.crowns", 2]}
            ]
        }
    })
    return vitorias_condicionais

# Exemplo de parâmetros
trofeus_percentual = 20  # Z% menos troféus
print(f"Vitórias com {trofeus_percentual}% menos troféus, duração < 2 minutos, e 2 torres derrubadas: {calcular_vitorias_com_condicoes(carta_id, trofeus_percentual, start_time, end_time)}")


### Consulta 5: Listar combos de cartas de tamanho N com mais de Y% de vitórias
def listar_combos_com_vitorias(tamanho_combo, min_porcentagem, start_time, end_time):
    pipeline = [
        {"$match": {"battle_time": {"$gte": start_time, "$lte": end_time}}},
        {"$project": {"combo": {"$slice": ["$winner.deck", tamanho_combo]}, "vitorias": 1}},
        {"$group": {"_id": "$combo", "total_vitorias": {"$sum": 1}}},
        {"$addFields": {"porcentagem_vitorias": {"$multiply": [{"$divide": ["$total_vitorias", {"$sum": "$total_vitorias"}]}, 100]}}},
        {"$match": {"porcentagem_vitorias": {"$gte": min_porcentagem}}}
    ]
    result = list(batalhas_collection.aggregate(pipeline))
    return result

# Exemplo de parâmetros
tamanho_combo = 3  # Tamanho do combo
min_porcentagem = 60.0  # Porcentagem mínima de vitórias
combos = listar_combos_com_vitorias(tamanho_combo, min_porcentagem, start_time, end_time)
print(f"Combos de cartas com mais de {min_porcentagem}% de vitórias: {combos}")
