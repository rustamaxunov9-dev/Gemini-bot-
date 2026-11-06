import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from google import genai

# Kalitlar
TELEGRAM_BOT_TOKEN = "9180336409:AAHxLv7rLjYqTt0w5sPTVdsaPlNOfH19Wo0"
GEMINI_API_KEY = "AQ.Ab8RN6J8eQwVZmtWJCLME5TA1fDc97JkfvboyW6X7IkMr21Ucw"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
ai_client = genai.Client(api_key=GEMINI_API_KEY)


@dp.message(CommandStart())
async def start_handler(message: types.Message):
  await message.answer(
      "Assalomu alaykum! Men Gemini AI botiman. Savolingizni yozishingiz"
      " mumkin."
  )


@dp.message()
async def chat_handler(message: types.Message):
  await bot.send_chat_action(chat_id=message.chat.id, action="typing")
  try:
    response = ai_client.models.generate_content(
        model="gemini-2.5-flash", contents=message.text
    )
    answer = (
        response.text
        if response.text
        else "Uzr, javob shakllantirib bo‘lmadi."
    )

    if len(answer) > 4000:
      for i in range(0, len(answer), 4000):
        await message.answer(answer[i : i + 4000])
    else:
      await message.answer(answer)
  except Exception as e:
    logging.error(f"Xatolik: {e}")
    await message.answer("Xatolik yuz berdi. Qaytadan urinib ko‘ring.")


async def main():
  await bot.delete_webhook(drop_pending_updates=True)
  await dp.start_polling(bot)


if name == "main":
  asyncio.run(main())
