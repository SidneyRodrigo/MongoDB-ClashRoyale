from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

app = Flask(__name__)

# Conexão com o MongoDB (a senha é fornecida uma vez)
senha = "sua_senha_aqui"
uri = f"mongodb+srv://ioshuan:{senha}@cluster0.azdlm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Conexão com o banco de dados
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['clash_royale']
batalhas_collection = db['batalhas']

# Função para listar decks com mais de X% de vitórias
def listar_decks_com_vitorias(min_porcentagem, min_vitorias, start_time, end_time):
    # Converte os tempos para strings no formato esperado
    start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S+00:00')
    end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S+00:00')

    # Pipeline para o MongoDB
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

# Rota para listar decks com mais de X% de vitórias
@app.route('/decks', methods=['GET'])
def decks():
    try:
        # Obtém os parâmetros da requisição
        min_porcentagem = float(request.args.get('min_porcentagem', 80.0))
        min_vitorias = int(request.args.get('min_vitorias', 500))
        start_time_str = request.args.get('start_time')
        end_time_str = request.args.get('end_time')

        # Converte strings para objetos datetime
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d")
        end_time = datetime.strptime(end_time_str, "%Y-%m-%d")

        # Lista os decks com a porcentagem mínima de vitórias
        decks = listar_decks_com_vitorias(min_porcentagem, min_vitorias, start_time, end_time)

        return jsonify(decks)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
