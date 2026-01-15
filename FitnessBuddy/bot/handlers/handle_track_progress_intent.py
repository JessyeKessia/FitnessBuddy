from FitnessBuddy.bot.polly.send_workout import send_workout_to_tts_api
from FitnessBuddy.bot.utils.get_workout_count import get_workout_count

def handle_track_progress_intent(event, track_progress_validation_result):
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