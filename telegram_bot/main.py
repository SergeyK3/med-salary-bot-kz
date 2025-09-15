from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
)
from src.calc.totals import calc_total

# Состояния диалога
async def restart_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if isinstance(context.user_data, dict):
        context.user_data.clear()
    return await start(update, context)

SPECIALTY, EDUCATION, EXPERIENCE, CATEGORY, ZONE, LOCALITY, ORG_TYPE, UCHASTOK = range(8)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    context.user_data.clear()
    keyboard = [["Врач", "Медсестра"]]
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
    else:
        # Для врача образование сразу "высшее"
        context.user_data["education"] = "высшее"
        # Для врача сразу спрашиваем про хирургическую должность
        keyboard = [["Да", "Нет"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(
            "Ваша должность хирургическая?",
            reply_markup=reply_markup
        )
        return UCHASTOK

async def education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    if context.user_data.get("specialty") == "Медсестра":
        context.user_data["education"] = update.message.text
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
        # Предложить выбор конкретной зоны
        zone_keyboard = [
            ["Экол. катастрофы", "экол. кризиса"],
            ["Экол. предкризис", "чрезвыч риск радиации"],
            ["максим риск радиации", "повыш риск радиации"],
            ["миним риск радиации", "льгот соц-экон статус"],
            ["Нет"]
        ]
        reply_markup = ReplyKeyboardMarkup(zone_keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Уточните зону:", reply_markup=reply_markup)
        return ZONE  # повторно, чтобы сохранить выбранную зону
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

# Вопрос о хирургической должности
async def org_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    org_type_value = update.message.text
    # Разрешаем только выбор из двух кнопок
    if org_type_value not in ["Стационар", "Поликлиника"]:
        keyboard = [["Стационар", "Поликлиника"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Пожалуйста, выберите тип медорганизации:", reply_markup=reply_markup)
        return ORG_TYPE

    answers = {
        "role": context.user_data.get("specialty"),
        "education": context.user_data.get("education"),
        "category": context.user_data.get("category"),
        "experience_years": context.user_data.get("experience"),
        "eco_zone": context.user_data.get("zone"),
        "location": context.user_data.get("locality"),
        "facility": context.user_data.get("org_type"),
        "senior_nurse": context.user_data.get("senior_nurse", False),
        "hazard_profile": None,
        "is_surgery": context.user_data.get("is_surgery", False),
        "is_uchastok": context.user_data.get("is_uchastok", False),
    }

    result = calc_total(answers)
    total = result["total_salary"]
    base_oklad = result["base_oklad"]
    allowances = result["allowances"]
    ets_coeff = result.get("ets_coeff")
    role_multiplier = result.get("role_multiplier")

    param_names = {
        "specialty": "должность",
        "education": "образование",
        "experience": "опыт работы",
        "category": "категория",
        "zone": "зона экологического неблагополучия",
        "locality": "местность проживания",
        "org_type": "тип медорганизации",
        "is_uchastok": "участковый специалист",
        "is_surgery": "хирургическая должность",
        "senior_nurse": "старшая медсестра",
    }
    # Выводить "Да"/"Нет" для хирургической должности
    def surgery_ru(val):
        if isinstance(val, bool):
            return "Да" if val else "Нет"
        if val in [True, "Да"]:
            return "Да"
        if val in [False, "Нет"]:
            return "Нет"
        return val
    summary_lines = []
    for k in param_names:
        v = context.user_data.get(k)
        if k == "is_surgery":
            v = surgery_ru(v)
        summary_lines.append(f"{param_names[k]}: {v}")
    summary = "\n".join(summary_lines)

    allowance_names = {
        "k1": "Экологическая зона",
        "k2": "Сельская местность",
        "k3": "Старшая медсестра",
        "k4": "Вредные условия",
        "k5": "Психоэмоц напряжение",
        "special": "Особые условия труда",
    }
    # Не показывать надбавку "Старшая медсестра" для врача
    role = context.user_data.get("specialty")
    allowance_details = "\n".join([
        f"{allowance_names.get(k, k)}: {round(v, 2) if k == 'special' else v}"
        for k, v in allowances.items()
        if k in allowance_names and not (k == "k3" and role == "Врач")
    ])

    # Формируем строку с сомножителями
    multipliers = ""
    # Для врачей и медсестер — фиксированные значения
    role_mult_val = None
    if context.user_data.get("specialty") == "Врач":
        role_mult_val = 3.42
    elif context.user_data.get("specialty") == "Медсестра":
        role_mult_val = 2.34
    if ets_coeff is not None or role_mult_val is not None:
        parts = []
        if ets_coeff is not None:
            parts.append(f"ETS coeff: {ets_coeff}")
        if role_mult_val is not None:
            parts.append(f"Role multiplier: {role_mult_val}")
        multipliers = f" ({' '.join(parts)})"
    await update.message.reply_text(
        f"Спасибо! Ваши параметры:\n{summary}\n\n"
        f"Должностной оклад: {base_oklad} KZT{multipliers}\n"
        f"Надбавки:\n{allowance_details}\n"
        f"\nРасчёт завершён!\nВаша зарплата: {total} KZT\n"
        f"Это предварительная начисленная зарплата. Реальные расчеты могут быть меньше примерно на 20%: 10% обязательные пенсионные взносы и 10% подоходный налог."
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and hasattr(update.message, "reply_text"):
        await update.message.reply_text("Диалог отменён.")
    return ConversationHandler.END

# Добавить обработку ответа на уточняющий вопрос
async def uchastok_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return ConversationHandler.END
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    if context.user_data is None:
        context.user_data = {}
    text = update.message.text
    # Определяем, какой параметр ожидается
    if "is_surgery" not in context.user_data and context.user_data.get("specialty") == "Врач":
        context.user_data["is_surgery"] = text == "Да"
        return await education(update, context)
    if "hazard_profile" not in context.user_data:
        if text == "Да":
            # Предложить выбор отделения с вредностью
            hazard_departments = [
                ["Рентген"], ["УЗИ"], ["Инфекционное отделение"], ["Паллиатив"],
                ["Анестезиология и реанимация"], ["Трансфузиология"], ["Эндоскопия"],
                ["Физиотерапия"], ["Клинико-диагностическая лаборатория"], ["Бактериологическая лаборатория"],
                ["Цитологическая лаборатория"], ["Морг и патоморфологическая лаборатория"]
            ]
            reply_markup = ReplyKeyboardMarkup(hazard_departments, one_time_keyboard=True, resize_keyboard=True)
            await update.message.reply_text(
                "Уточните отделение с вредными условиями труда:",
                reply_markup=reply_markup
            )
            # Следующий ответ будет отделение
            return UCHASTOK
        else:
            context.user_data["hazard_profile"] = None
            return await org_type(update, context)
    elif context.user_data.get("hazard_profile") is None and text in [
        "Рентген", "УЗИ", "Инфекционное отделение", "Паллиатив", "Анестезиология и реанимация",
        "Трансфузиология", "Эндоскопия", "Физиотерапия", "Клинико-диагностическая лаборатория",
        "Бактериологическая лаборатория", "Цитологическая лаборатория", "Морг и патоморфологическая лаборатория"
    ]:
        context.user_data["hazard_profile"] = text
        # После выбора отделения сразу переходить к расчету
        return await org_type(update, context)
    elif "senior_nurse" not in context.user_data and context.user_data.get("specialty") == "Медсестра":
        context.user_data["senior_nurse"] = text == "Да"
    elif "is_uchastok" not in context.user_data and context.user_data.get("specialty") == "Медсестра" and context.user_data.get("org_type") == "Поликлиника":
        context.user_data["is_uchastok"] = text == "Да"
    return await org_type(update, context)

app = Application.builder().token(str(TOKEN)).build()

async def exit_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and hasattr(update.message, "reply_text"):
        await update.message.reply_text("Спасибо за использование бота! До свидания.")
    if isinstance(context.user_data, dict):
        context.user_data.clear()
    return ConversationHandler.END

# --- Запуск приложения ---
conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", restart_handler),
        MessageHandler(filters.Regex("^(Старт|старт)$") & ~filters.COMMAND, restart_handler)
    ],
    states={
        SPECIALTY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, specialty),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        EDUCATION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, education),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        EXPERIENCE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, experience),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        CATEGORY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, category),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        ZONE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, zone),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        LOCALITY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, locality),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        ORG_TYPE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, org_type),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        UCHASTOK: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, uchastok_handler),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
    },
    fallbacks=[
        CommandHandler("cancel", exit_handler),
        MessageHandler(filters.Regex("^Выход$"), exit_handler),
        MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler)
    ],
)
if not TOKEN:
    print("Ошибка: TELEGRAM_TOKEN не задан в переменных окружения.")
    exit(1)
