def validate_track_progress(slots):
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