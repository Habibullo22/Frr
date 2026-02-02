# -*- coding: utf-8 -*-
import telebot
from telebot import types
import json
import os
import time

# ================== CONFIG ==================
BOT_TOKEN = "7320532115:AAGqzrL7pM_wnBVxT0zU_Z_9JdcTLEG7rqM"
ADMIN_ID = 5815294733
CARD_NUMBER = "9860 6067 5024 7151"
DATA_FILE = "bot_data.json"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# ================== I18N (UZ/RU/EN) ==================
T = {
    "uz": {
        "choose_lang": "🌐 Tilni tanlang:",
        "need_contact": "📲 Davom etish uchun kontakt ulashing.",
        "share_contact_btn": "📞 Kontakt ulashish",
        "contact_saved": "✅ Kontakt saqlandi!\nAsosiy menyu:",
        "menu_title": "🏠 Asosiy menyu:",
        "btn_buy": "💎 Almaz/Voucher olish",
        "btn_balance": "💰 Balans",
        "btn_deposit": "➕ Balans to‘ldirish",
        "btn_orders": "📦 Buyurtmalarim",
        "btn_ref": "👥 Referal",
        "btn_help": "ℹ️ Yordam",
        "btn_back": "⬅️ Ortga",
        "balance_text": "💰 Balansingiz: <b>{bal}</b> so‘m",
        "select_package": "🛒 Paketni tanlang:",
        "send_ffid": "✍️ Free Fire ID ni yuboring (faqat raqam):",
        "invalid_ffid": "❌ FF ID noto‘g‘ri. Qayta yuboring (kamida 6 ta raqam).",
        "order_created": "✅ Buyurtma yaratildi!\n📦 Paket: <b>{pkg}</b>\n🆔 Order: <b>#{oid}</b>\n⏳ Admin tekshiradi.",
        "orders_empty": "📦 Sizda buyurtmalar yo‘q.",
        "orders_list_title": "📦 Buyurtmalar ro‘yxati:",
        "deposit_enter_amount": "➕ To‘ldirish summasini yuboring (so‘m):",
        "deposit_invalid": "❌ Noto‘g‘ri summa. Masalan: 10000",
        "deposit_req_sent": "✅ So‘rov yuborildi!\n💳 Karta: <code>{card}</code>\n💰 Summa: <b>{amt}</b> so‘m\n⏳ Admin tasdiqlaydi.",
        "help_text": "ℹ️ Yordam:\n- Paket tanlab FF ID yuborasiz\n- Admin tasdiqlasa buyurtma bajariladi\n- Rad bo‘lsa pul balansga qaytariladi",
        "ref_text": "👥 Referal havolangiz:\n<code>{link}</code>\nTaklif qilganlar: <b>{cnt}</b> ta",
        "only_admin": "❌ Siz admin emassiz!",
        "approved": "✅ Tasdiqlandi.",
        "rejected": "❌ Rad etildi.",
        "already_done": "⚠️ Bu so‘rov allaqachon ishlangan.",
        "admin_new_order": "🆕 <b>Yangi buyurtma</b>\n👤 User: <b>{name}</b> (<code>{uid}</code>)\n📞 Tel: <code>{phone}</code>\n📦 Paket: <b>{pkg}</b>\n🎮 FF ID: <code>{ffid}</code>\n🆔 Order: <b>#{oid}</b>\n🕒 {dt}",
        "admin_new_deposit": "🆕 <b>Balans to‘ldirish so‘rovi</b>\n👤 User: <b>{name}</b> (<code>{uid}</code>)\n📞 Tel: <code>{phone}</code>\n💰 Summa: <b>{amt}</b> so‘m\n🆔 DepID: <b>D{did}</b>\n🕒 {dt}",
        "user_order_done": "✅ Buyurtmangiz bajarildi!\n📦 {pkg}\n🆔 #{oid}",
        "user_order_reject": "❌ Buyurtmangiz rad etildi.\n💰 {refund} so‘m balansingizga qaytarildi.\n🆔 #{oid}",
        "user_deposit_ok": "✅ Balansingiz to‘ldirildi: <b>+{amt}</b> so‘m\n💰 Yangi balans: <b>{bal}</b> so‘m",
        "user_deposit_reject": "❌ To‘ldirish rad etildi.\n🆔 DepID: D{did}"
    },
    "ru": {
        "choose_lang": "🌐 Выберите язык:",
        "need_contact": "📲 Чтобы продолжить — поделитесь контактом.",
        "share_contact_btn": "📞 Поделиться контактом",
        "contact_saved": "✅ Контакт сохранён!\nГлавное меню:",
        "menu_title": "🏠 Главное меню:",
        "btn_buy": "💎 Купить алмазы/ваучер",
        "btn_balance": "💰 Баланс",
        "btn_deposit": "➕ Пополнить баланс",
        "btn_orders": "📦 Мои заказы",
        "btn_ref": "👥 Рефералы",
        "btn_help": "ℹ️ Помощь",
        "btn_back": "⬅️ Назад",
        "balance_text": "💰 Ваш баланс: <b>{bal}</b> сум",
        "select_package": "🛒 Выберите пакет:",
        "send_ffid": "✍️ Отправьте Free Fire ID (только цифры):",
        "invalid_ffid": "❌ Неверный FF ID. Отправьте снова (минимум 6 цифр).",
        "order_created": "✅ Заказ создан!\n📦 Пакет: <b>{pkg}</b>\n🆔 Заказ: <b>#{oid}</b>\n⏳ Ожидайте подтверждения администратора.",
        "orders_empty": "📦 У вас нет заказов.",
        "orders_list_title": "📦 Список заказов:",
        "deposit_enter_amount": "➕ Отправьте сумму пополнения (сум):",
        "deposit_invalid": "❌ Неверная сумма. Пример: 10000",
        "deposit_req_sent": "✅ Запрос отправлен!\n💳 Карта: <code>{card}</code>\n💰 Сумма: <b>{amt}</b> сум\n⏳ Админ подтвердит.",
        "help_text": "ℹ️ Помощь:\n- Выбираете пакет и отправляете FF ID\n- Если админ подтвердит — заказ выполнится\n- Если отклонит — деньги вернутся на баланс",
        "ref_text": "👥 Ваша реф-ссылка:\n<code>{link}</code>\nПриглашено: <b>{cnt}</b>",
        "only_admin": "❌ Вы не админ!",
        "approved": "✅ Подтверждено.",
        "rejected": "❌ Отклонено.",
        "already_done": "⚠️ Уже обработано.",
        "admin_new_order": "🆕 <b>Новый заказ</b>\n👤 User: <b>{name}</b> (<code>{uid}</code>)\n📞 Tel: <code>{phone}</code>\n📦 Пакет: <b>{pkg}</b>\n🎮 FF ID: <code>{ffid}</code>\n🆔 Заказ: <b>#{oid}</b>\n🕒 {dt}",
        "admin_new_deposit": "🆕 <b>Запрос пополнения</b>\n👤 User: <b>{name}</b> (<code>{uid}</code>)\n📞 Tel: <code>{phone}</code>\n💰 Сумма: <b>{amt}</b> сум\n🆔 DepID: <b>D{did}</b>\n🕒 {dt}",
        "user_order_done": "✅ Заказ выполнен!\n📦 {pkg}\n🆔 #{oid}",
        "user_order_reject": "❌ Заказ отклонён.\n💰 {refund} сум возвращены на баланс.\n🆔 #{oid}",
        "user_deposit_ok": "✅ Баланс пополнен: <b>+{amt}</b> сум\n💰 Новый баланс: <b>{bal}</b> сум",
        "user_deposit_reject": "❌ Пополнение отклонено.\n🆔 DepID: D{did}"
    },
    "en": {
        "choose_lang": "🌐 Choose language:",
        "need_contact": "📲 To continue, please share your contact.",
        "share_contact_btn": "📞 Share contact",
        "contact_saved": "✅ Contact saved!\nMain menu:",
        "menu_title": "🏠 Main menu:",
        "btn_buy": "💎 Buy diamonds/voucher",
        "btn_balance": "💰 Balance",
        "btn_deposit": "➕ Top up balance",
        "btn_orders": "📦 My orders",
        "btn_ref": "👥 Referral",
        "btn_help": "ℹ️ Help",
        "btn_back": "⬅️ Back",
        "balance_text": "💰 Your balance: <b>{bal}</b> UZS",
        "select_package": "🛒 Choose a package:",
        "send_ffid": "✍️ Send your Free Fire ID (digits only):",
        "invalid_ffid": "❌ Invalid FF ID. Try again (min 6 digits).",
        "order_created": "✅ Order created!\n📦 Package: <b>{pkg}</b>\n🆔 Order: <b>#{oid}</b>\n⏳ Waiting for admin review.",
        "orders_empty": "📦 You have no orders.",
        "orders_list_title": "📦 Orders list:",
        "deposit_enter_amount": "➕ Send top-up amount (UZS):",
        "deposit_invalid": "❌ Invalid amount. Example: 10000",
        "deposit_req_sent": "✅ Request sent!\n💳 Card: <code>{card}</code>\n💰 Amount: <b>{amt}</b> UZS\n⏳ Admin will confirm.",
        "help_text": "ℹ️ Help:\n- Choose a package and send FF ID\n- If approved, order is completed\n- If rejected, money is refunded to your balance",
        "ref_text": "👥 Your referral link:\n<code>{link}</code>\nInvited: <b>{cnt}</b>",
        "only_admin": "❌ You are not admin!",
        "approved": "✅ Approved.",
        "rejected": "❌ Rejected.",
        "already_done": "⚠️ Already processed.",
        "admin_new_order": "🆕 <b>New order</b>\n👤 User: <b>{name}</b> (<code>{uid}</code>)\n📞 Tel: <code>{phone}</code>\n📦 Package: <b>{pkg}</b>\n🎮 FF ID: <code>{ffid}</code>\n🆔 Order: <b>#{oid}</b>\n🕒 {dt}",
        "admin_new_deposit": "🆕 <b>Top-up request</b>\n👤 User: <b>{name}</b> (<code>{uid}</code>)\n📞 Tel: <code>{phone}</code>\n💰 Amount: <b>{amt}</b> UZS\n🆔 DepID: <b>D{did}</b>\n🕒 {dt}",
        "user_order_done": "✅ Your order is completed!\n📦 {pkg}\n🆔 #{oid}",
        "user_order_reject": "❌ Order rejected.\n💰 Refunded: {refund} UZS\n🆔 #{oid}",
        "user_deposit_ok": "✅ Balance topped up: <b>+{amt}</b> UZS\n💰 New balance: <b>{bal}</b> UZS",
        "user_deposit_reject": "❌ Top-up rejected.\n🆔 DepID: D{did}"
    }
}

