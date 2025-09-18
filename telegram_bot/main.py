from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
)
from src.calc.totals import calc_total

SPECIALTY, EDUCATION, EXPERIENCE, CATEGORY, ZONE, LOCALITY, ORG_TYPE, UCHASTOK = range(8)

async def restart_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if isinstance(context.user_data, dict):
        context.user_data.clear()
    keyboard = [["Врач", "Медсестра", "Другое"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Выберите вашу должность:",
        reply_markup=reply_markup
    )
    return SPECIALTY

async def specialty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    context.user_data["specialty"] = update.message.text
    if update.message.text == "Медсестра":
        keyboard = [["Высшее", "Среднее"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Укажите образование:", reply_markup=reply_markup)
        return EDUCATION
    elif update.message.text == "Врач":
        context.user_data["education"] = "высшее"
        await update.message.reply_text("Введите ваш опыт работы (лет):")
        return EXPERIENCE
    else:
        await update.message.reply_text("Пока поддерживаются только должности 'Врач' и 'Медсестра'.")
        return ConversationHandler.END

async def education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("specialty") == "Медсестра":
        context.user_data["education"] = update.message.text
        await update.message.reply_text("Введите ваш опыт работы (лет):")
        return EXPERIENCE
    else:
        context.user_data["education"] = "—"
        await update.message.reply_text("Введите ваш опыт работы (лет):")
        return EXPERIENCE

async def experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    context.user_data["experience"] = update.message.text
    keyboard = [["Высшая", "Первая"], ["Вторая", "Нет категории"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Выберите вашу категорию:", reply_markup=reply_markup)
    return CATEGORY

async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    context.user_data["category"] = update.message.text
    keyboard = [["Да", "Нет"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Ваша работа относится к зоне экологического неблагополучия?", reply_markup=reply_markup)
    return ZONE

async def zone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    if update.message.text == "Да":
        zone_keyboard = [
            ["Экол. катастрофы", "экол. кризиса"],
            ["Экол. предкризис", "чрезвыч риск радиации"],
            ["максим риск радиации", "повыш риск радиации"],
            ["миним риск радиации", "льгот соц-экон статус"],
            ["Нет"]
        ]
        reply_markup = ReplyKeyboardMarkup(zone_keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Уточните зону:", reply_markup=reply_markup)
        return ZONE
    else:
        context.user_data["zone"] = "Нет"
        keyboard = [["Город", "Село"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Вы проживаете в городе или селе?", reply_markup=reply_markup)
        return LOCALITY

async def locality(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    context.user_data["locality"] = update.message.text
    keyboard = [["Стационар", "Поликлиника"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Выберите тип медорганизации:", reply_markup=reply_markup)
    return ORG_TYPE

async def org_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    org_type_value = update.message.text
    if org_type_value not in ["Стационар", "Поликлиника"]:
        keyboard = [["Стационар", "Поликлиника"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Пожалуйста, выберите тип медорганизации:", reply_markup=reply_markup)
        return ORG_TYPE

    context.user_data["org_type"] = org_type_value

    # Ветвление по типу организации и роли
    if org_type_value == "Стационар":
        keyboard = [["Да", "Нет"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Ваша должность хирургическая?", reply_markup=reply_markup)
        return UCHASTOK
    elif org_type_value == "Поликлиника":
        keyboard = [["Да", "Нет"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Вы участковый специалист?", reply_markup=reply_markup)
        return UCHASTOK

async def uchastok_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    text = update.message.text

    # Для стационара — хирургия
    if context.user_data.get("org_type") == "Стационар":
        context.user_data["is_surgery"] = text == "Да"
        # Для медсестры — вопрос о старшей медсестре
        if context.user_data.get("specialty") == "Медсестра":
            keyboard = [["Да", "Нет"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            await update.message.reply_text("Вы являетесь старшей медсестрой?", reply_markup=reply_markup)
            return UCHASTOK
        # После хирургии для врача — сразу расчет
        return await org_type(update, context)

    # Для поликлиники — участковый
    if context.user_data.get("org_type") == "Поликлиника":
        context.user_data["is_uchastok"] = text == "Да"
        # Для медсестры — вопрос о старшей медсестре
        if context.user_data.get("specialty") == "Медсестра":
            keyboard = [["Да", "Нет"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            await update.message.reply_text("Вы являетесь старшей медсестрой?", reply_markup=reply_markup)
            return UCHASTOK
        # После участкового для врача — сразу расчет
        return await org_type(update, context)

    # Для медсестры — старшая медсестра
    if context.user_data.get("specialty") == "Медсестра" and "senior_nurse" not in context.user_data:
        context.user_data["senior_nurse"] = text == "Да"
        return await org_type(update, context)

    # Если все параметры собраны — расчет
    return await org_type(update, context)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and hasattr(update.message, "reply_text"):
        await update.message.reply_text("Диалог отменён.")
    return ConversationHandler.END

async def exit_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and hasattr(update.message, "reply_text"):
        await update.message.reply_text("Спасибо за использование бота! До свидания.")
    if isinstance(context.user_data, dict):
        context.user_data.clear()
    return ConversationHandler.END

# --- Запуск приложения ---
import re
state_handlers = [
    (SPECIALTY, specialty),
    (EDUCATION, education),
    (EXPERIENCE, experience),
    (CATEGORY, category),
    (ZONE, zone),
    (LOCALITY, locality),
    (ORG_TYPE, org_type),
    (UCHASTOK, uchastok_handler),
]

START_REGEX = filters.Regex(re.compile(r"^(старт|start)$", re.IGNORECASE))
EXIT_REGEX = filters.Regex(re.compile(r"^выход$", re.IGNORECASE))
states = {
    state: [
        MessageHandler(filters.TEXT & ~filters.COMMAND, handler),
        MessageHandler(EXIT_REGEX, exit_handler),
        MessageHandler(START_REGEX, restart_handler),
    ]
    for state, handler in state_handlers
}

conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", restart_handler),
        MessageHandler(START_REGEX & ~filters.COMMAND, restart_handler)
    ],
    states=states,  # type: ignore
    fallbacks=[
        CommandHandler("cancel", exit_handler),
        MessageHandler(EXIT_REGEX, exit_handler),
        MessageHandler(START_REGEX, restart_handler)
    ],
)

if not TOKEN:
    print("Ошибка: TELEGRAM_TOKEN не задан в переменных окружения.")
    exit(1)

app = Application.builder().token(str(TOKEN)).build()
app.add_handler(conv_handler)
app.run_polling()