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
SPECIALTY, EDUCATION, EXPERIENCE, CATEGORY, ZONE, LOCALITY, ORG_TYPE, UCHASTOK = range(8)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    keyboard = [["Врач", "Медсестра"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Выберите вашу должность:",
        reply_markup=reply_markup
    )
    return SPECIALTY

async def specialty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["specialty"] = update.message.text
    if update.message.text == "Медсестра":
        keyboard = [["Высшее", "Среднее"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Укажите образование:", reply_markup=reply_markup)
        return EDUCATION
    else:
        # Для врача сразу спрашиваем про хирургическую должность
        keyboard = [["Да", "Нет"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(
            "Ваша должность хирургическая?",
            reply_markup=reply_markup
        )
        return UCHASTOK

async def education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("specialty") == "Медсестра":
        context.user_data["education"] = update.message.text
    else:
        context.user_data["education"] = "—"
    await update.message.reply_text("Введите ваш опыт работы (лет):")
    return EXPERIENCE

async def experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["experience"] = update.message.text
    keyboard = [["Высшая", "Первая"], ["Вторая", "Нет категории"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Выберите вашу категорию:", reply_markup=reply_markup)
    return CATEGORY

async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["category"] = update.message.text
    keyboard = [["Да", "Нет"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Ваша работа относится к зоне экологического неблагополучия?", reply_markup=reply_markup)
    return ZONE

async def zone(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    context.user_data["locality"] = update.message.text
    keyboard = [["Стационар", "Поликлиника"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Укажите тип медорганизации:", reply_markup=reply_markup)
    return ORG_TYPE

# Вопрос о хирургической должности
async def org_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["org_type"] = update.message.text

    # Вопрос о наличии вредности
    if "hazard_profile" not in context.user_data:
        keyboard = [["Да", "Нет"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(
            "Есть ли у вас вредные условия труда?",
            reply_markup=reply_markup
        )
        return UCHASTOK

    # Вопрос о хирургической должности для врача в стационаре
    if (
        context.user_data.get("specialty") == "Врач"
        and context.user_data.get("org_type") == "Стационар"
        and "is_surgery" not in context.user_data
    ):
        keyboard = [["Да", "Нет"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(
            "Ваша должность хирургическая?",
            reply_markup=reply_markup
        )
        return UCHASTOK

    # Вопрос о старшей медсестре для медсестры
    if (
        context.user_data.get("specialty") == "Медсестра"
        and "senior_nurse" not in context.user_data
    ):
        keyboard = [["Да", "Нет"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(
            "Вы являетесь старшей медсестрой?",
            reply_markup=reply_markup
        )
        return UCHASTOK

    # Уточняющий вопрос для медсестры в поликлинике
    if (
        context.user_data.get("specialty") == "Медсестра"
        and context.user_data.get("org_type") == "Поликлиника"
        and "is_uchastok" not in context.user_data
    ):
        keyboard = [["Да", "Нет"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(
            "Относится ли ваша должность к участковым специалистам?",
            reply_markup=reply_markup
        )
        return UCHASTOK

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
    summary = "\n".join([
        f"{param_names.get(k, k)}: {v}" for k, v in context.user_data.items() if k in param_names
    ])

    allowance_names = {
        "k1": "Экологическая зона",
        "k2": "Сельская местность",
        "k3": "Старшая медсестра",
        "k4": "Вредные условия",
        "k5": "Психоэмоц напряжение",
        "special": "Особые условия труда",
    }
    allowance_details = "\n".join([
        f"{allowance_names.get(k, k)}: {round(v, 2) if k == 'special' else v}" for k, v in allowances.items() if k in allowance_names
    ])

    await update.message.reply_text(
        f"Спасибо! Ваши параметры:\n{summary}\n\n"
        f"Должностной оклад: {base_oklad} KZT\n"
        f"Надбавки:\n{allowance_details}\n"
        f"\nРасчёт завершён!\nВаша зарплата: {total} KZT"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Диалог отменён.")
    return ConversationHandler.END

# Добавить обработку ответа на уточняющий вопрос
async def uchastok_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        return await org_type(update, context)
    elif "senior_nurse" not in context.user_data and context.user_data.get("specialty") == "Медсестра":
        context.user_data["senior_nurse"] = text == "Да"
    elif "is_uchastok" not in context.user_data and context.user_data.get("specialty") == "Медсестра" and context.user_data.get("org_type") == "Поликлиника":
        context.user_data["is_uchastok"] = text == "Да"
    return await org_type(update, context)

app = Application.builder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", start),
        MessageHandler(filters.Regex("^(Старт|старт)$") & ~filters.COMMAND, start)
    ],
    states={
        SPECIALTY: [MessageHandler(filters.TEXT & ~filters.COMMAND, specialty)],
        EDUCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, education)],
        EXPERIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, experience)],
        CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, category)],
        ZONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, zone)],
        LOCALITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, locality)],
        ORG_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, org_type)],
        UCHASTOK: [MessageHandler(filters.TEXT & ~filters.COMMAND, uchastok_handler)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(conv_handler)
app.run_polling()