from FitnessBuddy.bot.utils.create_workout import create_workout

def handle_plan_workout_intent(event, workout_validation_result):
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
        workout_experience = slots['WorkoutExperience']['value']['interpretedValue']
        workout_duration = slots['WorkoutDuration']['value']['interpretedValue']
        
        
        
        response_message = create_workout(workout_type, workout_experience, workout_duration)
    
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