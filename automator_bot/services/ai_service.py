import g4f
import base64
import requests
import random

class AIService:
    @staticmethod
    def analyze_image(image_path: str) -> str:
        """Анализ изображения через CogVLM"""
        try:
            print("Используем CogVLM для анализа")
            API_URL = "https://api-inference.huggingface.co/models/THUDM/cogvlm-chat-17b"
            
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            
            print("Отправляем запрос к CogVLM...")
            response = requests.post(
                API_URL,
                headers={"Content-Type": "application/json"},
                json={
                    "inputs": {
                        "image": base64.b64encode(image_bytes).decode(),
                        "prompt": "Что изображено на этой картинке? Ответь кратко на русском языке."
                    }
                }
            )
            
            print(f"Статус ответа CogVLM: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if result and isinstance(result, list) and len(result) > 0:
                    return f"CogVLM: {result[0]}"
                else:
                    print("CogVLM вернул пустой результат")
            else:
                print(f"CogVLM вернул ошибку: {response.text}")
            
            return "Извините, не удалось проанализировать изображение. Попробуйте еще раз."
            
        except Exception as e:
            print(f"Ошибка при анализе изображения: {e}")
            return "Произошла ошибка при обработке изображения."

    @staticmethod
    def generate_response(prompt: str, user_id: int = None) -> str:
        """Генерация ответа от ИИ через Free2GPT"""
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты - дружелюбный ассистент, который отвечает на русском языке."},
                    {"role": "user", "content": prompt}
                ],
                provider=g4f.Provider.Free2GPT,  # Free2GPT для текста
                stream=False
            )
            
            if response and len(str(response).strip()) > 0:
                return str(response)
            
        except Exception as e:
            print(f"Ошибка: {str(e)}")
        
        return "Извините, сейчас сервис недоступен. Попробуйте позже."
    
    @staticmethod
    def generate_fallback_response(prompt: str) -> str:
        """Генерация ответа на основе ключевых слов (если AI недоступен)"""
        prompt_lower = prompt.lower()
        
        if "привет" in prompt_lower:
            return "Привет! Как я могу помочь вам сегодня?"
            
        if "анекдот" in prompt_lower:
            return "Программист заходит в бар и заказывает 1.0 пива."
            
        if "python" in prompt_lower:
            return "Python - это высокоуровневый язык программирования с простым синтаксисом."
            
        if "стихотворение" in prompt_lower:
            return """
            Код пишу я день и ночь,
            Баги гоню из кода прочь.
            В функциях и классах я живу,
            И в Git свой код всегда пушу.
            """
            
        return "Расскажите подробнее, что вас интересует?"

    @staticmethod
    async def generate_response_old(prompt: str) -> str:
        """Генерация ответа на основе ключевых слов"""
        prompt_lower = prompt.lower()
        
        # Генерация текста
        if "статья" in prompt_lower:
            topics = ["технологии", "здоровье", "образование", "путешествия", "еда"]
            return f"Давайте напишем статью! Выберите тему:\n" + "\n".join([f"- {topic}" for topic in topics])
            
        # Анализ текста
        elif "анализ" in prompt_lower:
            return "Отправьте текст для анализа, и я помогу определить его основные темы, тональность и структуру."
            
        # Перевод
        elif "перевод" in prompt_lower or "переведи" in prompt_lower:
            return "Укажите текст для перевода и целевой язык (например: 'переведи на английский: привет')"
            
        # Помощь
        elif "помощь" in prompt_lower or "help" in prompt_lower:
            return """Я могу помочь вам с:
• Генерацией текста (статьи, посты, рефераты)
• Анализом текста
• Переводом
• Ответами на вопросы
Просто опишите, что нужно сделать!"""
            
        # Общие ответы
        else:
            return random.choice([
                "Расскажите подробнее, что именно вас интересует?",
                "Я готов помочь! Уточните, пожалуйста, задачу.",
                "Интересный вопрос! Давайте разберем его детальнее.",
                "Какой аспект этой темы вас интересует больше всего?"
            ]) 