import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет, пупсик!\n"
                        " Напиши мне названия города и я пришлю тебе сводку погоды.\n"
                        "Название города пиши 'Латинскими' буквами.\n"
                        " Знаешь такие?\n"
                        " Да?\n"
                        " Да ты ж моя умница. Череп не жмёт?")

@dp.message_handler()
async  def get_weather(message: types.Message):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        # pprint(data)

        city = data["name"]
        cur_weather = data["main"]["temp"]
        feels_like_temp = data["main"]["feels_like"]
        humidity = data['main']["humidity"]
        pressure = data['main']["pressure"]
        temp_min = data['main']["temp_min"]
        temp_max = data['main']["temp_max"]
        wind = data['wind']["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"Погода в городе: {city}\nТемпература воздуха: {cur_weather}°C\nПо ощущениям: {feels_like_temp}°C\n"
              f"Влажность воздуха: {humidity}%\n"
              f"Давление воздуха: {pressure} мм рт.ст.\nМинимальная температура сегодня: {temp_min}°C\n"
              f"Максимальная температура сегодня: {temp_max}°C\n"
              f"Скорость ветра: {wind} м/c\nВосход солнца: {sunrise_timestamp}\nЗаход солнца: {sunset_timestamp}\n"
              f"Продолжительность светового дня: {length_of_the_day}\n"
              f"Хорошего дня!!!"
              )

    except:
        await message.reply("Проверьте правильность написание названия города!")


if __name__ == '__main__':
    executor.start_polling(dp)
