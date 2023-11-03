from time import sleep
import requests
from bs4 import BeautifulSoup
import fake_useragent
import re
import lxml


def get_diary_page_data():
    username = input('Введите username: ')
    password = input('Введите password: ')
    url = 'https://my.e-klase.lv/?v=15'
    user_agent = fake_useragent.UserAgent().random
    header = {'user-agent': user_agent}
    data = {
        'UserName': str(username),
        'Password': str(password)
    }
    with requests.session() as session:  # Создаём сессию(Продвинутый вариант).Обычный: session = requests.session()
        session.get(url)  # Получаем Куки
        response = session.post(url, data=data, headers=header)  # Логинимся
        if response.status_code == 200:
            cookies = response.cookies.get_dict()  # Получаем куки из ответа сервера
        else:
            print('Ошибка при отправке запроса для авторизации!')

        # Переходим на страницу с кнопками, использую куки
        buttons_url = 'https://my.e-klase.lv/SessionContext/SwitchStudentWithFamilyStudentAutoAdd'
        response = session.get(buttons_url, cookies=cookies)
        if response.status_code == 200:
            cookies = response.cookies.get_dict()  # Получаем куки из ответа сервера
        else:
            print('Ошибка при отправке запроса в окне выбора профиля!')

        # Переходим на страницу Дневника, использую куки
        diary = 'https://my.e-klase.lv/Family/Diary'
        diary = re.sub(r'>\s+<', '><', diary.replace('\n', ''))
        response = session.get(diary, cookies=cookies)
        if response.status_code == 200:
            cookies = response.cookies.get_dict()  # Получаем данные с сервера для парсинга
        else:
            print('Ошибка при отправке запроса, вкладка - "Дневник"!')
        soup = BeautifulSoup(response.text, 'lxml')

        return soup


def get_diary_days_data():
    week_data = get_diary_page_data().find('div', class_='student-journal-lessons-table-holder hidden-xs')
    dates = week_data.find_all('h2')
    dates_list = []
    count = 0
    for date in dates:
        dates_list.append(date.text.strip())
    day_data = week_data.find_all('table', class_='lessons-table')
    for i in day_data:
        print()
        print()
        print(f'<<<<<<<<<<   {dates_list[count]}   >>>>>>>>>>')
        print()
        lessons_data = i.find('tbody').find_all('tr')
        count += 1

        for j, datas in enumerate(lessons_data, 1):
            try:
                lesson_name = datas.find('span', class_='room')
                lesson_name = lesson_name.previous_element.text.strip()
            except AttributeError:
                lesson_name = ''

            try:
                lesson_topic = datas.find('td', class_='subject').text.strip()
            except AttributeError:
                lesson_topic = ''

            try:
                hometask_1 = datas.find('span', class_='ThirdPartyEvent__EventName').get_text(strip=True)
            except AttributeError:
                hometask_1 = ''
            if hometask_1 == '':
                try:
                    hometask_2 = datas.find('td', class_='hometask').text.strip()
                # hometask_2 = hometask_2.next_element.text.strip()
                except AttributeError:
                    hometask_2 = ''
            else:
                hometask_2 = ''

            try:
                score = datas.find('span', class_='score').text.strip()
            except AttributeError:
                score = ''

            result = (f'{j})\n<<< {lesson_name} >>>\n- Тема урока: "{lesson_topic}"\n'
                      f'- Домашнее задание: "{hometask_1}{hometask_2}"\n'
                      f'- Оценка: {score}')
            sleep(2)

            yield result


for data in get_diary_days_data():
    print(f'{data}')
    print('---' * 20)
#     main()
