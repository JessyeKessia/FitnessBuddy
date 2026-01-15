import json
import random
import boto3
import urllib3
from urllib3.exceptions import HTTPError
from datetime import datetime, timedelta
bucket_name = 'your-bucket-name'

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

def validate_planWorkout(slots):
    workout_types = ['cardio', 'força', 'flexibilidade']
    experience_levels = ['iniciante', 'intermediário', 'avançado']
    workout_durations = ['30 minutos', '1 hora', '2 horas']

    # Validando WorkoutType
    if not slots['WorkoutType']:
        print('Validating WorkoutType Slot')
        return {
            'isValid': False,
            'invalidSlot': 'WorkoutType',
            'message': 'Qual tipo de treino você prefere (Cardio, Força ou Flexibilidade)?'
        }
    
    if slots['WorkoutType']['value']['originalValue'].lower() not in workout_types:
        print('Invalid WorkoutType')
        return {
            'isValid': False,
            'invalidSlot': 'WorkoutType',
            'message': 'Por favor, selecione um tipo de treino: {}.'.format(", ".join(workout_types))
        }
    
    # Validando WorkoutExperience
    if not slots['WorkoutExperience']:
        print('Validating WorkoutExperience Slot')
        return {
            'isValid': False,
            'invalidSlot': 'WorkoutExperience',
            'message': 'Qual seu nível de experiência? (Iniciante, Intermediário ou Avançado)'
        }

    if slots['WorkoutExperience']['value']['originalValue'].lower() not in experience_levels:
        print('Invalid WorkoutExperience')
        return {
            'isValid': False,
            'invalidSlot': 'WorkoutExperience',
            'message': 'Por favor, selecione um nível de experiência: {}.'.format(", ".join(experience_levels))
        }
    
    # Validando WorkoutDuration
    if not slots['WorkoutDuration']:
        print('Validating WorkoutDuration Slot')
        return {
            'isValid': False,
            'invalidSlot': 'WorkoutDuration',
            'message': 'Qual duração do treino você deseja? (30 minutos, 1 hora ou 2 horas)'
        }

    if slots['WorkoutDuration']['value']['originalValue'].lower() not in workout_durations:
        print('Invalid WorkoutDuration')
        return {
            'isValid': False,
            'invalidSlot': 'WorkoutDuration',
            'message': 'Por favor, selecione uma duração: {}.'.format(", ".join(workout_durations))
        }
    
    # Validar treino
    return {'isValid': True}
    
def validate_offerHelp(slots):
    help_types = ['treino', 'saude']

    # Validando WorkoutType
    if not slots['WorkoutHelp']:
        print('Validating WorkoutHelp Slot')
        return {
            'isValid': False,
            'invalidSlot': 'WorkoutHelp',
            'message': 'Qual tipo de ajuda você necessita (Treino ou Saúde)?'
        }
    
    if slots['WorkoutHelp']['value']['originalValue'].lower() not in help_types:
        print('Invalid WorkoutHelp')
        return {
            'isValid': False,
            'invalidSlot': 'WorkoutHelp',
            'message': 'Por favor, selecione um tipo de ajuda: {}.'.format(", ".join(help_types))
        }
    
    # Validar treino
    return {'isValid': True}
    
