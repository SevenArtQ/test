from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    keyboard = [
        [KeyboardButton("🤖 AI Помощник"), KeyboardButton("🎨 Генерация изображений")],
        [KeyboardButton("📊 Анализ текста"), KeyboardButton("📈 Excel помощник")],
        [KeyboardButton("ℹ️ О боте"), KeyboardButton("📝 Отзыв")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "Привет! Я AI бот-помощник. Выберите действие:",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text(
        "Я могу помочь вам с:\n"
        "• Генерацией текста и ответами на вопросы\n"
        "• Созданием изображений\n"
        "• Анализом текста\n"
        "• Работой с Excel файлами\n\n"
        "Просто выберите нужную опцию в меню!"
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /about"""
    await update.message.reply_text(
        "🤖 AI Бот-помощник\n\n"
        "Я использую искусственный интеллект для помощи с различными задачами.\n\n"
        "🔹 Возможности:\n"
        "• Ответы на вопросы\n"
        "• Помощь с задачами\n"
        "• Генерация идей\n"
        "• Генерация изображений\n"
        "• Анализ текста\n"
        "• Excel автоматизация\n\n"
        "📱 Разработчик: @kachki2d\n\n"
        "Буду рад помочь! Просто напишите свой вопрос."
    )

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /settings"""
    keyboard = [
        [KeyboardButton("🔄 Сбросить настройки")],
        [KeyboardButton("↩️ Вернуться в главное меню")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "⚙️ Настройки бота\n\n"
        "Выберите действие:",
        reply_markup=reply_markup
    )

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /feedback"""
    keyboard = [
        [KeyboardButton("📝 Обычный отзыв"), KeyboardButton("🎭 Анонимный отзыв")],
        [KeyboardButton("👀 Посмотреть отзывы")],
        [KeyboardButton("↩️ Вернуться в главное меню")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "📝 Оставьте свой отзыв о боте\n\n"
        "Выберите тип отзыва:",
        reply_markup=reply_markup
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /cancel"""
    await start(update, context)

# Остальные обработчики команд будут добавлены позже 