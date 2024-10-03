from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

app = Flask(__name__)

# Conexão com o MongoDB (senha já fornecida)
senha = "sua_senha_aqui"
uri = f"mongodb+srv://ioshuan:{senha}@cluster0.azdlm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Conexão com o banco de dados
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['clash_royale']
batalhas_collection = db['batalhas']

# Função para listar combos com vitórias
def listar_combos_com_vitorias(tamanho_combo, min_porcentagem, start_time, end_time):
    # Pipeline no MongoDB
    pipeline = [
        {"$match": {"battle_time": {"$gte": start_time, "$lte": end_time}}},
        {"$project": {"combo": {"$slice": ["$winner.deck", tamanho_combo]}, "vitorias": 1}},
        {"$group": {"_id": "$combo", "total_vitorias": {"$sum": 1}}},
        {"$match": {"total_vitorias": {"$gte": 1100}}},  # Ajuste o limite de vitórias conforme necessário
        {"$addFields": {"porcentagem_vitorias": {"$multiply": [{"$divide": ["$total_vitorias", {"$sum": "$total_vitorias"}]}, 100]}}},
        {"$match": {"porcentagem_vitorias": {"$gte": min_porcentagem}}}
    ]
    
    result = list(batalhas_collection.aggregate(pipeline))
    return result

# Rota para listar combos com vitórias
@app.route('/combos', methods=['GET'])
def combos():
    try:
        # Obtém os parâmetros da requisição
        tamanho_combo = int(request.args.get('tamanho_combo', 3))
        min_porcentagem = float(request.args.get('min_porcentagem', 80.0))
        start_time_str = request.args.get('start_time')
        end_time_str = request.args.get('end_time')

        # Converte strings para objetos datetime
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

        # Lista os combos de cartas
        combos = listar_combos_com_vitorias(tamanho_combo, min_porcentagem, start_time, end_time)

        return jsonify(combos)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