def tr(uid, key, **kwargs):
    u = ensure_user(uid)
    lang = u.get("lang", "uz")
    s = T.get(lang, T["uz"]).get(key, key)
    return s.format(**kwargs)

# ================== PACKAGES ==================
voucher_packages = {
    "💳 Haftalik Lite [90💎] – 9,000 so‘m": 9000,
    "💳 Haftalik [450💎] – 21,000 so‘m": 21000,
    "💳 Oylik [2600💎] – 135,000 so‘m": 135000,
    "💎 LvL Up [1270💎] – 67,000 so‘m": 67000
}

# ================== DATA LOAD/SAVE ==================
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                d = json.load(f)
                return d.get("users", {}), d.get("orders", {}), d.get("deposits", {}), d.get("state", {})
        except Exception as e:
            print("Data load error:", e)
    return {}, {}, {}, {}

def save_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "users": users,
                "orders": orders,
                "deposits": deposits,
                "state": state
            }, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Data save error:", e)

users, orders, deposits, state = load_data()

# ================== HELPERS ==================
def ensure_user(user_id):
    uid = str(user_id)
    if uid not in users:
        users[uid] = {
            "balance": 0,
            "lang": None,
            "phone": None,
            "name": None,
            "created_at": int(time.time()),
            "ref_by": None,
            "referrals": []
        }
        save_data()
    # ensure fields exist
    u = users[uid]
    u.setdefault("balance", 0)
    u.setdefault("lang", None)
    u.setdefault("phone", None)
    u.setdefault("name", None)
    u.setdefault("ref_by", None)
    u.setdefault("referrals", [])
    return u

