import g4f
import re
from textblob import TextBlob
import matplotlib.pyplot as plt
import io
import os
from datetime import datetime

class AnalysisService:
    @staticmethod
    async def analyze_image(image_url: str) -> str:
        """Анализ изображения и описание его содержимого"""
        
    @staticmethod
    async def analyze_text(text: str) -> dict:
        """Глубокий анализ текста: тональность, ключевые слова, темы"""
        try:
            # Анализ тональности через TextBlob
            blob = TextBlob(text)
            sentiment = "позитивный" if blob.sentiment.polarity > 0 else "негативный" if blob.sentiment.polarity < 0 else "нейтральный"
            
            # Простой анализ ключевых слов
            words = text.lower().split()
            # Исключаем стоп-слова и короткие слова
            stop_words = {'и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то', 'все', 'она', 'так', 'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только', 'ее', 'мне', 'было', 'вот', 'от', 'меня', 'еще', 'нет', 'о', 'из', 'ему'}
            keywords = [word for word in words if len(word) > 3 and word not in stop_words]
            keywords = list(set(keywords))[:7]  # Берем только уникальные слова, максимум 7
            
            # Определяем основную тему
            themes = "Общая тема текста"
            if len(text) > 20:  # Если текст достаточно длинный
                themes = f"Текст о {', '.join(keywords[:3])}"  # Используем первые 3 ключевых слова
            
            return {
                "sentiment": sentiment,
                "keywords": keywords,
                "themes": themes,
                "word_count": len(words),
                "char_count": len(text)
            }
        except Exception as e:
            print(f"Ошибка при анализе текста: {e}")
            return None

    @staticmethod
    async def generate_statistics(data: str) -> str:
        """Генерация статистики и визуализаций"""
        try:
            # Создаем график
            plt.figure(figsize=(10, 6))
            
            # Анализируем данные (пример для числовых данных)
            numbers = [float(x) for x in re.findall(r'-?\d+\.?\d*', data)]
            
            if numbers:
                plt.plot(numbers)
                plt.title('Анализ данных')
                plt.xlabel('Индекс')
                plt.ylabel('Значение')
                
                # Сохраняем график
                os.makedirs("statistics", exist_ok=True)
                output_path = f"statistics/graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                plt.savefig(output_path)
                plt.close()
                
                return output_path
                
        except Exception as e:
            print(f"Ошибка при генерации статистики: {e}")
            return None 