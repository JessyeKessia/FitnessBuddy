def handle_greetings_intent(event):
    response_message = "Olá! Eu sou o Fitness Buddy, seu amigo de treino. Como posso te ajudar hoje?"
    response_card_title = "Fitness Buddy"
    response_card_sub_title = "Escolha uma das opções abaixo:"
    response_card_image_url = "https://images2.imgbox.com/aa/dc/6yttlQNY_o.png"
    response_card_buttons = [
        {"text": "Treino", "value": "treino"},
        {"text": "Registrar Progresso", "value": "registrar progresso"},
        {"text": "Consultar Progresso", "value": "consultar progresso"},
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

    return response