def set_state(user_id, step=None, payload=None):
    uid = str(user_id)
    if step is None:
        state.pop(uid, None)
    else:
        state[uid] = {"step": step, "payload": payload or {}}
    save_data()

def get_state(user_id):
    return state.get(str(user_id))

def now_text():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def next_order_id(user_id):
    uid = str(user_id)
    if uid not in orders:
        orders[uid] = []
    return len(orders[uid]) + 1

def next_deposit_id():
    # global increasing by counting all deposits
    return sum(len(v) for v in deposits.values()) + 1

def find_order(user_id, order_id):
    uid = str(user_id)
    for o in orders.get(uid, []):
        if o.get("order_id") == order_id:
            return o
    return None

def find_deposit(user_id, dep_id):
    uid = str(user_id)
    for d in deposits.get(uid, []):
        if d.get("dep_id") == dep_id:
            return d
    return None

# ================== KEYBOARDS ==================
def lang_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("🇺🇿 O‘zbek", callback_data="lang_uz"),
        types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        types.InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
    )
    return kb

def contact_kb(user_id):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = types.KeyboardButton(tr(user_id, "share_contact_btn"), request_contact=True)
    kb.add(btn)
    return kb

def main_menu(user_id):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(tr(user_id, "btn_buy"), tr(user_id, "btn_balance"))
    kb.row(tr(user_id, "btn_deposit"), tr(user_id, "btn_orders"))
    kb.row(tr(user_id, "btn_ref"), tr(user_id, "btn_help"))
    return kb

