from fastapi import FastAPI, Request
import telegram
import os
import asyncio

# Отримання токена з змінної середовища
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Токен не знайдено! Встановіть змінну BOT_TOKEN.")

# Ініціалізація бота
bot = telegram.Bot(token=TOKEN)
app = FastAPI()

# Ендпоінт для обробки оновлень від Telegram
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "").lower()

        # Асинхронна відправка повідомлень
        loop = asyncio.get_event_loop()
        if text == "/start":
            await loop.run_in_executor(None, bot.send_message, chat_id, "Привіт! Я — Шеф-бот 🤖👨‍🍳")
        elif text == "/menu":
            await loop.run_in_executor(None, bot.send_message, chat_id, "Меню: 1) Борщ /borsch, 2) Плов /plov")
        elif text == "/borsch":
            await loop.run_in_executor(None, bot.send_message, chat_id, "Рецепт борща: 500 г яловичини, 2 буряки, 200 г капусти, 3 картоплини, 1 морква, 1 цибулина, 2 ст. л. томатної пасти. Вари 2 години, подавай зі сметаною!")
        elif text == "/plov":
            await loop.run_in_executor(None, bot.send_message, chat_id, "Рецепт плова: 500 г баранини, 400 г рису, 2 моркви, 1 цибулина, 1 ч. л. зіри. Готуй у казані 1,5 години!")
        else:
            await loop.run_in_executor(None, bot.send_message, chat_id, f"Ти сказав: {text}")
    return {"ok": True}

# Установка webhook при запуску
@app.on_event("startup")
async def on_startup():
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOST', 'your-app-name.onrender.com')}/webhook"
    await bot.set_webhook(url=webhook_url)
    print(f"Webhook встановлено: {webhook_url}")

# Видалення webhook при завершенні
@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    print("Webhook видалено.")