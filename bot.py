from aiogram import Bot, Dispatcher
from datetime import datetime
from aiogram import executor
from aiogram import types
import asyncio

bot = Bot(token='7122305869:AAHvFzw6okCmBGKUBzJ2VgC_MQVhA1duwZg')
dp = Dispatcher(bot)

running = True

async def on_startup(dp):
    print("your bot worked, never give up")


async def on_shutdown(dp):
    print("you did it")

    await bot.session.close()

def calculate_weeks_lived(birth_date: str) -> int:
    try:
        birth_date = datetime.strptime(birth_date, "%d.%m.%Y")
        current_date = datetime.now()
        delta = current_date - birth_date
        weeks_lived = delta.days // 7
        return weeks_lived
    except ValueError:
        return -1


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Assalomu aleykum! Man umr bo'yi davomida necha hafta yashaganingizni bilib beraman.")
    await message.reply("Tug'ilgan sanangizni quyidagi formatda yuboring: kun.oy.yil (masalan: 12.02.2002)")

@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
    global running
    running = False
    await message.reply("Biz sizning tanlovizni togri qabul kilamiz!")


@dp.message_handler()
async def handle_message(message: types.Message):
    global running
    try:
        birth_date = message.text.strip()
        weeks_lived = calculate_weeks_lived(birth_date)

        if weeks_lived >= 0:
            for week in range(weeks_lived, 4500):
                if not running:
                    break
                response = f"Siz {week} hafta yashadingiz. Qolgan hafta: {4500 - week}"
                await bot.send_message(message.chat.id, response)
                await asyncio.sleep(7)  # !!!!!!!!!!!
        else:
            response = "Tug'ilgan sanangizni to'g'ri kiriting. Misol uchun: kun.oy.yil (masalan: 13.02.2004)"
            await bot.send_message(message.chat.id, response)

    except Exception as e:
        print(f"Error occurred: {e}")
        response = "Xatolik yuz berdi. Iltimos qayta urinib ko'ring."
        await bot.send_message(message.chat.id, response)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