def back_kb(user_id):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(tr(user_id, "btn_back"))
    return kb

def packages_kb():
    kb = types.InlineKeyboardMarkup()
    for name in voucher_packages.keys():
        kb.add(types.InlineKeyboardButton(name, callback_data=f"pkg|{name}"))
    return kb

def admin_order_kb(uid, oid):
    kb = types.InlineKeyboardMarkup()
    kb.row(
        types.InlineKeyboardButton("✅ Confirm", callback_data=f"ord_ok|{uid}|{oid}"),
        types.InlineKeyboardButton("❌ Reject", callback_data=f"ord_no|{uid}|{oid}")
    )
    return kb

def admin_deposit_kb(uid, did, amt):
    kb = types.InlineKeyboardMarkup()
    kb.row(
        types.InlineKeyboardButton("✅ Confirm", callback_data=f"dep_ok|{uid}|{did}|{amt}"),
        types.InlineKeyboardButton("❌ Reject", callback_data=f"dep_no|{uid}|{did}")
    )
    return kb

# ================== START / LANGUAGE / CONTACT ==================
@bot.message_handler(commands=["start"])
def cmd_start(message):
    uid = message.from_user.id
    u = ensure_user(uid)
    u["name"] = (message.from_user.first_name or "")[:64]
    save_data()

    # referral
    # /start ref_123
    parts = (message.text or "").split()
    if len(parts) > 1 and parts[1].startswith("ref_"):
        ref_id = parts[1].replace("ref_", "").strip()
        if ref_id.isdigit() and ref_id != str(uid):
            if u.get("ref_by") is None:
                u["ref_by"] = ref_id
                # add to ref owner's referrals
                ensure_user(ref_id)
                if str(uid) not in users[str(ref_id)]["referrals"]:
                    users[str(ref_id)]["referrals"].append(str(uid))
                save_data()

    # language flow
    if not u.get("lang"):
        bot.send_message(uid, "🌐 Choose language / Выберите язык / Tilni tanlang:", reply_markup=lang_kb())
        return

    # contact flow
    if not u.get("phone"):
        bot.send_message(uid, tr(uid, "need_contact"), reply_markup=contact_kb(uid))
        return

    bot.send_message(uid, tr(uid, "menu_title"), reply_markup=main_menu(uid))

@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def on_lang(call):
    uid = call.from_user.id
    ensure_user(uid)
    lang = call.data.split("_", 1)[1]
    if lang not in ("uz", "ru", "en"):
        lang = "uz"
    users[str(uid)]["lang"] = lang
    save_data()

    bot.answer_callback_query(call.id, "OK")
    # ask contact
    bot.send_message(uid, tr(uid, "need_contact"), reply_markup=contact_kb(uid))

@bot.message_handler(content_types=["contact"])
def on_contact(message):
    uid = message.from_user.id
    u = ensure_user(uid)

    # only accept user's own contact (security)
    if not message.contact or message.contact.user_id != uid:
        bot.send_message(uid, "❌ Iltimos, o‘zingizning kontaktingizni yuboring.")
        return

    phone = message.contact.phone_number
    u["phone"] = phone
    u["name"] = (message.from_user.first_name or "")[:64]
    save_data()

    bot.send_message(uid, tr(uid, "contact_saved"), reply_markup=main_menu(uid))

