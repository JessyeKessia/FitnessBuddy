from datetime import datetime
import os
import json
import logging
import hashlib
import boto3
from botocore.exceptions import ClientError
from contextlib import closing

def v1_tts(event, context):
    try: 
        # Verificação da existência do 'body' no evento
        if 'body' not in event:
            logging.error("Validation Failed: 'body' not in event")
            raise KeyError("Couldn't create the audio. 'body' key is missing in the event.")
        
        # Pega a frase do body
        body = json.loads(event['body'])

        # pegando a frase
        phrase = body['phrase']
        
        # Pega o hash único da frase
        unique_id = hashlib.md5(phrase.encode()).hexdigest()
        
        # Conectando ao dynamodb
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

        # Obtendo a tabela
        table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

        # Obtem o bucket
        bucket_name = os.environ['S3_BUCKET_NAME']
        
        # Obtem a data
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # Verifica se o item já existe
        response_dynamo = table.get_item(
            Key={'id': unique_id}
        )
        # Caso esteja
        if 'Item' in response_dynamo:
            item = response_dynamo['Item']
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'received_phrase': phrase,
                    'url_to_audio': item['audio_url'],
                    'created_audio': item['created_at'],
                    'unique_id': unique_id
                })
            }

        # Criando o audio com a polly
        # Abre uma sessão com o Polly
        polly_client = boto3.client("polly", region_name="us-east-1")
        # Cria o texto pegando os elementos e definindo
        polly_response = polly_client.synthesize_speech (
            Text=phrase,
            OutputFormat='mp3',
            VoiceId='Vitoria' 
        )

        # Salva temporariamente no polly e cria o path
        if "AudioStream" in polly_response:
            with closing(polly_response["AudioStream"]) as stream:
                output = os.path.join("/tmp/", unique_id)
                with open(output, "ab") as file:
                    file.write(stream.read())

        # Upload do áudio para o S3
        s3_client = boto3.client('s3')
        s3_client.upload_file(output, bucket_name, f"{unique_id}.mp3")
        s3_client.put_object_acl(ACL='public-read', Bucket=bucket_name, Key=f"{unique_id}.mp3")

        # Define a url
        audio_url = f"https://{bucket_name}.s3.amazonaws.com/{unique_id}.mp3"

        # Usa o método put_item para colocar o item na tabela no dynamonbd
        table.put_item(
            Item={
                'id': unique_id,
                'audio_url': audio_url,
                'created_at': now
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps({
                'received_phrase': phrase,
                'url_to_audio': audio_url,
                'created_audio': now,
                'unique_id': unique_id
            })
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    