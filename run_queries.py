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

# conversão de data
def str_to_datetime(date_str):
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")

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
start_time = str_to_datetime("2020-01-01T00:00:00+00:00")
end_time = str_to_datetime("2022-12-31T23:59:59+00:00")

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
    # Certificar-se de que os parâmetros de tempo sejam do tipo datetime
    start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    
    vitorias_condicionais = batalhas_collection.count_documents({
        # Filtro de tempo de batalha
        "battle_time": {"$gte": start_time, "$lte": end_time},
        # Carta do vencedor no deck
        "winner.deck": carta_id,
        # Expressão para comparar troféus e coroas
        "$expr": {
            "$and": [
                {"$lt": ["$winner.starting_trophies", {"$multiply": ["$loser.starting_trophies", (1 - trofeus_percentual / 100)]}]},
                # Verifica se a duração da batalha é menor que 2 minutos
                {"$lt": [{"$dateDiff": {
                    "startDate": "$battle_time",
                    "endDate": {"$dateAdd": {"startDate": "$battle_time", "unit": "second", "amount": 120}},
                    "unit": "second"
                }}, 120]},
                # Vencedor com pelo menos 2 coroas
                {"$gte": ["$winner.crowns", 2]}
            ]
        }
    })
    
    return vitorias_condicionais

# Exemplo de parâmetros
carta_id = 26000023  # ID de carta fictício para teste
trofeus_percentual = 20 # 1% menos troféus
start_time = "2021-01-01 00:00:00"
end_time = "2021-12-31 23:59:59"

# Executar a consulta e exibir o resultado
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
