import sys
import os

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
import nest_asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config.config import Config
from handlers.command_handlers import start, help_command, about, settings, feedback, cancel
from handlers.message_handlers import handle_message
from handlers.callback_handlers import handle_callback
from utils.logger import setup_logger

nest_asyncio.apply()

async def main():
    # Настройка логирования
    setup_logger()
    logger = logging.getLogger(__name__)
    
    # Создание приложения
    application = Application.builder().token(Config.TELEGRAM_TOKEN).build()
    
    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("settings", settings))
    application.add_handler(CommandHandler("feedback", feedback))
    application.add_handler(CommandHandler("cancel", cancel))
    
    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(
        filters.TEXT | filters.Document.ALL | filters.PHOTO,
        handle_message
    ))
    
    # Обработчик callback запросов
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    # Запуск бота
    logger.info("Bot started")
    await application.run_polling(allowed_updates=[], drop_pending_updates=True)

if __name__ == '__main__':
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass 