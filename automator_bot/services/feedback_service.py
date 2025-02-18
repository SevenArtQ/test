from typing import List, Dict
import json
import os
from datetime import datetime

class FeedbackService:
    FEEDBACK_FILE = "feedback_data.json"
    
    @staticmethod
    def save_feedback(author: str, text: str, is_anonymous: bool = False) -> None:
        """Сохранение отзыва"""
        feedback = {
            'author': author,
            'text': text,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'is_anonymous': is_anonymous
        }
        
        # Загружаем существующие отзывы
        feedbacks = []
        if os.path.exists(FeedbackService.FEEDBACK_FILE):
            with open(FeedbackService.FEEDBACK_FILE, 'r', encoding='utf-8') as file:
                feedbacks = json.load(file)
        
        # Добавляем новый отзыв
        feedbacks.append(feedback)
        
        # Сохраняем обновленный список
        with open(FeedbackService.FEEDBACK_FILE, 'w', encoding='utf-8') as file:
            json.dump(feedbacks, file, ensure_ascii=False, indent=2)
    
    @staticmethod
    def get_recent_feedbacks(limit: int = 5) -> str:
        """Получение последних отзывов"""
        if not os.path.exists(FeedbackService.FEEDBACK_FILE):
            return "Пока нет отзывов 😢"
            
        with open(FeedbackService.FEEDBACK_FILE, 'r', encoding='utf-8') as file:
            feedbacks = json.load(file)
        
        if not feedbacks:
            return "Пока нет отзывов 😢"
            
        # Берем последние отзывы
        recent = feedbacks[-limit:]
        
        # Формируем текст
        result = "📝 Последние отзывы:\n\n"
        for feedback in recent:
            result += f"От: {feedback['author']}\n"
            result += f"Дата: {feedback['date']}\n"
            result += f"Отзыв: {feedback['text']}\n"
            result += "➖" * 20 + "\n\n"
            
        return result 