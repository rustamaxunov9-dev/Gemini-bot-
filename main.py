import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from google import genai

# Сиз тақдим этган токенлар
TELEGRAM_BOT_TOKEN = "9180336409:AAHxLv7rLjYqTt0w5sPTVdsaPlNOfH19Wo0"
GEMINI_API_KEY = "AQ.Ab8RN6J8eQwVZmtWJCLME5TA1fDc97JkfvboyW6X7IkMr21Ucw"

# Логларни консолда чиқариб бориш (хатолик ёки жараённи кузатиш учун)
logging.basicConfig(level=logging.INFO)

# Телеграм бот ва диспетчер
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Gemini мижози
ai_client = genai.Client(api_key=GEMINI_API_KEY)


@dp.message(CommandStart())
async def start_handler(message: types.Message):
  await message.answer(
      "Ассалому алайкум! Мен Gemini сунъий интеллект ёрдамчисиман.\n"
      "Менга исталган саволингизни ёзинг, батафсил жавоб бераман!"
  )


@dp.message()
async def ai_message_handler(message: types.Message):
  # Фойдаланувчига "ёзяпти..." ҳолатини кўрсатиш
  await bot.send_chat_action(chat_id=message.chat.id, action="typing")

  try:
    # Gemini моделига сўров юбориш
    response = ai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=message.text,
    )

    answer_text = (
        response.text
        if response.text
        else "Узр, саволга жавоб шакллантирилмади."
    )

    # Телеграмда хабар 4096 та белгидан ошса, қисмларга бўлиб юбориш
    if len(answer_text) > 4000:
      for i in range(0, len(answer_text), 4000):
        await message.answer(answer_text[i : i + 4000])
    else:
      await message.answer(answer_text)

  except Exception as err:
    logging.error(f"Хатолик юз берди: {err}")
    await message.answer(
        "Кечирасиз, жавоб тайёрлашда хатолик юз берди ёки API калитда муаммо бор."
    )


async def main():
  # Эски келиб тушган ва жавоб берилмаган хабарларни тозалаш
  await bot.delete_webhook(drop_pending_updates=True)
  # Ботни ишга тушириш
  await dp.start_polling(bot)


if name == "main":
  asyncio.run(main())