# ================== MENU HANDLERS ==================
@bot.message_handler(func=lambda m: True)
def on_text(message):
    uid = message.from_user.id
    u = ensure_user(uid)

    # must have lang + contact first
    if not u.get("lang"):
        bot.send_message(uid, "🌐 Choose language / Выберите язык / Tilni tanlang:", reply_markup=lang_kb())
        return
    if not u.get("phone"):
        bot.send_message(uid, tr(uid, "need_contact"), reply_markup=contact_kb(uid))
        return

    st = get_state(uid)

    # state steps
    if st:
        step = st.get("step")
        payload = st.get("payload", {})

        if step == "WAIT_FF_ID":
            ffid = (message.text or "").strip()
            if not (ffid.isdigit() and len(ffid) >= 6):
                bot.send_message(uid, tr(uid, "invalid_ffid"))
                return

            pkg = payload.get("package")
            price = voucher_packages.get(pkg, 0)

            # create order
            oid = next_order_id(uid)
            orders.setdefault(str(uid), []).append({
                "order_id": oid,
                "ff_id": ffid,
                "package": pkg,
                "price": price,
                "status": "Kutilmoqda",
                "created_at": int(time.time())
            })
            save_data()
            set_state(uid, None)

            bot.send_message(uid, tr(uid, "order_created", pkg=pkg, oid=oid), reply_markup=main_menu(uid))

            # send to admin
            phone = users[str(uid)].get("phone") or "—"
            name = users[str(uid)].get("name") or "—"
            txt = tr(uid, "admin_new_order", name=name, uid=uid, phone=phone, pkg=pkg, ffid=ffid, oid=oid, dt=now_text())
            bot.send_message(ADMIN_ID, txt, reply_markup=admin_order_kb(uid, oid))
            return

        if step == "WAIT_DEPOSIT_AMOUNT":
            raw = (message.text or "").replace(" ", "").replace(",", "")
            if not raw.isdigit():
                bot.send_message(uid, tr(uid, "deposit_invalid"))
                return
            amt = int(raw)
            if amt < 1000:
                bot.send_message(uid, tr(uid, "deposit_invalid"))
                return

            did = next_deposit_id()
            deposits.setdefault(str(uid), []).append({
                "dep_id": did,
                "amount": amt,
                "status": "Kutilmoqda",
                "created_at": int(time.time())
            })
            save_data()
            set_state(uid, None)

            bot.send_message(uid, tr(uid, "deposit_req_sent", card=CARD_NUMBER, amt=amt), reply_markup=main_menu(uid))

            phone = users[str(uid)].get("phone") or "—"
            name = users[str(uid)].get("name") or "—"
            txt = tr(uid, "admin_new_deposit", name=name, uid=uid, phone=phone, amt=amt, did=did, dt=now_text())
            bot.send_message(ADMIN_ID, txt, reply_markup=admin_deposit_kb(uid, did, amt))
            return

    # main menu actions
    text = (message.text or "").strip()

    if text == tr(uid, "btn_balance"):
        bot.send_message(uid, tr(uid, "balance_text", bal=u.get("balance", 0)))
        return

    if text == tr(uid, "btn_buy"):
        bot.send_message(uid, tr(uid, "select_package"), reply_markup=packages_kb())
        return

    if text == tr(uid, "btn_deposit"):
        set_state(uid, "WAIT_DEPOSIT_AMOUNT")
        bot.send_message(uid, tr(uid, "deposit_enter_amount"), reply_markup=back_kb(uid))
        return

    if text == tr(uid, "btn_orders"):
        my = orders.get(str(uid), [])
        if not my:
            bot.send_message(uid, tr(uid, "orders_empty"))
            return
        lines = [tr(uid, "orders_list_title")]
        for o in my[-10:]:
            lines.append(f"• #{o['order_id']} | {o['status']} | {o['package']}")
        bot.send_message(uid, "\n".join(lines))
        return

    if text == tr(uid, "btn_ref"):
        link = f"https://t.me/{bot.get_me().username}?start=ref_{uid}"
        cnt = len(u.get("referrals", []))
        bot.send_message(uid, tr(uid, "ref_text", link=link, cnt=cnt))
        return

    if text == tr(uid, "btn_help"):
        bot.send_message(uid, tr(uid, "help_text"))
        return

    if text == tr(uid, "btn_back"):
        set_state(uid, None)
        bot.send_message(uid, tr(uid, "menu_title"), reply_markup=main_menu(uid))
        return

    # default
    bot.send_message(uid, tr(uid, "menu_title"), reply_markup=main_menu(uid))

# ================== PACKAGE SELECT (INLINE) ==================
@bot.callback_query_handler(func=lambda call: call.data.startswith("pkg|"))
def on_package(call):
    uid = call.from_user.id
    ensure_user(uid)

    pkg = call.data.split("|", 1)[1]
    if pkg not in voucher_packages:
        bot.answer_callback_query(call.id, "Package not found")
        return

    set_state(uid, "WAIT_FF_ID", {"package": pkg})
    bot.answer_callback_query(call.id, "OK")
    bot.send_message(uid, tr(uid, "send_ffid"), reply_markup=back_kb(uid))

