from FitnessBuddy.bot.utils.give_help import give_help

def handle_offer_help_intent(event, help_validation_result):
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
        help_type = slots['WorkoutHelp']['value']['interpretedValue']

        response_message = give_help(help_type)
    
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