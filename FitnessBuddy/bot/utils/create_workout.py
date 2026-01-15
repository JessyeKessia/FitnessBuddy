from FitnessBuddy.bot.polly.send_workout import send_workout_to_tts_api

def create_workout(workoutType, workoutExperience, workoutDuration):
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
    return workout_text + "\n" + "URL para download do audio: " + "\n" + send_workout_to_tts_api(workout_text) 