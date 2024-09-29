from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd

senha = input("Insira a senha do banco de dados: ")

uri = f"mongodb+srv://ioshuan:{senha}@cluster0.azdlm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

try:
    # Carregar o CSV (ajuste o caminho do arquivo conforme necessário)
    df = pd.read_csv('BattlesStaging_n_WL_tagged.csv')
    print("Arquivo .csv carregado com sucesso!")
except Exception as e:
    print(e)

# Selecionar colunas de interesse
df = df[['battleTime', 'winner.tag', 'winner.startingTrophies', 'winner.trophyChange', 'winner.crowns', 
         'winner.card1.id', 'winner.card2.id', 'winner.card3.id', 'winner.card4.id', 'winner.card5.id', 
         'winner.card6.id', 'winner.card7.id', 'winner.card8.id', 
         'loser.tag', 'loser.startingTrophies', 'loser.trophyChange', 'loser.crowns', 
         'loser.card1.id', 'loser.card2.id', 'loser.card3.id', 'loser.card4.id', 'loser.card5.id', 
         'loser.card6.id', 'loser.card7.id', 'loser.card8.id', 'arena.id']]

# Função para criar uma lista de cartas a partir das colunas
def criar_deck(row, tipo_jogador):
    return [row[f'{tipo_jogador}.card{i}.id'] for i in range(1, 9)]

# Função para organizar cada linha em um formato de batalha
def organizar_batalha(row):
    return {
        "battle_time": row['battleTime'],
        "winner": {
            "nickname": row['winner.tag'],
            "starting_trophies": row['winner.startingTrophies'],
            "trophy_change": row['winner.trophyChange'],
            "crowns": row['winner.crowns'],
            "deck": criar_deck(row, 'winner')
        },
        "loser": {
            "nickname": row['loser.tag'],
            "starting_trophies": row['loser.startingTrophies'],
            "trophy_change": row['loser.trophyChange'],
            "crowns": row['loser.crowns'],
            "deck": criar_deck(row, 'loser')
        },
        "arena": row['arena.id']
    }

# Aplicar a função para organizar os dados
batalhas = df.apply(organizar_batalha, axis=1)

db = client['clash_royale']
batalhas_collection = db['batalhas']

# Inserir todas as batalhas
batalhas_collection.insert_many(batalhas.tolist())

print("Banco criado e dados inseridos com sucesso!")
