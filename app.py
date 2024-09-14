from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS
from bson.objectid import ObjectId

app = Flask(__name__)

CORS(app)

# Conexão com o MongoDB
client = MongoClient('mongodb+srv://leonardopacielloescritorio:S3m5%23nhaSum0@bancodebarrasmg.5xocv.mongodb.net/')
db = client['micro_saas']
collection = db['texts']

# Rota para buscar os textos
@app.route('/texts', methods=['GET'])
def get_texts():
    texts = list(collection.find({}, {'_id': 0, 'text': 1}))
    return jsonify(texts), 200

# Rota para adicionar um novo texto
@app.route('/texts', methods=['POST'])
def add_text():
    data = request.get_json()
    text = data.get('text')

    # Verifica se o texto já existe no banco
    if collection.find_one({'text': text}):
        return jsonify({'message': 'Texto já existente'}), 400

    # Insere o novo texto no banco
    collection.insert_one({'text': text})
    return jsonify({'message': 'Texto adicionado com sucesso!'}), 201

if __name__ == '__main__':
    app.run(debug=True)
