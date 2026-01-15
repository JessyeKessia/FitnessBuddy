from urllib3.exceptions import HTTPError
import urllib3
import json

def send_workout_to_tts_api(text):
    url = "https://vgc4joemri.execute-api.us-east-1.amazonaws.com/v1/tts"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "phrase": text
    }

    http = urllib3.PoolManager()

    try:
        # Convertendo o dicionário para uma string JSON
        json_data = json.dumps(data)

        # Enviando a requisição POST
        response = http.request(
            'POST',
            url,
            body=json_data,
            headers=headers
        )

        # Verificando se a resposta foi bem-sucedida
        if response.status == 200:
            # Pega o JSON da resposta
            response_json = json.loads(response.data.decode('utf-8'))
            print("Requisição enviada com sucesso.")
            print("Resposta JSON:", response_json)
            return response_json.get('url_to_audio')
        else:
            print(f"Erro ao enviar a requisição: Status code {response.status}")
            return None
    except HTTPError as e:
        print(f"Erro ao enviar a requisição: {e}")
        return None