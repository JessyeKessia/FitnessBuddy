from flask import Flask, request
from flask_cors import CORS

from FitnessBuddy.bot.lambda_function import lambda_handler


app = Flask(__name__)
CORS(app) 

@app.route('/data', methods=['POST'])
def data():
    data = request.get_json()  # Obtém o JSON enviado no corpo da requisição
    response = lambda_handler(data)
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
