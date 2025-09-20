import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Запуск Telegram-бота...")
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
)

from src.calc.totals import calc_total

async def exit_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"exit_handler: user_id={update.effective_user.id if update.effective_user else None}, message={update.message.text if update.message else None}")
    if update.message:
        await update.message.reply_text("Диалог завершён. Для нового расчёта отправьте /start или 'старт'.")
    return ConversationHandler.END

SPECIALTY, EDUCATION, EXPERIENCE, CATEGORY, ZONE, LOCALITY, ORG_TYPE, CLINICAL_DEPT, UCHASTOK = range(9)

async def restart_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"restart_handler: user_id={update.effective_user.id if update.effective_user else None}, message={update.message.text if update.message else None}")
    if isinstance(context.user_data, dict):
        context.user_data.clear()
    keyboard = [["врач", "медсестра", "другое"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    if update.message:
        await update.message.reply_text(
        "Выберите вашу должность:",
        reply_markup=reply_markup
    )
    return SPECIALTY

async def specialty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"specialty: user_id={update.effective_user.id if update.effective_user else None}, message={update.message.text if update.message else None}")
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    context.user_data["specialty"] = str(update.message.text).strip().lower()
    import json
    with open("current_params.json", "w", encoding="utf-8") as f:
        json.dump(context.user_data, f, ensure_ascii=False, indent=2)
    if update.message and update.message.text and update.message.text.strip().lower() == "медсестра":
        keyboard = [["высшее", "среднее"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Укажите образование:", reply_markup=reply_markup)
        return EDUCATION
    elif update.message and update.message.text and update.message.text.strip().lower() == "врач":
        context.user_data["education"] = "высшее"
        await update.message.reply_text("Введите ваш опыт работы (лет):")
        return EXPERIENCE
    else:
        await update.message.reply_text("Пока поддерживаются только должности 'врач' и 'медсестра'.")
        return ConversationHandler.END

async def education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"education: user_id={update.effective_user.id if update.effective_user else None}, message={update.message.text if update.message else None}")
    if context.user_data and context.user_data.get("specialty") == "медсестра":
        if update.message and update.message.text:
            context.user_data["education"] = str(update.message.text).strip().lower()
    else:
        if context.user_data is not None:
            context.user_data["education"] = "—"
    import json
    with open("current_params.json", "w", encoding="utf-8") as f:
        json.dump(context.user_data, f, ensure_ascii=False, indent=2)
    if update.message:
        await update.message.reply_text("Введите ваш опыт работы (лет):")
    return EXPERIENCE

async def experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"experience: user_id={update.effective_user.id if update.effective_user else None}, message={update.message.text if update.message else None}")
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    context.user_data["experience"] = update.message.text
    import json
    with open("current_params.json", "w", encoding="utf-8") as f:
        json.dump(context.user_data, f, ensure_ascii=False, indent=2)
    keyboard = [["высшая", "первая"], ["вторая", "нет категории"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Выберите вашу категорию:", reply_markup=reply_markup)
    return CATEGORY

async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"category: user_id={update.effective_user.id if update.effective_user else None}, message={update.message.text if update.message else None}")
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    cat_text = str(update.message.text).strip().lower()
    cat_map = {
        "высшая": 1,
        "первая": 2,
        "вторая": 3,
        "нет категории": 4
    }
    context.user_data["category"] = cat_map.get(cat_text, cat_text)
    import json
    with open("current_params.json", "w", encoding="utf-8") as f:
        json.dump(context.user_data, f, ensure_ascii=False, indent=2)
    keyboard = [["да", "нет"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Ваша работа относится к зоне экологического неблагополучия?", reply_markup=reply_markup)
    return ZONE

async def zone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"zone: user_id={update.effective_user.id if update.effective_user else None}, message={update.message.text if update.message else None}")
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    import json
    with open("current_params.json", "w", encoding="utf-8") as f:
        json.dump(context.user_data, f, ensure_ascii=False, indent=2)
    if str(update.message.text).strip().lower() == "да":
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
    logger.info(f"locality: user_id={update.effective_user.id if update.effective_user else None}, message={update.message.text if update.message else None}")
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    context.user_data["locality"] = str(update.message.text).strip().lower()
    import json
    with open("current_params.json", "w", encoding="utf-8") as f:
        json.dump(context.user_data, f, ensure_ascii=False, indent=2)
    keyboard = [["стационар", "поликлиника"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Выберите тип медорганизации:", reply_markup=reply_markup)
    return ORG_TYPE

async def org_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"org_type: user_id={update.effective_user.id if update.effective_user else None}, message={update.message.text if update.message else None}")
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    org_type_value = str(update.message.text).strip().lower()
    valid_types = ["стационар", "поликлиника"]
    if org_type_value not in valid_types:
        keyboard = [["стационар", "поликлиника"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Пожалуйста, выберите тип медорганизации:", reply_markup=reply_markup)
        return ORG_TYPE

    context.user_data["org_type"] = org_type_value
    import json
    with open("current_params.json", "w", encoding="utf-8") as f:
        json.dump(context.user_data, f, ensure_ascii=False, indent=2)

    if org_type_value == "стационар":
        keyboard = [["клиническое", "неклиническое"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Вы работаете или будете работать в клиническом отделении?", reply_markup=reply_markup)
        return CLINICAL_DEPT
    elif org_type_value == "поликлиника":
        keyboard = [["да", "нет"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Вы участковый специалист?", reply_markup=reply_markup)
        return UCHASTOK
async def clinical_dept_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"clinical_dept_handler: user_id={update.effective_user.id if update.effective_user else None}, message={update.message.text if update.message else None}")
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}

    dept_text = update.message.text if update.message and update.message.text else ""
    dept = str(dept_text).strip().lower()
    context.user_data["clinical_dept"] = dept
    import json
    with open("current_params.json", "w", encoding="utf-8") as f:
        json.dump(context.user_data, f, ensure_ascii=False, indent=2)
    if dept == "клиническое":
        keyboard = [["да", "нет"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Ваша должность хирургическая?", reply_markup=reply_markup)
        return UCHASTOK
    # Неклиническое — сразу к расчёту, без вопроса о хирургии
    context.user_data["is_surgery"] = False
    # Передаём признак отделения в answers
    answers = {
        "role": str(context.user_data.get("specialty", "")).strip().lower(),
        "education": context.user_data.get("education"),
        "category": context.user_data.get("category"),
        "experience_years": context.user_data.get("experience"),
        "eco_zone": context.user_data.get("zone"),
        "location": context.user_data.get("locality"),
        "facility": str(context.user_data.get("org_type", "")).strip().lower(),
        "clinical_dept": dept,  # Явно передаём выбранный признак
        "hazard_profile": None,
        "is_surgery": False,
        "is_uchastok": context.user_data.get("is_uchastok", False),
    }
    # Если отделение неклиническое, k5=0, иначе расчёт по стандартной логике
    result = calc_total(answers)
    if dept == "неклиническое":
        result["allowances"]["k5"] = 0
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
        "clinical_dept": "отделение",
        "is_uchastok": "участковый специалист",
        "is_surgery": "хирургическая должность",
    }
    def surgery_ru(val):
        if val is None:
            return "нет"
        if isinstance(val, bool):
            return "да" if val else "нет"
        if str(val).strip().lower() in ["да", "true", "1"]:
            return "да"
        if str(val).strip().lower() in ["нет", "false", "0"]:
            return "нет"
        return str(val)
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
    # k5=0 если отделение неклиническое
    allowance_details = "\n".join([
        f"{allowance_names.get(k, k)}: {0 if k == 'k5' and dept == 'неклиническое' else (round(v, 2) if k == 'special' else v)}"
        for k, v in allowances.items()
        if k in allowance_names and not (k == "k3" and role == "врач")
    ])

    multipliers = ""
    role_mult_val = None
    if context.user_data.get("specialty") == "врач":
        role_mult_val = 3.42
    elif context.user_data.get("specialty") == "медсестра":
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

async def uchastok_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"uchastok_handler: user_id={update.effective_user.id if update.effective_user else None}, message={update.message.text if update.message else None}")
    if not update.message:
        return ConversationHandler.END
    if context.user_data is None:
        context.user_data = {}
    text = str(update.message.text).strip().lower() if update.message and update.message.text else ""
    import json
    with open("current_params.json", "w", encoding="utf-8") as f:
        json.dump(context.user_data, f, ensure_ascii=False, indent=2)

    # Для стационара — хирургия
    if context.user_data.get("org_type") == "стационар":
        context.user_data["is_surgery"] = text.strip().lower() == "да"
    # Для поликлиники — участковый
    elif context.user_data.get("org_type") == "поликлиника":
        context.user_data["is_uchastok"] = text.strip().lower() == "да"

    answers = {
        "role": str(context.user_data.get("specialty", "")).strip().lower(),
        "education": context.user_data.get("education"),
        "category": context.user_data.get("category"),
        "experience_years": context.user_data.get("experience"),
        "eco_zone": context.user_data.get("zone"),
        "location": context.user_data.get("locality"),
        "facility": str(context.user_data.get("org_type", "")).strip().lower(),
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
    }
    category_map = {
        1: "высшая",
        2: "первая",
        3: "вторая",
        4: "без категории"
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
        if k == "category":
            try:
                if v is not None and str(v).isdigit():
                    v = category_map.get(int(v), v)
            except Exception:
                pass
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
    org_type = context.user_data.get("org_type")
    is_uchastok = context.user_data.get("is_uchastok", False)
    # k5 для участковой медсестры поликлиники = 150% БДО
    allowance_details = []
    for k, v in allowances.items():
        if k == "k3" and role == "врач":
            continue
        if k == "k5" and role == "медсестра" and org_type == "поликлиника" and is_uchastok:
            v = round(base_oklad * 1.5, 2)
        elif k == "special":
            v = round(v, 2)
        allowance_details.append(f"{allowance_names.get(k, k)}: {v}")
    allowance_details = "\n".join(allowance_details)

    multipliers = ""
    role_mult_val = None
    if context.user_data.get("specialty") == "врач":
        role_mult_val = 3.42
    elif context.user_data.get("specialty") == "медсестра":
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

## --- Запуск приложения ---
import re
state_handlers = [
    (SPECIALTY, specialty),
    (EDUCATION, education),
    (EXPERIENCE, experience),
    (CATEGORY, category),
    (ZONE, zone),
    (LOCALITY, locality),
    (ORG_TYPE, org_type),
    (CLINICAL_DEPT, clinical_dept_handler),
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
app.run_polling(drop_pending_updates=True)