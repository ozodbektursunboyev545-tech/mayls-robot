"""
╔══════════════════════════════════════════════════════════╗
║           PROFESSIONAL ADMIN INBOX BOT                   ║
║     Barcha xabarlar maxfiy — faqat admin ko'radi         ║
╚══════════════════════════════════════════════════════════╝

SOZLASH:
  1. @BotFather dan bot yarating va TOKEN oling
  2. Pastdagi BOT_TOKEN va ADMIN_ID ni to'ldiring
  3. pip install pyTelegramBotAPI
  4. python admin_bot.py

TOPISH: @userinfobot ga /start yozing — u sizning ID ingizni beradi
"""

import telebot
from telebot import types
from datetime import datetime

# ──────────────────────────────────────────────
#  ⚙️  SOZLAMALAR — faqat shu ikkitasini o'zgartiring
# ──────────────────────────────────────────────
BOT_TOKEN  = "8940311623:AAGRMmlqNIFjjQVRKIDg6B6BkDIhs_OFM9c"   # @BotFather dan olingan token
ADMIN_ID   = 7594436413                   # Sizning Telegram ID ingiz (raqam)

BOT_NAME   = "Mayls ROBOT"                 # Botingiz nomi (xohlagan narsa)
# ──────────────────────────────────────────────

bot = telebot.TeleBot(BOT_TOKEN)

# Suhbatlarni saqlash: {user_id: chat_history}
conversations: dict[int, list] = {}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  YORDAMCHI FUNKSIYALAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def user_info(user: types.User) -> str:
    """Foydalanuvchi haqida chiroyli matn."""
    name = user.first_name or ""
    if user.last_name:
        name += f" {user.last_name}"
    username = f"@{user.username}" if user.username else "username yo'q"
    return f"{name} ({username}) [ID: {user.id}]"


def now() -> str:
    return datetime.now().strftime("%H:%M · %d.%m.%Y")


def reply_keyboard(user_id: int) -> types.InlineKeyboardMarkup:
    """Admin uchun 'Javob berish' tugmasi."""
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        "✍️ Javob berish",
        callback_data=f"reply_{user_id}"
    ))
    return kb


def back_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel"))
    return kb


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  FOYDALANUVCHI TOMONIDA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@bot.message_handler(commands=["start"])
def handle_start(msg: types.Message):
    if msg.from_user.id == ADMIN_ID:
        bot.send_message(msg.chat.id,
            "👋 *Admin panelga xush kelibsiz!*\n\n"
            "Foydalanuvchilar yozganida siz bu yerda ko'rasiz.\n"
            "Javob berish uchun kerakli xabardagi `✍️ Javob berish` tugmasini bosing.",
            parse_mode="Markdown"
        )
        return

    # Oddiy foydalanuvchi uchun chiroyli xush kelibsiz xabari
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("📩 Xabar yuborish"))

    bot.send_message(msg.chat.id,
        f"*Assalomu alaykum!* 👋\n\n"
        f"Siz *{BOT_NAME}* ga murojaat qildingiz.\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"Xabaringizni yozing — admin imkon qadar tez javob beradi.\n"
        f"Barcha muloqotlaringiz *maxfiy* va faqat admin ko'radi.\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"💬 _Pastga xabaringizni yozing yoki yuborish tugmasini bosing._",
        parse_mode="Markdown",
        reply_markup=kb
    )


