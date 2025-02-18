import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram Bot токен
    TELEGRAM_TOKEN = '7303005720:AAFM1LAy7zYb2AJ5RqM6dxhB1YD-UZk31jY'  # Вернем ваш токен
    
    # Настройки логирования
    LOG_FILE = "bot.log"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Настройки базы данных
    DB_FILE = "bot_database.db"
    
    # Пути к файлам
    FEEDBACK_FILE = "feedbacks.json"
    MEMORY_FILE = "chat_history.json"
    ACHIEVEMENTS_FILE = "user_achievements.json"
    
    # Настройки AI
    AI_MODEL = "gpt-4"
    AI_PROVIDER = "DeepAi"
    
    # Настройки изображений
    IMAGE_PROVIDERS = ["Prodia", "DeepAi"]
    IMAGE_TIMEOUT = 120
    IMAGE_NEGATIVE_PROMPT = "bad quality, blurry, low resolution"
    IMAGE_STEPS = 25
    IMAGE_CFG = 7.5
    
    # Директории для сохранения файлов
    IMAGES_DIR = "images"
    VIDEOS_DIR = "videos"
    STATISTICS_DIR = "statistics"
    
    # API ключи
    AI_API_KEY = 'Jf6Iq3WSSgNOIGgvYFxj6ieW1rGfeTwX'
    
    # Настройки логирования
    LOG_LEVEL = 'INFO'
    
    # Настройки базы данных
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # Поддерживаемые языки
    SUPPORTED_LANGUAGES = ['ru', 'en']
    
    OPENAI_API_KEY = "your-api-key"  # Получите ключ на platform.openai.com 
    
    CLAUDE_API_KEY = "your-anthropic-api-key"  # Получите ключ на console.anthropic.com 
    
    GOOGLE_CLOUD_CREDENTIALS = "path/to/your/credentials.json"  # Путь к файлу с ключом
    
    # Админ ID
    ADMIN_ID = int(os.getenv('ADMIN_ID', 0))