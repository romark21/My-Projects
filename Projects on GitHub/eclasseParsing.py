from time import sleep
import requests
from bs4 import BeautifulSoup
import fake_useragent
import re


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
    with requests.session() as session:  
        session.get(url)  # Получаем Куки
        response = session.post(url, data=data, headers=header)  
        if response.status_code == 200:
            cookies = response.cookies.get_dict()  
        else:
            print('Ошибка при отправке запроса для авторизации!')

        # Go to the page with the buttons, using cookies
        buttons_url = 'https://my.e-klase.lv/SessionContext/SwitchStudentWithFamilyStudentAutoAdd'
        response = session.get(buttons_url, cookies=cookies)
        if response.status_code == 200:
            cookies = response.cookies.get_dict()  
        else:
            print('Ошибка при отправке запроса в окне выбора профиля!')

        # Go to the Diary page, using cookies.
        diary = 'https://my.e-klase.lv/Family/Diary'
        diary = re.sub(r'>\s+<', '><', diary.replace('\n', ''))
        response = session.get(diary, cookies=cookies)
        if response.status_code == 200:
            cookies = response.cookies.get_dict()  
        else:
            print('Ошибка при отправке запроса, вкладка - "Дневник"!')

        # Prompt the user for information about the week selection.
        user_week_data = input(f'Укажите за какую неделю вы хотите получить данные!\n1 - За текущую неделю\n'
                               f'2 - За следующию неделю\n'
                               f'Введите число: ')
        soup = BeautifulSoup(response.text, 'lxml')

        if user_week_data == '1':
            soup = soup
        elif user_week_data == '2':
            #find the link for next week's page
            next_week_url = soup.find('div', class_='week-selector clearfix').find_all('a')[-1].get('href')
            response = session.get('https://my.e-klase.lv/' + next_week_url,
                                   cookies=cookies)  # Check out next week's page
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
            else:
                print('Ошибка при отправке запроса на информацию о следующей недели!')
        else:
            print('Вы ввели неправильную команду!')

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
