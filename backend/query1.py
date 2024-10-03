from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

app = Flask(__name__)

# Conexão com o MongoDB (a senha será fornecida uma vez)
senha = "sua_senha_aqui"
uri = f"mongodb+srv://ioshuan:{senha}@cluster0.azdlm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# conexão com o MongoDB
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['clash_royale']
batalhas_collection = db['batalhas']

# Função para calcular vitórias por carta
def calcular_vitorias_por_carta(carta_id, start_time, end_time):
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

# Rota para calcular vitórias por carta
@app.route('/vitorias', methods=['GET'])
def vitorias():
    try:
        # Parâmetros da requisição
        carta_id = int(request.args.get('carta_id'))
        start_time_str = request.args.get('start_time')
        end_time_str = request.args.get('end_time')

        # Converte strings para datetime
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d")
        end_time = datetime.strptime(end_time_str, "%Y-%m-%d")

        # Calcula a porcentagem de vitórias
        porcentagem = calcular_vitorias_por_carta(carta_id, start_time, end_time)

        return jsonify({
            'carta_id': carta_id,
            'porcentagem_vitorias': porcentagem
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
