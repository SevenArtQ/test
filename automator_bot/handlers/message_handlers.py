from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ai_service import AIService
from services.automation_service import AutomationService
from services.feedback_service import FeedbackService
from services.memory_service import MemoryService
from services.image_service import ImageService
from services.analysis_service import AnalysisService
from services.achievement_service import AchievementService
from services.excel_service import ExcelService
import re
from datetime import datetime
from handlers.command_handlers import help_command, settings, about, feedback, start

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    user_message = update.message.text
    
    # Обработка кнопок меню
    if user_message == "🤖 AI Помощник":
        keyboard = [
            [KeyboardButton("↩️ Вернуться в главное меню")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "Режим AI помощника активирован!\n"
            "Задайте любой вопрос, и я постараюсь на него ответить.\n"
            "Для возврата в главное меню нажмите кнопку ниже.",
            reply_markup=reply_markup
        )
        context.user_data['mode'] = 'ai_assistant'
        return
    
    # Возврат в главное меню
    elif user_message == "↩️ Вернуться в главное меню":
        await start(update, context)
        context.user_data['mode'] = None
        return
        
    elif user_message == "ℹ️ О боте":
        await about(update, context)
        return
        
    elif user_message == "📝 Отзыв":
        await feedback(update, context)
        return
        
    elif user_message == "📝 Обычный отзыв":
        context.user_data['feedback_type'] = 'regular'
        context.user_data['mode'] = 'waiting_feedback'
        await update.message.reply_text(
            "Напишите ваш отзыв о боте:",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("↩️ Отмена")]], resize_keyboard=True)
        )
        return
        
    elif user_message == "🎭 Анонимный отзыв":
        context.user_data['feedback_type'] = 'anonymous'
        context.user_data['mode'] = 'waiting_anonymous_name'
        await update.message.reply_text(
            "Как вы хотите представиться?",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("↩️ Отмена")]], resize_keyboard=True)
        )
        return
        
    elif user_message == "↩️ Отмена":
        await start(update, context)
        context.user_data['mode'] = None
        return
    
    elif user_message == "👀 Посмотреть отзывы":
        feedbacks = FeedbackService.get_recent_feedbacks()
        await update.message.reply_text(
            feedbacks,
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("↩️ Вернуться в главное меню")]], resize_keyboard=True)
        )
        return
    
    elif user_message == "🎨 Генерация изображений":
        keyboard = [
            [KeyboardButton("↩️ Вернуться в главное меню")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "🎨 Режим генерации изображений\n\n"
            "Опишите изображение, которое хотите создать.\n"
            "Например: 'космический корабль в стиле киберпанк' или 'котенок играет с клубком в стиле аниме'",
            reply_markup=reply_markup
        )
        context.user_data['mode'] = 'image_generation'
        return
    
    elif user_message == "📊 Анализ текста":
        keyboard = [
            [KeyboardButton("↩️ Вернуться в главное меню")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "📊 Режим анализа текста\n\n"
            "Отправьте текст, который хотите проанализировать.\n"
            "Я определю его тональность, ключевые слова и темы.",
            reply_markup=reply_markup
        )
        context.user_data['mode'] = 'text_analysis'
        return
        
    elif user_message == "📈 Excel помощник":
        keyboard = [
            [KeyboardButton("📤 Загрузить Excel"), KeyboardButton("📝 Создать Excel")],
            [KeyboardButton("↩️ Вернуться в главное меню")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "📈 Excel помощник\n\n"
            "Я могу помочь вам с Excel файлами:\n"
            "- Загрузите файл для редактирования\n"
            "- Создайте новый файл из данных\n"
            "- Используйте команды для работы с данными",
            reply_markup=reply_markup
        )
        context.user_data['mode'] = 'excel_helper'
        return
    
    elif user_message == "👤 Мой профиль":
        user_data = AchievementService.get_user_level(update.effective_user.id)
        
        profile_text = (
            f"👤 Ваш профиль:\n\n"
            f"🏅 Уровень: {user_data['level']}\n"
            f"✨ Титул: {user_data['title']}\n"
            f"📈 Опыт: {user_data['exp']}\n"
            f"🎯 До следующего уровня: {user_data['next_level'] - user_data['exp']}\n\n"
            f"🏆 Достижения:\n"
        )
        
        for achievement in user_data['achievements'][-5:]:  # Последние 5 достижений
            profile_text += f"• {achievement['title']} - {achievement['date']}\n"
            
        await update.message.reply_text(profile_text)
        return
    
    # Обработка режимов отзыва
    if context.user_data.get('mode') == 'waiting_anonymous_name':
        context.user_data['anonymous_name'] = user_message
        context.user_data['mode'] = 'waiting_feedback'
        await update.message.reply_text("Теперь напишите ваш отзыв о боте:")
        return
        
    elif context.user_data.get('mode') == 'waiting_feedback':
        feedback_type = context.user_data.get('feedback_type')
        if feedback_type == 'regular':
            author = update.message.from_user.username or update.message.from_user.first_name
        else:
            author = context.user_data.get('anonymous_name', 'Аноним')
            
        # Сохраняем отзыв
        FeedbackService.save_feedback(
            author=author,
            text=user_message,
            is_anonymous=(feedback_type == 'anonymous')
        )
        
        await update.message.reply_text(
            "Спасибо за ваш отзыв! 🙏\n"
            "Вы можете посмотреть другие отзывы, нажав '👀 Посмотреть отзывы'",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("↩️ Вернуться в главное меню")]], resize_keyboard=True)
        )
        context.user_data['mode'] = None
        return
    
    # Обработка сообщений в режиме AI
    if context.user_data.get('mode') == 'ai_assistant':
        try:
            await update.message.chat.send_action(ChatAction.TYPING)
            
            # Сохраняем сообщение пользователя
            MemoryService.save_message(
                user_id=update.effective_user.id,
                username=update.effective_user.username or update.effective_user.first_name,
                message=user_message
            )
            
            # Получаем ответ от AI
            ai_response = AIService.generate_response(
                prompt=user_message,
                user_id=update.effective_user.id
            )
            
            # Сохраняем ответ бота
            MemoryService.save_message(
                user_id=update.effective_user.id,
                username=update.effective_user.username or update.effective_user.first_name,
                message=ai_response,
                is_bot=True
            )
            
            await update.message.reply_text(ai_response)
            
            AchievementService.add_experience(update.effective_user.id, "message")
            
        except Exception as e:
            print(f"Ошибка при обработке сообщения: {str(e)}")
            await update.message.reply_text(
                "Извините, произошла ошибка. Попробуйте позже или переформулируйте вопрос."
            )
    elif context.user_data.get('mode') == 'image_generation':
        try:
            await update.message.chat.send_action(ChatAction.UPLOAD_PHOTO)
            await update.message.reply_text("🎨 Генерирую изображение, подождите...")
            
            # Генерируем изображение
            image_url = await ImageService.generate_image(
                prompt=user_message,
                user_id=update.effective_user.id
            )
            
            if image_url.startswith('http'):
                await update.message.reply_photo(image_url)
            else:
                await update.message.reply_text(image_url)
                
        except Exception as e:
            print(f"Ошибка при генерации изображения: {str(e)}")
            await update.message.reply_text(
                "Извините, произошла ошибка при генерации изображения. Попробуйте другое описание."
            )
    elif context.user_data.get('mode') == 'text_analysis':
        await update.message.chat.send_action(ChatAction.TYPING)  # Показываем "печатает"
        await update.message.reply_text("📊 Анализирую текст...")
        try:
            analysis = await AnalysisService.analyze_text(user_message)
            if analysis:
                await update.message.chat.send_action(ChatAction.TYPING)
                response = (
                    f"📊 Результаты анализа:\n\n"
                    f"😊 Тональность: {analysis['sentiment']}\n"
                    f"🔑 Ключевые слова: {', '.join(analysis['keywords'])}\n"
                    f"📝 Основные темы: {analysis['themes']}\n"
                    f"📏 Статистика:\n"
                    f"- Слов: {analysis['word_count']}\n"
                    f"- Символов: {analysis['char_count']}"
                )
                await update.message.reply_text(response)
                
                # Добавляем опыт за использование анализа
                AchievementService.add_experience(update.effective_user.id, "analysis")
                
        except Exception as e:
            print(f"Ошибка при анализе текста: {e}")
            await update.message.reply_text(
                "Извините, произошла ошибка при анализе текста. Попробуйте другой текст."
            )
    elif context.user_data.get('mode') == 'excel_helper':
        if user_message == "↩️ Вернуться в меню":
            # Очищаем данные о текущем Excel файле
            if 'current_excel' in context.user_data:
                del context.user_data['current_excel']
            context.user_data['mode'] = None
            
            # Возвращаемся в главное меню
            keyboard = [
                [KeyboardButton("🤖 AI Помощник"), KeyboardButton("🎨 Генерация изображений")],
                [KeyboardButton("📊 Анализ текста"), KeyboardButton("📈 Excel помощник")],
                [KeyboardButton("ℹ️ О боте"), KeyboardButton("📝 Отзыв")],
                [KeyboardButton("🎮 Игровой центр", web_app=WebAppInfo(url="http://localhost:5000"))]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            
            await update.message.reply_text(
                "Вы вернулись в главное меню. Выберите действие:",
                reply_markup=reply_markup
            )
            return
            
        elif update.message.document:  # Если пользователь отправил файл
            file = await context.bot.get_file(update.message.document.file_id)
            file_path = f"excel_files/temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            os.makedirs("excel_files", exist_ok=True)
            await file.download_to_drive(file_path)
            
            # Читаем информацию о файле
            info = await ExcelService.read_excel(file_path)
            
            # Создаем клавиатуру с командами
            keyboard = [
                [KeyboardButton("📊 Сортировать"), KeyboardButton("🔍 Фильтровать")],
                [KeyboardButton("➕ Добавить столбец"), KeyboardButton("➖ Удалить столбец")],
                [KeyboardButton("📋 Информация"), KeyboardButton("↩️ Вернуться в меню")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            
            await update.message.reply_text(
                f"{info}\n\n"
                "Выберите действие с файлом:",
                reply_markup=reply_markup
            )
            context.user_data['current_excel'] = file_path
            
        elif user_message == "📊 Сортировать":
            await update.message.reply_text(
                "Введите название столбца для сортировки\n"
                "Например: сортировать по Имя"
            )
            
        elif user_message == "🔍 Фильтровать":
            await update.message.reply_text(
                "Введите условие фильтрации\n"
                "Например: фильтровать где Возраст > 25"
            )
            
        elif user_message == "➕ Добавить столбец":
            await update.message.reply_text(
                "Введите название нового столбца\n"
                "Например: добавить столбец Зарплата"
            )
            
        elif user_message == "➖ Удалить столбец":
            await update.message.reply_text(
                "Введите название столбца для удаления\n"
                "Например: удалить столбец Возраст"
            )
            
        elif user_message == "📋 Информация":
            if 'current_excel' in context.user_data:
                info = await ExcelService.read_excel(context.user_data['current_excel'])
                await update.message.reply_text(info)
            else:
                await update.message.reply_text("Сначала загрузите Excel файл!")
            
        elif user_message.startswith(("сортировать", "фильтровать", "добавить", "удалить")):
            if 'current_excel' in context.user_data:
                edited_file = await ExcelService.edit_excel(
                    context.user_data['current_excel'],
                    user_message
                )
                await update.message.reply_document(
                    document=open(edited_file, 'rb'),
                    caption="Вот ваш отредактированный файл!"
                )
            else:
                await update.message.reply_text("Сначала загрузите Excel файл!")
    else:
        await update.message.reply_text(
            "Для общения с AI помощником нажмите кнопку '🤖 AI Помощник'"
        )

async def handle_state(update: Update, context: ContextTypes.DEFAULT_TYPE, state: str, user_message: str):
    """Обработка различных состояний диалога"""
    if state == 'waiting_text_prompt':
        # Если пользователь выбрал тип текста (Реферат, Статья и т.д.)
        prompt = f"Сгенерируй {user_message.lower()} на тему: {context.user_data.get('topic', 'общая тема')}. "
        prompt += "Текст должен быть информативным, структурированным и интересным."
        
        await update.message.reply_text("Генерирую текст, пожалуйста подождите...")
        response = await AIService.generate_response(prompt)
        
        # Отправляем результат по частям, если текст длинный
        if len(response) > 4000:
            parts = [response[i:i+4000] for i in range(0, len(response), 4000)]
            for part in parts:
                await update.message.reply_text(part)
        else:
            await update.message.reply_text(response)
            
        context.user_data['state'] = None

    elif state == 'waiting_image_prompt':
        image_url = await AutomationService.generate_image(user_message)
        await update.message.reply_text(f"Ваше изображение: {image_url}")
        context.user_data['state'] = None

    elif state == 'waiting_analysis_text':
        analysis = await AutomationService.analyze_text(user_message)
        response = (
            f"Анализ текста:\n"
            f"Тональность: {analysis['sentiment']}\n"
            f"Ключевые слова: {', '.join(analysis['keywords'])}\n"
            f"Краткое содержание: {analysis['summary']}"
        )
        await update.message.reply_text(response)
        context.user_data['state'] = None

    elif state == 'waiting_translation':
        if user_message == "На английский":
            context.user_data['target_lang'] = 'en'
            await update.message.reply_text("Введите текст для перевода на английский:")
        elif user_message == "На русский":
            context.user_data['target_lang'] = 'ru'
            await update.message.reply_text("Enter text to translate to Russian:")
        elif user_message == "↩️ Назад":
            context.user_data['state'] = None
            await start(update, context)
        else:
            target_lang = context.user_data.get('target_lang', 'en')
            translation = await AutomationService.translate_text(user_message, target_lang)
            await update.message.reply_text(translation)
            context.user_data['state'] = None

    elif state == 'waiting_reminder':
        # Простой парсер для времени напоминания
        match = re.search(r'(.*?)(?:завтра в|сегодня в|в)?\s*(\d{1,2}:\d{2})', user_message)
        if match:
            text = match.group(1).strip()
            time_str = match.group(2)
            time = datetime.strptime(time_str, "%H:%M")
            if await AutomationService.set_reminder(update.effective_user.id, text, time):
                await update.message.reply_text(f"Напоминание установлено на {time_str}")
            else:
                await update.message.reply_text("Не удалось установить напоминание")
        else:
            await update.message.reply_text(
                "Неверный формат. Пример: Купить молоко завтра в 18:00"
            )
        context.user_data['state'] = None 