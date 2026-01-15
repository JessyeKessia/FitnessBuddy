def validate_register_progress(slots):
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