@bot.message_handler(func=lambda m: m.from_user.id != ADMIN_ID)
def handle_user_message(msg: types.Message):
    user = msg.from_user

    # Xabarni saqla
    if user.id not in conversations:
        conversations[user.id] = []
    conversations[user.id].append({
        "from": "user",
        "text": msg.text or "[media]",
        "time": now()
    })

    # ── Adminga bildirish ──
    header = (
        f"📨 *Yangi xabar*\n"
        f"👤 {user_info(user)}\n"
        f"🕐 {now()}\n"
        f"─────────────────────\n"
    )
    body = msg.text or ""

    # Media fayllarni ham adminga yuborish
    if msg.photo:
        bot.send_photo(ADMIN_ID, msg.photo[-1].file_id,
                       caption=header + (msg.caption or ""),
                       parse_mode="Markdown",
                       reply_markup=reply_keyboard(user.id))
    elif msg.video:
        bot.send_video(ADMIN_ID, msg.video.file_id,
                       caption=header + (msg.caption or ""),
                       parse_mode="Markdown",
                       reply_markup=reply_keyboard(user.id))
    elif msg.document:
        bot.send_document(ADMIN_ID, msg.document.file_id,
                          caption=header + (msg.caption or ""),
                          parse_mode="Markdown",
                          reply_markup=reply_keyboard(user.id))
    elif msg.voice:
        bot.send_voice(ADMIN_ID, msg.voice.file_id,
                       caption=header,
                       parse_mode="Markdown",
                       reply_markup=reply_keyboard(user.id))
    elif msg.sticker:
        bot.send_message(ADMIN_ID, header + "🎭 Sticker yubordi",
                         parse_mode="Markdown",
                         reply_markup=reply_keyboard(user.id))
        bot.send_sticker(ADMIN_ID, msg.sticker.file_id)
    else:
        bot.send_message(ADMIN_ID,
                         header + body,
                         parse_mode="Markdown",
                         reply_markup=reply_keyboard(user.id))

    # ── Foydalanuvchiga tasdiqlash ──
    bot.send_message(msg.chat.id,
        "✅ *Xabaringiz adminga yuborildi.*\n"
        "_Tez orada javob beriladi — sabr qiling!_ 🙏",
        parse_mode="Markdown"
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ADMIN TOMONIDA — JAVOB BERISH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Adminga kim bilan gaplashayotganini saqlash
admin_replying_to: dict[int, int] = {}  # {admin_id: target_user_id}


@bot.callback_query_handler(func=lambda c: c.data.startswith("reply_"))
def on_reply_button(call: types.CallbackQuery):
    if call.from_user.id != ADMIN_ID:
        return
    target_id = int(call.data.split("_")[1])
    admin_replying_to[ADMIN_ID] = target_id

    bot.answer_callback_query(call.id)
    bot.send_message(ADMIN_ID,
        f"✍️ *Javob yozyapsiz:*\n"
        f"Qabul qiluvchi: `{target_id}`\n\n"
        f"Javobingizni yozing 👇",
        parse_mode="Markdown",
        reply_markup=back_keyboard()
    )


@bot.callback_query_handler(func=lambda c: c.data == "cancel")
def on_cancel(call: types.CallbackQuery):
    if call.from_user.id == ADMIN_ID:
        admin_replying_to.pop(ADMIN_ID, None)
        bot.answer_callback_query(call.id, "Bekor qilindi")
        bot.send_message(ADMIN_ID, "❌ Javob bekor qilindi.")


@bot.message_handler(
    func=lambda m: m.from_user.id == ADMIN_ID and ADMIN_ID in admin_replying_to
)
def handle_admin_reply(msg: types.Message):
    target_id = admin_replying_to.pop(ADMIN_ID)

    # Foydalanuvchiga javobni yuborish
    try:
        bot.send_message(target_id,
            f"💬 *Admin javob berdi:*\n"
            f"─────────────────────\n"
            f"{msg.text}",
            parse_mode="Markdown"
        )
        # Adminga tasdiq
        bot.send_message(ADMIN_ID,
            f"✅ Javob yetkazildi → `{target_id}`",
            parse_mode="Markdown"
        )
        # Suhbatni saqlash
        if target_id not in conversations:
            conversations[target_id] = []
        conversations[target_id].append({
            "from": "admin",
            "text": msg.text,
            "time": now()
        })
    except Exception as e:
        bot.send_message(ADMIN_ID,
            f"❗ Xabar yuborib bo'lmadi: {e}"
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ADMIN KOMANDALAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@bot.message_handler(commands=["users"], func=lambda m: m.from_user.id == ADMIN_ID)
def cmd_users(msg: types.Message):
    if not conversations:
        bot.send_message(ADMIN_ID, "📭 Hali hech kim murojaat qilmagan.")
        return
    text = f"👥 *Murojaat qilganlar ({len(conversations)} kishi):*\n\n"
    for uid, history in conversations.items():
        count = len([h for h in history if h["from"] == "user"])
        last = history[-1]["time"]
        text += f"• `{uid}` — {count} ta xabar · oxirgisi {last}\n"
    bot.send_message(ADMIN_ID, text, parse_mode="Markdown")


@bot.message_handler(commands=["broadcast"], func=lambda m: m.from_user.id == ADMIN_ID)
def cmd_broadcast(msg: types.Message):
    text = msg.text.replace("/broadcast", "").strip()
    if not text:
        bot.send_message(ADMIN_ID,
            "📢 Foydalanish: `/broadcast Hammaga xabar matni`",
            parse_mode="Markdown")
        return
    success = 0
    for uid in conversations:
        try:
            bot.send_message(uid,
                f"📢 *Admin xabari:*\n─────────────────────\n{text}",
                parse_mode="Markdown")
            success += 1
        except:
            pass
    bot.send_message(ADMIN_ID, f"✅ {success} ta foydalanuvchiga yuborildi.")


@bot.message_handler(commands=["help"], func=lambda m: m.from_user.id == ADMIN_ID)
def cmd_help(msg: types.Message):
    bot.send_message(ADMIN_ID,
        "*🛠 Admin komandalar:*\n\n"
        "`/users` — murojaat qilganlar ro'yxati\n"
        "`/broadcast [matn]` — hammaga xabar yuborish\n"
        "`/help` — bu yordam\n\n"
        "_Javob berish uchun xabardagi_ `✍️ Javob berish` _tugmasini bosing._",
        parse_mode="Markdown"
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ISHGA TUSHIRISH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    print("╔══════════════════════════════════════╗")
    print("║      Admin Inbox Bot — ISHGA TUSHDI  ║")
    print("╚══════════════════════════════════════╝")
    print(f"Admin ID: {ADMIN_ID}")
    print("To'xtatish uchun: Ctrl+C\n")
    bot.infinity_polling(timeout=30, long_polling_timeout=20)