def validate_registerProgress(slots):
    workout_types = ['cardio', 'força', 'flexibilidade']
    workout_durations = ['30 minutos', '1 hora', '2 horas']

    # Validando WorkoutType
    if not slots['WorkoutType']:
        return {
            'isValid': False,
            'invalidSlot': 'WorkoutType',
            'message': 'Qual tipo de treino você fez (Cardio, Força ou Flexibilidade)?'
        }
    
    if slots['WorkoutType']['value']['originalValue'].lower() not in workout_types:
        return {
            'isValid': False,
            'invalidSlot': 'WorkoutType',
            'message': 'Por favor, selecione um tipo de treino: {}.'.format(", ".join(workout_types))
        }

    # Validando WorkoutDuration
    if not slots['WorkoutDuration']:
        return {
            'isValid': False,
            'invalidSlot': 'WorkoutDuration',
            'message': 'Qual foi a duração do treino? (30 minutos, 1 hora ou 2 horas)'
        }

    if slots['WorkoutDuration']['value']['originalValue'].lower() not in workout_durations:
        return {
            'isValid': False,
            'invalidSlot': 'WorkoutDuration',
            'message': 'Por favor, selecione uma duração: {}.'.format(", ".join(workout_durations))
        }
    
    # Validando WorkoutDate
    if not slots['WorkoutDate']:
        return {
            'isValid': False,
            'invalidSlot': 'WorkoutDate',
            'message': 'Qual foi a data do treino? (AAAA-MM-DD)'
        }

    # Validar progresso
    return {'isValid': True}

def validate_trackProgress(slots):
    workout_periods = ['semana atual', 'semana passada', 'mes atual', 'mes passado']

    if not slots['WorkoutPeriod']:
        print('Validating WorkoutPeriod Slot')
        return {
            'isValid': False,
            'invalidSlot': 'WorkoutPeriod',
            'message': 'Qual período você deseja consultar? (Semana atual, Semana passada, Mês atual, Mês passado)?'
        }

    if slots['WorkoutPeriod']['value']['originalValue'].lower() not in [period.lower() for period in workout_periods]:
        print('Invalid WorkoutPeriod')
        return {
            'isValid': False,
            'invalidSlot': 'WorkoutPeriod',
            'message': 'Por favor, selecione um período válido: {}.'.format(", ".join(workout_periods))
        }

    return {'isValid': True}
    
def lambda_handler(event, context):
    
    # Pegas as intents
    intent = event['sessionState']['intent']['name']
    # Pega dos slots
    slots = event['sessionState']['intent']['slots']
    
    if intent not in ['Greetings', 'PlanWorkout', 'OfferHelp', 'RegisterProgress', 'TrackProgress']: 
        return handle_fallback_intent()
    
    if intent == 'Greetings':
        return handle_greetings_intent(event)
    if intent == 'OfferHelp':
        help_validation_result = validate_offerHelp(event['sessionState']['intent']['slots'])
        return handle_offerHelp_intent(event, help_validation_result)
    if intent == 'PlanWorkout':
        workout_validation_result = validate_planWorkout(event['sessionState']['intent']['slots'])
        return handle_planWorkout_intent(event, workout_validation_result)
    if intent == 'RegisterProgress':
        register_validation_result = validate_registerProgress(event['sessionState']['intent']['slots'])
        return handle_registerProgress_intent(event, register_validation_result)
    if intent == 'TrackProgress':
        track_progress_validation_result = validate_trackProgress(event['sessionState']['intent']['slots'])
        return handle_trackProgress_intent(event, track_progress_validation_result)
        
def handle_greetings_intent(event):
    response_message = "Olá! Eu sou o Fitness Buddy, seu amigo de treino. Como posso te ajudar hoje?"
    response_card_title = "Fitness Buddy"
    response_card_sub_title = "Escolha uma das opções abaixo:"
    response_card_image_url = "https://cdn.shopify.com/s/files/1/0047/4657/5970/files/The_Top_8_Ways_To_Take_Your_Workout_to_the_Next_Level_480x480.jpg?v=1634815059"
    response_card_buttons = [
        {"text": "Treino", "value": "treino"},
        {"text": "Consultar Progresso", "value": "consultar progresso"},
        {"text": "Registrar Progresso", "value": "registrar progresso"},
        {"text": "Ajuda", "value": "ajuda"}
    ]

    response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled"
            },
            "intent": {
                "name": event['sessionState']['intent']['name'],
                "slots": event['sessionState']['intent']['slots'],
                "state": "Fulfilled"
            }
        },
        "messages": [
            {
                "contentType": "ImageResponseCard",
                "content": response_message,
                "imageResponseCard": {
                    "title": response_card_title,
                    "subtitle": response_card_sub_title,
                    "imageUrl": response_card_image_url,
                    "buttons": response_card_buttons
                }
            }
        ]
    }

    print(response)
    return response

