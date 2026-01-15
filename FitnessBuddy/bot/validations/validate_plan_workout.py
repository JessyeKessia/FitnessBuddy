def validate_plan_workout(slots):
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