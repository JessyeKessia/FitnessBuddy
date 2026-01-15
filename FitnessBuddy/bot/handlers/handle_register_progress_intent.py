from FitnessBuddy.bot.polly.send_workout import send_workout_to_tts_api
import boto3
import os
from dotenv import load_dotenv

def handle_register_progress_intent(event, register_validation_result, bucket_name):
    intent = event['sessionState']['intent']['name']
    slots = event['sessionState']['intent']['slots']

    if event['invocationSource'] == 'DialogCodeHook':
        
        if not register_validation_result['isValid']:
            
            response_message = register_validation_result['message']
            response_audio_message = ""
            response_card_sub_title = ''
            response_card_buttons = []
            
            if register_validation_result['invalidSlot'] == "WorkoutType":
                response_card_sub_title = "Por favor, selecione um tipo de treino"
                response_card_buttons = [
                    {"text": "Cardio", "value": "cardio"},
                    {"text": "Força", "value": "força"},
                    {"text": "Flexibilidade", "value": "flexibilidade"}
                ]

            if register_validation_result['invalidSlot'] == "WorkoutDuration":
                response_card_sub_title = "Por favor, selecione uma duração para o treino"
                response_card_buttons = [
                    {"text": "30 minutos", "value": "30 minutos"},
                    {"text": "1 hora", "value": "1 hora"},
                    {"text": "2 horas", "value": "2 horas"}
                ]

            if register_validation_result['invalidSlot'] == "WorkoutDate":
                response_card_sub_title = "Por favor, informe o dia que você fez o treino"
                response_card_buttons = [
                    {"text": "Hoje", "value": "hoje"},
                    {"text": "Ontem", "value": "ontem"}
                ]

            response = {
                "sessionState": {
                    "dialogAction": {
                        "slotToElicit": register_validation_result['invalidSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        "name": intent,
                        "slots": slots,
                    }
                },
                "messages": [
                    {
                        "contentType": "ImageResponseCard",
                        "content": response_message,
                        "imageResponseCard": {
                            "title": "Fitness Buddy",
                            "subtitle": response_card_sub_title,
                            "imageUrl": "https://images2.imgbox.com/aa/dc/6yttlQNY_o.png",
                            "buttons": response_card_buttons,
                            
                        }
                    }
                ]
            }
        else:
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                }
            }

    if event['invocationSource'] == 'FulfillmentCodeHook':
        workout_type = slots['WorkoutType']['value']['interpretedValue']
        workout_duration = slots['WorkoutDuration']['value']['interpretedValue']
        workout_date = slots['WorkoutDate']['value']['interpretedValue']

        BUCKET_NAME = os.getenv('S3_BUCKET_NAME_ELEMENTOS')
        AWS_PROF = os.getenv('AWS_PROF')
        REGION = os.getenv('REGION')

        bucket_name = BUCKET_NAME
        profile_name = AWS_PROF
        region = REGION
        # Salvando progresso no S3
        boto_session = boto3.Session(profile_name=profile_name, region_name=region)
        s3 = boto_session.client('s3')
        object_key = f'{workout_date}_{workout_type}.txt'
        object_content = f'Tipo de treino: {workout_type}\nDuração: {workout_duration}\nData: {workout_date}'
        
        s3.put_object(Body=object_content, Bucket=bucket_name, Key=object_key)
        
        response_message = "Progresso registrado com sucesso!" 
        response_message = response_message + "\n"+ "Audio:" + send_workout_to_tts_api(response_message)
    
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent,
                    "slots": slots,
                    "state": "Fulfilled"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": response_message
                }
            ]
        }
    return response        