app = Application.builder().token(str(TOKEN)).build()
app.add_handler(conv_handler)
app.run_polling()

# --- Запуск приложения ---
conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", restart_handler),
        MessageHandler(filters.Regex("^(Старт|старт)$") & ~filters.COMMAND, restart_handler)
    ],
    states={
        SPECIALTY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, specialty),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        EDUCATION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, education),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        EXPERIENCE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, experience),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        CATEGORY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, category),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        ZONE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, zone),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        LOCALITY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, locality),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        ORG_TYPE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, org_type),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        UCHASTOK: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, uchastok_handler),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
    },
    fallbacks=[
        CommandHandler("cancel", exit_handler),
        MessageHandler(filters.Regex("^Выход$"), exit_handler),
        MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler)
    ],
)
if not TOKEN:
    print("Ошибка: TELEGRAM_TOKEN не задан в переменных окружения.")
    exit(1)
app = Application.builder().token(str(TOKEN)).build()
app.add_handler(conv_handler)
app.run_polling()

# --- Запуск приложения ---
conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", restart_handler),
        MessageHandler(filters.Regex("^(Старт|старт)$") & ~filters.COMMAND, restart_handler)
    ],
    states={
        SPECIALTY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, specialty),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        EDUCATION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, education),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        EXPERIENCE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, experience),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        CATEGORY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, category),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        ZONE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, zone),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        LOCALITY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, locality),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        ORG_TYPE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, org_type),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        UCHASTOK: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, uchastok_handler),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
    },
    fallbacks=[
        CommandHandler("cancel", exit_handler),
        MessageHandler(filters.Regex("^Выход$"), exit_handler),
        MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler)
    ],
)
if not TOKEN:
    print("Ошибка: TELEGRAM_TOKEN не задан в переменных окружения.")
    exit(1)
