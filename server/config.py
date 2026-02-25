import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'joke-evaluator-secret-key')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Model
    MODEL_PATH = os.getenv('MODEL_PATH', 'artifacts/best_model.pth')
    TOKENIZER_PATH = os.getenv('TOKENIZER_PATH', 'artifacts/tokenizer')
    MAX_LENGTH = int(os.getenv('MAX_LENGTH', '128'))
    
    # Voice Processing
    ENABLE_VOICE = os.getenv('ENABLE_VOICE', 'True').lower() == 'true'
    MAX_AUDIO_SIZE = int(os.getenv('MAX_AUDIO_SIZE', '10485760'))  # 10MB
    
    # Battery System
    BATTERY_DECAY_RATE = float(os.getenv('BATTERY_DECAY_RATE', '0.1'))
    BATTERY_RECHARGE_TIME = int(os.getenv('BATTERY_RECHARGE_TIME', '300'))  # 5 minutes
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5000').split(',')