# ================== ADMIN: ORDER CONFIRM/REJECT ==================
@bot.callback_query_handler(func=lambda call: call.data.startswith("ord_ok|") or call.data.startswith("ord_no|"))
def admin_order_action(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, T["uz"]["only_admin"])
        return

    parts = call.data.split("|")
    action = parts[0]      # ord_ok / ord_no
    uid = parts[1]
    oid = int(parts[2])

    order = find_order(uid, oid)
    if not order:
        bot.answer_callback_query(call.id, "Order not found")
        return

    if order["status"] in ("Bajarildi", "Rad etildi"):
        bot.answer_callback_query(call.id, T["uz"]["already_done"])
        return

    ensure_user(uid)
    user_lang = users[str(uid)].get("lang") or "uz"

    if action == "ord_ok":
        order["status"] = "Bajarildi"
        save_data()
        bot.answer_callback_query(call.id, T["uz"]["approved"])
        bot.send_message(int(uid), T[user_lang]["user_order_done"].format(pkg=order["package"], oid=oid))
    else:
        order["status"] = "Rad etildi"
        refund = int(order.get("price", 0))
        users[str(uid)]["balance"] = int(users[str(uid)].get("balance", 0)) + refund
        save_data()
        bot.answer_callback_query(call.id, T["uz"]["rejected"])
        bot.send_message(int(uid), T[user_lang]["user_order_reject"].format(refund=refund, oid=oid))

# ================== ADMIN: DEPOSIT CONFIRM/REJECT ==================
@bot.callback_query_handler(func=lambda call: call.data.startswith("dep_ok|") or call.data.startswith("dep_no|"))
def admin_deposit_action(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, T["uz"]["only_admin"])
        return

    parts = call.data.split("|")
    action = parts[0]   # dep_ok / dep_no
    uid = parts[1]
    did = int(parts[2])

    ensure_user(uid)
    user_lang = users[str(uid)].get("lang") or "uz"

    dep = find_deposit(uid, did)
    if not dep:
        bot.answer_callback_query(call.id, "Deposit not found")
        return

    if dep["status"] in ("Bajarildi", "Rad etildi"):
        bot.answer_callback_query(call.id, T["uz"]["already_done"])
        return

    if action == "dep_ok":
        amt = int(dep.get("amount", 0))
        dep["status"] = "Bajarildi"
        users[str(uid)]["balance"] = int(users[str(uid)].get("balance", 0)) + amt
        save_data()
        bot.answer_callback_query(call.id, T["uz"]["approved"])
        bot.send_message(int(uid), T[user_lang]["user_deposit_ok"].format(amt=amt, bal=users[str(uid)]["balance"]))
    else:
        dep["status"] = "Rad etildi"
        save_data()
        bot.answer_callback_query(call.id, T["uz"]["rejected"])
        bot.send_message(int(uid), T[user_lang]["user_deposit_reject"].format(did=did))

# ================== ADMIN COMMANDS ==================
@bot.message_handler(commands=["addbal"])
def admin_addbal(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, T["uz"]["only_admin"])
        return
    # /addbal user_id amount
    parts = (message.text or "").split()
    if len(parts) != 3 or (not parts[1].isdigit()) or (not parts[2].isdigit()):
        bot.reply_to(message, "Usage: /addbal <user_id> <amount>")
        return
    uid = parts[1]
    amt = int(parts[2])
    ensure_user(uid)
    users[str(uid)]["balance"] = int(users[str(uid)].get("balance", 0)) + amt
    save_data()
    bot.reply_to(message, f"✅ Added +{amt} to {uid}. New balance: {users[str(uid)]['balance']}")

@bot.message_handler(commands=["user"])
def admin_user(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, T["uz"]["only_admin"])
        return
    parts = (message.text or "").split()
    if len(parts) != 2 or not parts[1].isdigit():
        bot.reply_to(message, "Usage: /user <user_id>")
        return
    uid = parts[1]
    u = ensure_user(uid)
    bot.reply_to(message, json.dumps(u, ensure_ascii=False, indent=2))

# ================== RUN ==================
print("🤖 Bot ishga tushdi...")
bot.infinity_polling(skip_pending=True)
