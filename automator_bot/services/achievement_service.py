import json
import os
from datetime import datetime

class AchievementService:
    LEVELS = {
        1: {"exp": 0, "title": "Новичок"},
        2: {"exp": 100, "title": "Ученик"},
        3: {"exp": 300, "title": "Продвинутый"},
        4: {"exp": 600, "title": "Эксперт"},
        5: {"exp": 1000, "title": "Мастер"},
        6: {"exp": 1500, "title": "Гуру"},
        7: {"exp": 2100, "title": "Легенда"}
    }
    
    ACTIONS = {
        "message": 5,  # опыт за сообщение
        "image": 10,   # опыт за генерацию изображения
        "analysis": 15 # опыт за анализ данных
    }
    
    @staticmethod
    def _load_user_data():
        if os.path.exists("user_achievements.json"):
            with open("user_achievements.json", "r") as f:
                return json.load(f)
        return {}

    @staticmethod
    def _save_user_data(data):
        with open("user_achievements.json", "w") as f:
            json.dump(data, f)

    @staticmethod
    def add_experience(user_id: int, action_type: str):
        """Добавление опыта за действия"""
        user_data = AchievementService._load_user_data()
        user_id = str(user_id)
        
        if user_id not in user_data:
            user_data[user_id] = {"exp": 0, "level": 1, "achievements": []}
            
        # Добавляем опыт
        exp_gain = AchievementService.ACTIONS.get(action_type, 0)
        user_data[user_id]["exp"] += exp_gain
        
        # Проверяем повышение уровня
        current_exp = user_data[user_id]["exp"]
        current_level = user_data[user_id]["level"]
        
        # Проверяем все уровни выше текущего
        for level, data in AchievementService.LEVELS.items():
            if level > current_level and current_exp >= data["exp"]:
                user_data[user_id]["level"] = level
                # Добавляем достижение
                achievement = {
                    "title": f"Достигнут уровень {level}!",
                    "description": f"Получен титул: {data['title']}",
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                user_data[user_id]["achievements"].append(achievement)
                
        AchievementService._save_user_data(user_data)

    @staticmethod
    def get_user_level(user_id: int) -> dict:
        """Получение уровня и достижений пользователя"""
        user_data = AchievementService._load_user_data()
        user_id = str(user_id)
        
        if user_id not in user_data:
            return {
                "level": 1,
                "exp": 0,
                "title": "Новичок",
                "next_level": 100,
                "achievements": []
            }
            
        current_data = user_data[user_id]
        current_level = current_data["level"]
        current_exp = current_data["exp"]
        
        # Находим следующий уровень
        next_level_exp = None
        for level, data in AchievementService.LEVELS.items():
            if level > current_level:
                next_level_exp = data["exp"]
                break
                
        return {
            "level": current_level,
            "exp": current_exp,
            "title": AchievementService.LEVELS[current_level]["title"],
            "next_level": next_level_exp,
            "achievements": current_data.get("achievements", [])
        } 