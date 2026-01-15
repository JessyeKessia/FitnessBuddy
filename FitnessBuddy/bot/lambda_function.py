from FitnessBuddy.bot.validations.validate_offer_help import validate_offer_help
from FitnessBuddy.bot.validations.validate_plan_workout import validate_plan_workout
from FitnessBuddy.bot.validations.validate_register_progress import validate_register_progress
from FitnessBuddy.bot.validations.validate_track_progress import validate_track_progress

from FitnessBuddy.bot.handlers.handle_fallback_intent import handle_fallback_intent
from FitnessBuddy.bot.handlers.handle_greetings_intent import handle_greetings_intent
from FitnessBuddy.bot.handlers.handle_offer_help_intent import handle_offer_help_intent
from FitnessBuddy.bot.handlers.handle_plan_workout_intent import handle_plan_workout_intent
from FitnessBuddy.bot.handlers.handle_register_progress_intent import handle_register_progress_intent
from FitnessBuddy.bot.handlers.handle_track_progress_intent import handle_track_progress_intent


import os
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = os.getenv('S3_BUCKET_NAME_ELEMENTOS')
bucket_name = BUCKET_NAME

def lambda_handler(event):
    try:

        # Pegas as intents
        intent = event['sessionState']['intent']['name']
        # Pega dos slots
        slots = event['sessionState']['intent']['slots']
        
        if intent not in ['Greetings', 'PlanWorkout', 'OfferHelp', 'RegisterProgress', 'TrackProgress']: 
            return handle_fallback_intent()
        
        if intent == 'Greetings':
            return handle_greetings_intent(event)
        if intent == 'OfferHelp':
            help_validation_result = validate_offer_help(slots)
            return handle_offer_help_intent(event, help_validation_result)
        if intent == 'PlanWorkout':
            workout_validation_result = validate_plan_workout(slots)
            return handle_plan_workout_intent(event, workout_validation_result)
        if intent == 'RegisterProgress':
            register_validation_result = validate_register_progress(slots)
            return handle_register_progress_intent(event, register_validation_result, bucket_name)
        if intent == 'TrackProgress':
            track_progress_validation_result = validate_track_progress(slots)
            return handle_track_progress_intent(event, track_progress_validation_result)

    except Exception as e:
        # Imprimir qualquer exceção para depuração
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': 'Internal Server Error'
        }