from FitnessBuddy.bot.polly.send_workout import send_workout_to_tts_api
import random

def give_help(help_type):
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