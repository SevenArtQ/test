import requests
import os
from datetime import datetime
import urllib.parse
import hashlib
import time

class ImageService:
    @staticmethod
    async def generate_image(prompt: str, user_id: int) -> str:
        """Генерация изображения через Pollinations.ai"""
        try:
            # Создаем уникальный seed
            unique_string = f"{prompt}_{user_id}_{int(time.time())}"
            seed = int(hashlib.md5(unique_string.encode()).hexdigest(), 16) % 10000000
            
            # Улучшаем промпт
            enhanced_prompt = f"{prompt}, high quality, detailed, 4k, realistic"
            encoded_prompt = urllib.parse.quote(enhanced_prompt)
            
            # Формируем URL для Pollinations.ai
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
            
            # Проверяем доступность
            response = requests.head(image_url)
            if response.status_code == 200:
                return image_url
                
            return "Извините, сервис генерации временно недоступен."
            
        except Exception as e:
            print(f"Ошибка при генерации изображения: {e}")
            return "Произошла ошибка при генерации изображения. Попробуйте позже." 