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
    keyboard = [["врач", "медсестра", "другое"]]
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
    context.user_data["specialty"] = str(update.message.text).strip().lower()
    if update.message.text.strip().lower() == "медсестра":
        keyboard = [["высшее", "среднее"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Укажите образование:", reply_markup=reply_markup)
        return EDUCATION
    elif update.message.text.strip().lower() == "врач":
        context.user_data["education"] = "высшее"
        await update.message.reply_text("Введите ваш опыт работы (лет):")
        return EXPERIENCE
    else:
        await update.message.reply_text("Пока поддерживаются только должности 'врач' и 'медсестра'.")
        return ConversationHandler.END

async def education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("specialty") == "медсестра":
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
    keyboard = [["высшая", "первая"], ["вторая", "нет категории"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Выберите вашу категорию:", reply_markup=reply_markup)
    return CATEGORY

async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    context.user_data["category"] = update.message.text
    keyboard = [["да", "нет"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Ваша работа относится к зоне экологического неблагополучия?", reply_markup=reply_markup)
    return ZONE

async def zone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    if update.message.text.strip().lower() == "да":
        zone_keyboard = [
            ["экол. катастрофы", "экол. кризиса"],
            ["экол. предкризис", "чрезвыч риск радиации"],
            ["максим риск радиации", "повыш риск радиации"],
            ["миним риск радиации", "льгот соц-экон статус"],
            ["нет"]
        ]
        reply_markup = ReplyKeyboardMarkup(zone_keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Уточните зону:", reply_markup=reply_markup)
        return ZONE
    else:
        context.user_data["zone"] = "нет"
        keyboard = [["город", "село"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Вы проживаете в городе или селе?", reply_markup=reply_markup)
        return LOCALITY

async def locality(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    context.user_data["locality"] = update.message.text
    keyboard = [["стационар", "поликлиника"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Выберите тип медорганизации:", reply_markup=reply_markup)
    return ORG_TYPE

async def org_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    org_type_value = update.message.text.strip().lower()
    valid_types = ["стационар", "поликлиника"]
    if org_type_value not in valid_types:
        keyboard = [["стационар", "поликлиника"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Пожалуйста, выберите тип медорганизации:", reply_markup=reply_markup)
        return ORG_TYPE

    context.user_data["org_type"] = org_type_value

    if org_type_value == "стационар":
        keyboard = [["да", "нет"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Ваша должность хирургическая?", reply_markup=reply_markup)
        return UCHASTOK
    else:
        keyboard = [["да", "нет"]]
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
    if context.user_data.get("org_type") == "стационар":
        context.user_data["is_surgery"] = text.strip().lower() == "да"
        # Для медсестры — вопрос о старшей медсестре
        if context.user_data.get("specialty") == "медсестра" and "senior_nurse" not in context.user_data:
            keyboard = [["да", "нет"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            await update.message.reply_text("Вы являетесь старшей медсестрой?", reply_markup=reply_markup)
            return UCHASTOK
    # Для поликлиники — участковый
    elif context.user_data.get("org_type") == "поликлиника":
        context.user_data["is_uchastok"] = text.strip().lower() == "да"
        # Для медсестры — вопрос о старшей медсестре
        if context.user_data.get("specialty") == "медсестра" and "senior_nurse" not in context.user_data:
            keyboard = [["да", "нет"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            await update.message.reply_text("Вы являетесь старшей медсестрой?", reply_markup=reply_markup)
            return UCHASTOK
    # Для медсестры — старшая медсестра
    elif context.user_data.get("specialty") == "медсестра" and "senior_nurse" not in context.user_data:
        context.user_data["senior_nurse"] = text.strip().lower() == "да"
    # Все параметры собраны — финальный расчёт
    answers = {
        "role": str(context.user_data.get("specialty", "")).strip().lower(),
        "education": context.user_data.get("education"),
        "category": context.user_data.get("category"),
        "experience_years": context.user_data.get("experience"),
        "eco_zone": context.user_data.get("zone"),
        "location": context.user_data.get("locality"),
        "facility": str(context.user_data.get("org_type", "")).strip().lower(),
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
    role = context.user_data.get("specialty")
    allowance_details = "\n".join([
        f"{allowance_names.get(k, k)}: {round(v, 2) if k == 'special' else v}"
        for k, v in allowances.items()
        if k in allowance_names and not (k == "k3" and role == "Врач")
    ])

    multipliers = ""
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
    if update.message:
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