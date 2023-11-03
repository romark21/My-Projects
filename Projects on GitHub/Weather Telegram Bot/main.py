import requests
import datetime
from pprint import pprint
from config import open_weather_token


def get_weather(city, open_weather_token):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
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

        print(f"Погода в городе: {city}\nТемпература воздуха: {cur_weather}°C\nПо ощущениям: {feels_like_temp}°C\n"
              f"Влажность воздуха: {humidity}%\n"
              f"Давление воздуха: {pressure} мм рт.ст.\nМинимальная температура сегодня: {temp_min}°C\n"
              f"Максимальная температура сегодня: {temp_max}°C\n"
              f"Скорость ветра: {wind} м/c\nВосход солнца: {sunrise_timestamp}\nЗаход солнца: {sunset_timestamp}\n"
              f"Продолжительность светового дня: {length_of_the_day}\n"
              f"Хорошего дня!!!"
              )

    except Exception as ex:
        print(ex)
        print("Проверьте правильность написание названия города!")



def main():
    city = input("Введите город: ")
    get_weather(city, open_weather_token)


if __name__ == '__main__':
    main()