def handle_planWorkout_intent(event, workout_validation_result):
    intent = event['sessionState']['intent']['name']
    slots = event['sessionState']['intent']['slots']

    if event['invocationSource'] == 'DialogCodeHook':
        
        if not workout_validation_result['isValid']:
            
            response_message = workout_validation_result['message']
            response_audio_message = ""
            response_card_sub_title = ''
            response_card_buttons = []
            
            if workout_validation_result['invalidSlot'] == "WorkoutType":
                response_card_sub_title = "Por favor, selecione um tipo de treino"
                response_card_buttons = [
                    {"text": "Cardio", "value": "cardio"},
                    {"text": "Força", "value": "força"},
                    {"text": "Flexibilidade", "value": "flexibilidade"}
                ]

            if workout_validation_result['invalidSlot'] == "WorkoutExperience":
                response_card_sub_title = "Por favor, selecione um nível de experiência"
                response_card_buttons = [
                    {"text": "Iniciante", "value": "iniciante"},
                    {"text": "Intermediário", "value": "intermediário"},
                    {"text": "Avançado", "value": "avançado"}
                ]

            if workout_validation_result['invalidSlot'] == "WorkoutDuration":
                response_card_sub_title = "Por favor, selecione uma duração para o treino"
                response_card_buttons = [
                    {"text": "30 minutos", "value": "30 minutos"},
                    {"text": "1 hora", "value": "1 hora"},
                    {"text": "2 horas", "value": "2 horas"}
                ]

            response = {
                "sessionState": {
                    "dialogAction": {
                        "slotToElicit": workout_validation_result['invalidSlot'],
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
                            "imageUrl": "https://cdn.shopify.com/s/files/1/0047/4657/5970/files/The_Top_8_Ways_To_Take_Your_Workout_to_the_Next_Level_480x480.jpg?v=1634815059",
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
        workout_experience = slots['WorkoutExperience']['value']['interpretedValue']
        workout_duration = slots['WorkoutDuration']['value']['interpretedValue']
        
        
        
        response_message = createWorkout(workout_type, workout_experience, workout_duration)
    
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
        
def createWorkout(workoutType, workoutExperience, workoutDuration):
    workout_text = ""
    if workoutType == 'força':
        if workoutDuration == '30 minutos':
            if workoutExperience == 'iniciante':
                workout_text = "Treino de força para iniciantes em 30 minutos: \n- 3 séries de 10 agachamentos\n- 3 séries de 10 flexões\n- 3 séries de 10 abdominais"
            elif workoutExperience == 'intermediário':
                workout_text = "Treino de força para intermediários em 30 minutos: \n- 4 séries de 12 agachamentos\n- 4 séries de 12 flexões\n- 4 séries de 12 abdominais"
            elif workoutExperience == 'avançado':
                workout_text = "Treino de força para avançados em 30 minutos: \n- 5 séries de 15 agachamentos\n- 5 séries de 15 flexões\n- 5 séries de 15 abdominais"
        elif workoutDuration == '1 hora':
            if workoutExperience == 'iniciante':
                workout_text = "Treino de força para iniciantes em 1 hora: \n- 4 séries de 12 agachamentos\n- 4 séries de 12 flexões\n- 4 séries de 12 abdominais\n- 4 séries de 10 levantamento terra"
            elif workoutExperience == 'intermediário':
                workout_text = "Treino de força para intermediários em 1 hora: \n- 5 séries de 15 agachamentos\n- 5 séries de 15 flexões\n- 5 séries de 15 abdominais\n- 5 séries de 12 levantamento terra"
            elif workoutExperience == 'avançado':
                workout_text = "Treino de força para avançados em 1 hora: \n- 6 séries de 20 agachamentos\n- 6 séries de 20 flexões\n- 6 séries de 20 abdominais\n- 6 séries de 15 levantamento terra"
        elif workoutDuration == '2 horas':
            if workoutExperience == 'iniciante':
                workout_text = "Treino de força para iniciantes em 2 horas: \n- 5 séries de 15 agachamentos\n- 5 séries de 15 flexões\n- 5 séries de 15 abdominais\n- 5 séries de 12 levantamento terra\n- 5 séries de 10 supino"
            elif workoutExperience == 'intermediário':
                workout_text = "Treino de força para intermediários em 2 horas: \n- 6 séries de 18 agachamentos\n- 6 séries de 18 flexões\n- 6 séries de 18 abdominais\n- 6 séries de 15 levantamento terra\n- 6 séries de 12 supino"
            elif workoutExperience == 'avançado':
                workout_text = "Treino de força para avançados em 2 horas: \n- 7 séries de 20 agachamentos\n- 7 séries de 20 flexões\n- 7 séries de 20 abdominais\n- 7 séries de 18 levantamento terra\n- 7 séries de 15 supino"
    elif workoutType == 'cardio':
        if workoutDuration == '30 minutos':
            if workoutExperience == 'iniciante':
                workout_text = "Treino de cardio para iniciantes em 30 minutos: \n- 5 minutos de aquecimento\n- 10 minutos de corrida leve\n- 5 minutos de caminhada\n- 5 minutos de corrida leve\n- 5 minutos de alongamento"
            elif workoutExperience == 'intermediário':
                workout_text = "Treino de cardio para intermediários em 30 minutos: \n- 5 minutos de aquecimento\n- 15 minutos de corrida moderada\n- 5 minutos de caminhada\n- 5 minutos de alongamento"
            elif workoutExperience == 'avançado':
                workout_text = "Treino de cardio para avançados em 30 minutos: \n- 5 minutos de aquecimento\n- 20 minutos de corrida intensa\n- 5 minutos de alongamento"
        elif workoutDuration == '1 hora':
            if workoutExperience == 'iniciante':
                workout_text = "Treino de cardio para iniciantes em 1 hora: \n- 10 minutos de aquecimento\n- 20 minutos de corrida leve\n- 10 minutos de caminhada\n- 10 minutos de corrida leve\n- 10 minutos de alongamento"
            elif workoutExperience == 'intermediário':
                workout_text = "Treino de cardio para intermediários em 1 hora: \n- 10 minutos de aquecimento\n- 30 minutos de corrida moderada\n- 10 minutos de caminhada\n- 10 minutos de alongamento"
            elif workoutExperience == 'avançado':
                workout_text = "Treino de cardio para avançados em 1 hora: \n- 10 minutos de aquecimento\n- 40 minutos de corrida intensa\n- 10 minutos de alongamento"
        elif workoutDuration == '2 horas':
            if workoutExperience == 'iniciante':
                workout_text = "Treino de cardio para iniciantes em 2 horas: \n- 20 minutos de aquecimento\n- 40 minutos de corrida leve\n- 20 minutos de caminhada\n- 20 minutos de corrida leve\n- 20 minutos de alongamento"
            elif workoutExperience == 'intermediário':
                workout_text = "Treino de cardio para intermediários em 2 horas: \n- 20 minutos de aquecimento\n- 1 hora de corrida moderada\n- 20 minutos de caminhada\n- 20 minutos de alongamento"
            elif workoutExperience == 'avançado':
                workout_text = "Treino de cardio para avançados em 2 horas: \n- 20 minutos de aquecimento\n- 1 hora e 20 minutos de corrida intensa\n- 20 minutos de alongamento"
    elif workoutType == 'flexibilidade':
        if workoutDuration == '30 minutos':
            if workoutExperience == 'iniciante':
                workout_text = "Treino de flexibilidade para iniciantes em 30 minutos: \n- 5 minutos de alongamento de pescoço\n- 5 minutos de alongamento de ombros\n- 5 minutos de alongamento de braços\n- 5 minutos de alongamento de pernas\n- 10 minutos de alongamento de corpo inteiro"
            elif workoutExperience == 'intermediário':
                workout_text = "Treino de flexibilidade para intermediários em 30 minutos: \n- 5 minutos de alongamento de pescoço\n- 5 minutos de alongamento de ombros\n- 5 minutos de alongamento de braços\n- 5 minutos de alongamento de pernas\n- 10 minutos de yoga"
            elif workoutExperience == 'avançado':
                workout_text = "Treino de flexibilidade para avançados em 30 minutos: \n- 5 minutos de alongamento de pescoço\n- 5 minutos de alongamento de ombros\n- 5 minutos de alongamento de braços\n- 5 minutos de alongamento de pernas\n- 10 minutos de yoga avançada"
        elif workoutDuration == '1 hora':
            if workoutExperience == 'iniciante':
                workout_text = "Treino de flexibilidade para iniciantes em 1 hora: \n- 10 minutos de alongamento de pescoço\n- 10 minutos de alongamento de ombros\n- 10 minutos de alongamento de braços\n- 10 minutos de alongamento de pernas\n- 20 minutos de alongamento de corpo inteiro"
            elif workoutExperience == 'intermediário':
                workout_text = "Treino de flexibilidade para intermediários em 1 hora: \n- 10 minutos de alongamento de pescoço\n- 10 minutos de alongamento de ombros\n- 10 minutos de alongamento de braços\n- 10 minutos de alongamento de pernas\n- 20 minutos de yoga"
            elif workoutExperience == 'avançado':
                workout_text = "Treino de flexibilidade para avançados em 1 hora: \n- 10 minutos de alongamento de pescoço\n- 10 minutos de alongamento de ombros\n- 10 minutos de alongamento de braços\n- 10 minutos de alongamento de pernas\n- 20 minutos de yoga avançada"
        elif workoutDuration == '2 horas':
            if workoutExperience == 'iniciante':
                workout_text = "Treino de flexibilidade para iniciantes em 2 horas: \n- 20 minutos de alongamento de pescoço\n- 20 minutos de alongamento de ombros\n- 20 minutos de alongamento de braços\n- 20 minutos de alongamento de pernas\n- 40 minutos de alongamento de corpo inteiro"
            elif workoutExperience == 'intermediário':
                workout_text = "Treino de flexibilidade para intermediários em 2 horas: \n- 20 minutos de alongamento de pescoço\n- 20 minutos de alongamento de ombros\n- 20 minutos de alongamento de braços\n- 20 minutos de alongamento de pernas\n- 40 minutos de yoga"
            elif workoutExperience == 'avançado':
                workout_text = "Treino de flexibilidade para avançados em 2 horas: \n- 20 minutos de alongamento de pescoço\n- 20 minutos de alongamento de ombros\n- 20 minutos de alongamento de braços\n- 20 minutos de alongamento de pernas\n- 40 minutos de yoga avançada"
    
    # Envia o texto do treino para a API TTS e retorna a URL do áudio
    
    return workout_text + "\n" + "URL para download do audio: " + "\n" + send_workout_to_tts_api(workout_text) 
        
def handle_offerHelp_intent(event, help_validation_result):
    intent = event['sessionState']['intent']['name']
    slots = event['sessionState']['intent']['slots']

    if event['invocationSource'] == 'DialogCodeHook':
        
        if not help_validation_result['isValid']:
            
            response_message = help_validation_result['message']
            response_audio_message = ""
            response_card_sub_title = ''
            response_card_buttons = []
            
            if help_validation_result['invalidSlot'] == "WorkoutHelp":
                response_card_sub_title = "Por favor, selecione um tipo de ajuda"
                response_card_buttons = [
                    {"text": "Treino", "value": "treino"},
                    {"text": "Saúde", "value": "saude"}
                ]

            response = {
                "sessionState": {
                    "dialogAction": {
                        "slotToElicit": help_validation_result['invalidSlot'],
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
                            "imageUrl": "https://cdn.shopify.com/s/files/1/0047/4657/5970/files/The_Top_8_Ways_To_Take_Your_Workout_to_the_Next_Level_480x480.jpg?v=1634815059",
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
        help_type = slots['WorkoutHelp']['value']['interpretedValue']

        response_message = giveHelp(help_type)
    
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
        
def giveHelp(help_type):
    treino_dicas = [
        "Lembre-se de aquecer antes de começar o treino.",
        "Mantenha a postura correta para evitar lesões.",
        "Aumente gradualmente o peso para melhorar a força.",
        "Descanse entre as séries para maximizar os ganhos.",
        "Varie os exercícios para trabalhar diferentes grupos musculares."
    ]
    
    saude_dicas = [
        "Beba pelo menos 2 litros de água por dia.",
        "Durma entre 7 a 8 horas por noite.",
        "Inclua frutas e vegetais em sua dieta diária.",
        "Pratique meditação ou exercícios de respiração para reduzir o estresse.",
        "Evite alimentos processados e ricos em açúcares."
    ]
    
    if help_type == "treino":
        return  random.choice(treino_dicas)  + "\n"+ "Audio: " +  send_workout_to_tts_api(random.choice(treino_dicas) )
    else:
        return random.choice(saude_dicas) + "\n" + "Audio: " +  send_workout_to_tts_api(random.choice(treino_dicas) ) 
        
def handle_registerProgress_intent(event, register_validation_result):
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
                            "imageUrl": "https://cdn.shopify.com/s/files/1/0047/4657/5970/files/The_Top_8_Ways_To_Take_Your_Workout_to_the_Next_Level_480x480.jpg?v=1634815059",
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

        # Salvando progresso no S3
        s3 = boto3.client('s3')
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

def handle_trackProgress_intent(event, track_progress_validation_result):
    intent = event['sessionState']['intent']['name']
    slots = event['sessionState']['intent']['slots']

    if event['invocationSource'] == 'DialogCodeHook':
        if not track_progress_validation_result['isValid']:
            response_message = track_progress_validation_result['message']
            response_card_sub_title = ''
            response_card_buttons = []

            if track_progress_validation_result['invalidSlot'] == "WorkoutPeriod":
                response_card_sub_title = "Por favor, selecione um período"
                response_card_buttons = [
                    {"text": "Semana atual", "value": "semana atual"},
                    {"text": "Semana passada", "value": "semana passada"},
                    {"text": "Mês atual", "value": "mes atual"},
                    {"text": "Mês passado", "value": "mes passado"}
                ]

            response = {
                "sessionState": {
                    "dialogAction": {
                        "slotToElicit": track_progress_validation_result['invalidSlot'],
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
                            "imageUrl": "https://example.com/fitness_image.jpg",  # URL de exemplo
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
        workout_period = slots['WorkoutPeriod']['value']['interpretedValue']
        workout_count = get_workout_count(workout_period)
        
        response_message = f"Você registrou {workout_count} treinos durante o período da(o) {workout_period}." 
        response_message = response_message + "\n" +  "Audio: "+  send_workout_to_tts_api(response_message)

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
    
def get_workout_count(workout_period):
    s3 = boto3.client('s3')
    
    # Definir o intervalo de datas com base no período escolhido
    today = datetime.now().date()
    
    if workout_period == "semana atual":
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
    elif workout_period == "semana passada":
        start_date = today - timedelta(days=today.weekday() + 7)
        end_date = start_date + timedelta(days=6)
    elif workout_period == "mes atual":
        start_date = today.replace(day=1)
        end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    else:
        start_date = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    
    # Verificar arquivos no intervalo de datas no bucket S3
    objects = s3.list_objects_v2(Bucket='your-bucket-name')
    count = 0
    if 'Contents' in objects:
        for obj in objects['Contents']:
            key = obj['Key']
            date_str = key.split('_')[0]
            workout_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            if start_date <= workout_date <= end_date:
                count += 1
    
    return count 
    
def handle_fallback_intent():
    response_message = "Desculpe, não consegui entender o que você quis dizer."

    response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled"
            },
            "intent": {
                "name": "FallbackIntent",
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

    print(response)
    return response