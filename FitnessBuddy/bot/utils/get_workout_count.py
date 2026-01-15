import boto3
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações AWS
BUCKET_NAME = os.getenv('S3_BUCKET_NAME_ELEMENTOS')
AWS_PROF = os.getenv('AWS_PROF')
REGION = os.getenv('REGION')

# Validação das variáveis de ambiente
if not all([BUCKET_NAME, AWS_PROF, REGION]):
    raise ValueError("As variáveis de ambiente S3_BUCKET_NAME_ELEMENTOS, AWS_PROF e REGION devem estar definidas.")

def get_workout_count(workout_period):
    try:
        # Inicializar a sessão boto3
        boto_session = boto3.Session(profile_name=AWS_PROF, region_name=REGION)
        s3 = boto_session.client('s3')
        
        # Definir o intervalo de datas com base no período escolhido
        today = datetime.now().date()
        
        if workout_period == "semana atual":
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
        elif workout_period == "semana passada":
            start_date = today - timedelta(days=today.weekday() + 7)
            end_date = start_date + timedelta(days=6)
        elif workout_period == "mes atual":
            start_date = today.replace(day=1)
            end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        else:  # mês passado
            start_date = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
            end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        
        # Verificar arquivos no intervalo de datas no bucket S3
        objects = s3.list_objects_v2(Bucket=BUCKET_NAME)
        count = 0
        
        if 'Contents' in objects:
            for obj in objects['Contents']:
                key = obj['Key']
                
                # Verifique se a chave contém uma data válida
                try:
                    date_str = key.split('_')[0]
                    workout_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    print(f"A chave '{key}' não contém uma data válida no formato esperado.")
                    continue
                
                if start_date <= workout_date <= end_date:
                    count += 1
        
        return count
    
    except boto3.exceptions.Boto3Error as e:
        print(f"Erro ao acessar o bucket S3: {str(e)}")
        return 0
