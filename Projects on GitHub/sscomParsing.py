import requests
from bs4 import BeautifulSoup
from bs4 import Tag
import lxml
from time import sleep
import re

headers = {"User-Agent":
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}
# def main():
#     url = f'https://www.ss.com/ru/transport/cars/bmw.html'
#     get_url(url)
print(f'{"-" * 10}\nAlfa Romeo, Audi\n{"-" * 40}\n'
                   f'BMW\n{"-" * 40}\n'
                   f'Chevrolet, Chrysler, Citroen\n{"-" * 40}\n'
                   f'Dacia, Dodge\n{"-" * 40}\n'
                   f'Fiat, Ford\n{"-" * 40}\n'
                   f'Honda, Hyundai\n{"-" * 40}\n'
                   f'Infiniti\n{"-" * 40}\n'
                   f'Jaguar, Jeep\n{"-" * 40}\n'
                   f'Kia\n{"-" * 40}\n'
                   f'Lancia, Land Rover, Lexus\n{"-" * 40}\n'
                   f'Mazda, Mercedes, Mini, Mitsubishi\n{"-" * 40}\n'
                   f'Nissan\n{"-" * 40}\n'
                   f'Opel\n{"-" * 40}\n'
                   f'Peugeot, Porsche\n{"-" * 40}\n'
                   f'Renault\n{"-" * 40}\n'
                   f'Saab, Seat, Skoda, Smart, Subaru, Suzuki\n{"-" * 40}\n'
                   f'Toyota\n{"-" * 40}\n'
                   f'Volkswagen, Volvo\n{"-" * 40}\n'
                   f'Vaz, Gaz, Uaz\n{"-" * 40}\n'
                   f'Others\n{"-" * 10}\n')
brand_auto = input(f"Введите название марки автомобиля(На англиском языке),чтобы получить список обЪявлений: ").lower()
print()
def get_url():
    count = 1
    while count < 2:
        url = f'https://www.ss.com/ru/transport/cars/{brand_auto}/page{count}.html'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find_all('div', class_='d1')
        count += 1
        for i in data:
            card_url = i.find('a') # href найдём после проверки тега "а" ниже.
            if not card_url: #Праверяем если в item вложенное "а".Если элемент не будет найден, то find вернет None,
                # а у объекта None нет атрибута get.
                continue
            url = 'https://www.ss.lv' + card_url.get('href') # теперь после проверки можем применять "get"
            yield url

for i, url in enumerate(get_url(), 1):
    response = requests.get(url, headers=headers)
    sleep(2)
    soup = BeautifulSoup(response.text, 'lxml')

    data = soup.find('div', {'id': 'msg_div_msg'})

    try: #Проверяем соответствуют ли данные нашему запросу, если да присвоиваем
        year = data.find('td', {'id': 'tdo_18'}).text #, если да присвоиваем, тогда добавляем в переменную
    except AttributeError: #Если возникнет ошибка, тогда присвоим переменной другое значени и цикл не прирвётся
        year = "--------"

    try:
        model = data.find('td', {'id': 'tdo_31'}).text
    except AttributeError:
        model = "--------"

    try:
        motor = data.find('td', {'id': 'tdo_15'}).text
    except AttributeError:
        motor = "--------"

    try:
        transmission = data.find('td', {'id': 'tdo_35'}).text
    except AttributeError:
        transmission = "--------"

    try:
        car_mileage = data.find('td', {'id': 'tdo_16'}).text
    except AttributeError:
        car_mileage = "--------"

    try:
        color = data.find('td', {'id': 'tdo_17'}).text
    except AttributeError:
        color = "--------"

    try:
        car_body = data.find('td', {'id': 'tdo_32'}).text
    except AttributeError:
        car_body = "--------"

    try:
        technical_inspection = data.find('td', {'id': 'tdo_223'}).text
    except AttributeError:
        technical_inspection = "--------"

    del_str = data.text.find('Марка')
    description = re.sub("^\s+|\n|\r|", '', data.text[:del_str])



    print(f'{i})\nМодель: {model}\n{"-" * 20}\nГод выпуска: {year}\n{"-" * 20}\nДвигатель: {motor}\n{"-" * 20}\n'
          f'КПП: {transmission}\n{"-" * 20}\nТип кузова: {car_body}\n{"-" * 20}\nЦвет: {color}\n{"-" * 20}\n'
          f'Пробег: {car_mileage} км.\n{"-" * 20}\nТех.Осмотр: {technical_inspection}\n{"-" * 20}\n'
          f'Описание: {description}\n{url}\n{"-" * 60}\n')
    print()
# if __name__ == "__main__":
#     main()