app = Application.builder().token(str(TOKEN)).build()
app.add_handler(conv_handler)
app.run_polling()
conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", restart_handler),
        MessageHandler(filters.Regex("^(Старт|старт)$") & ~filters.COMMAND, restart_handler)
    ],
    states={
        SPECIALTY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, specialty),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        EDUCATION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, education),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        EXPERIENCE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, experience),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        CATEGORY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, category),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        ZONE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, zone),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        LOCALITY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, locality),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        ORG_TYPE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, org_type),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        UCHASTOK: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, uchastok_handler),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
    },
    fallbacks=[
        CommandHandler("cancel", exit_handler),
        MessageHandler(filters.Regex("^Выход$"), exit_handler),
        MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler)
    ],
)
if not TOKEN:
    print("Ошибка: TELEGRAM_TOKEN не задан в переменных окружения.")
    exit(1)
app = Application.builder().token(TOKEN).build()
app.add_handler(conv_handler)
app.run_polling()

# --- Запуск приложения ---
conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", restart_handler),
        MessageHandler(filters.Regex("^(Старт|старт)$") & ~filters.COMMAND, restart_handler)
    ],
    states={
        SPECIALTY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, specialty),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        EDUCATION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, education),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        EXPERIENCE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, experience),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        CATEGORY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, category),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        ZONE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, zone),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        LOCALITY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, locality),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        ORG_TYPE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, org_type),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
        UCHASTOK: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, uchastok_handler),
            MessageHandler(filters.Regex("^Выход$"), exit_handler),
            MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler),
        ],
    },
    fallbacks=[
        CommandHandler("cancel", exit_handler),
        MessageHandler(filters.Regex("^Выход$"), exit_handler),
        MessageHandler(filters.Regex("^(Старт|старт)$"), restart_handler)
    ],
)
if not TOKEN:
    print("Ошибка: TELEGRAM_TOKEN не задан в переменных окружения.")
    exit(1)
app = Application.builder().token(TOKEN).build()
app.add_handler(conv_handler)
app.run_polling()
