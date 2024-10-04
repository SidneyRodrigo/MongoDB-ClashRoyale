from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

# Solicita a senha para conexão
senha = input("Insira a senha do banco de dados: ")
uri = f"mongodb+srv://ioshuan:{senha}@cluster0.azdlm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Conexão com o MongoDB
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['clash_royale']
batalhas_collection = db['batalhas']

# Função para calcular derrotas por combo de cartas
def calcular_derrotas_por_combo(combo_cartas, start_time, end_time):
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S%z")
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S%z")

    # Filtra batalhas no intervalo de tempo e onde o perdedor utilizou todas as cartas do combo
    derrotas_com_combo = batalhas_collection.count_documents({
        "battle_time": {"$gte": start_time_str, "$lte": end_time_str},
        "loser.deck": {"$all": combo_cartas}
    })

    return derrotas_com_combo

# Exemplo de uso
if __name__ == "__main__":
    try:
        # Parâmetros de entrada
        combo_cartas_str = input("Digite o combo de cartas separadas por vírgula: ")
        combo_cartas = list(map(int, combo_cartas_str.split(',')))

        start_time_str = input("Digite o timestamp inicial (formato YYYY-MM-DD HH:MM:SS): ")
        end_time_str = input("Digite o timestamp final (formato YYYY-MM-DD HH:MM:SS): ")

        # Converte strings para objetos datetime
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

        # Calcula a quantidade de derrotas
        derrotas = calcular_derrotas_por_combo(combo_cartas, start_time, end_time)

        # Exibe o resultado
        print(f"Quantidade de derrotas para o combo {combo_cartas}: {derrotas}")

    except Exception as e:
        print(f"Erro: {str(e)}")
