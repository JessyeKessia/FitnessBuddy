def validate_offer_help(slots):
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