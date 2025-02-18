import json
import os
from datetime import datetime, timedelta
from typing import List, Dict

class MemoryService:
    MEMORY_FILE = "bot_memory.json"
    MAX_HISTORY_PER_USER = 100  # Максимум 100 сообщений
    MAX_STORAGE_DAYS = 7  # Храним историю максимум 7 дней
    
    @staticmethod
    def save_message(user_id: int, username: str, message: str, is_bot: bool = False) -> None:
        """Сохранение сообщения в память"""
        memory_data = MemoryService._load_memory()
        current_time = datetime.now()
        
        # Очищаем старые сообщения перед сохранением новых
        MemoryService._cleanup_old_messages(memory_data)
        
        # Создаем запись для пользователя, если её нет
        if str(user_id) not in memory_data:
            memory_data[str(user_id)] = {
                "username": username,
                "history": []
            }
            
        # Добавляем сообщение в историю
        memory_data[str(user_id)]["history"].append({
            "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "message": message,
            "is_bot": is_bot
        })
        
        # Ограничиваем историю до 100 сообщений
        if len(memory_data[str(user_id)]["history"]) > MemoryService.MAX_HISTORY_PER_USER:
            memory_data[str(user_id)]["history"] = memory_data[str(user_id)]["history"][-MemoryService.MAX_HISTORY_PER_USER:]
        
        # Сохраняем обновленные данные
        MemoryService._save_memory(memory_data)
    
    @staticmethod
    def _cleanup_old_messages(memory_data: Dict) -> None:
        """Очистка старых сообщений"""
        cutoff_date = datetime.now() - timedelta(days=MemoryService.MAX_STORAGE_DAYS)
        
        for user_id in list(memory_data.keys()):
            # Фильтруем сообщения, оставляя только те, которые не старше MAX_STORAGE_DAYS
            history = memory_data[user_id]["history"]
            fresh_history = [
                msg for msg in history 
                if datetime.strptime(msg["timestamp"], "%Y-%m-%d %H:%M:%S") > cutoff_date
            ]
            
            if fresh_history:
                memory_data[user_id]["history"] = fresh_history
            else:
                # Если все сообщения старые, удаляем запись пользователя
                del memory_data[user_id]
    
    @staticmethod
    def get_user_history(user_id: int, limit: int = 5) -> List[Dict]:
        """Получение истории диалога с пользователем"""
        memory_data = MemoryService._load_memory()
        
        if str(user_id) not in memory_data:
            return []
            
        history = memory_data[str(user_id)]["history"]
        return history[-limit:] if limit else history
    
    @staticmethod
    def get_context_for_ai(user_id: int, limit: int = 5) -> str:
        """Формирование контекста для AI из истории диалога"""
        history = MemoryService.get_user_history(user_id, limit)
        
        if not history:
            return ""
            
        context = "Предыдущий контекст разговора:\n\n"
        for msg in history:
            speaker = "Бот" if msg["is_bot"] else "Пользователь"
            context += f"{speaker} ({msg['timestamp']}): {msg['message']}\n"
        
        return context + "\n"
    
    @staticmethod
    def _load_memory() -> Dict:
        """Загрузка данных из файла"""
        if os.path.exists(MemoryService.MEMORY_FILE):
            with open(MemoryService.MEMORY_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        return {}
    
    @staticmethod
    def _save_memory(data: Dict) -> None:
        """Сохранение данных в файл"""
        with open(MemoryService.MEMORY_FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2) 