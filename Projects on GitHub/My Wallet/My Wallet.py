from datetime import datetime

import pandas as pd


def get_total_amount(data):
    value = sum(data['summa'])
    return value


def get_panel_data(template_data):
    df = pd.DataFrame(template_data)
    return df


class Wallet:
    def __init__(self, name):
        self.name = name
        try:
            self.data = self.read_data_csv()
            self.total_amount = get_total_amount(self.data)
        except FileNotFoundError:
            self.template_data = {'summa': [], 'description': [], 'date': []}
            self.data = self.save_data_csv(get_panel_data(self.template_data))
            self.total_amount = 0.00

    def get_value_from_user(self):
        value = ''
        while not value:
            try:
                value = float(input(f'Enter the amount of {self.name}: '))
                return value
            except ValueError:
                print('Enter a number or the field must not be empty!')
                print('---' * 20)

    def get_description_from_user(self):
        flag = True
        while flag:
            description = input(f'Enter a description of your {self.name}: ')
            if description != '':
                flag = False
                return description
            else:
                print('The field must not be empty!')
                print('---' * 20)

    def add_data(self, value, description):
        current_datetime = (datetime.now()).strftime("%H:%M:%S %d-%m-%Y")
        template_data = {'summa': [value], 'description': [description], 'date': [current_datetime]}

        if self.name == 'income':
            print(f"In your wallet added {value:.2f}€ for {description}.")
            print('---' * 20)
        else:
            print(f"You spent {value:.2f}€ to {description}.")
            print('---' * 20)
        return template_data

    def save_data_csv(self, data):
        save_data = data.to_csv(f'{self.name}.csv', mode='w', index=False, header=True)
        return save_data

    def overwrite_data_csv(self, data):
        overwrite_data = data.to_csv(f'{self.name}.csv', mode='a', index=False, header=False)
        return overwrite_data

    def read_data_csv(self):
        read_csv = pd.read_csv(f'{self.name}.csv', delimiter=',')
        return read_csv


def main():
    income = Wallet('income')
    outcome = Wallet('outcome')
    spliter = '---' * 20
    while True:
        try:
            user_choose = int(input(f" 1 - Add income.\n"
                                    f" 2 - Add outcome.\n"
                                    f" 3 - View wallet balance.\n"
                                    f" 4 - View total income.\n"
                                    f" 5 - View total outcome.\n"
                                    f" 6 - View total income list.\n"
                                    f" 7 - View total outcome list.\n"
                                    f"Select the action you need and input the command number: "))
            print(spliter)

            if user_choose == 1:
                value = income.get_value_from_user()
                description = income.get_description_from_user()
                income.overwrite_data_csv(get_panel_data(income.add_data(value, description)))

            elif user_choose == 2:
                value = outcome.get_value_from_user()
                description = outcome.get_description_from_user()
                outcome.overwrite_data_csv(get_panel_data(outcome.add_data(value, description)))

            elif user_choose == 3:
                print(f'In your wallet is: {income.total_amount - outcome.total_amount:.2f}€')
                print(spliter)

            elif user_choose == 4:
                print(f'Your total income is: {income.total_amount:.2f}€')
                print(spliter)

            elif user_choose == 5:
                print(f'Your total outcome is: {outcome.total_amount:.2f}€')
                print(spliter)

            elif user_choose == 6:
                print('Your total income list: ')
                print(income.data)
                print(spliter)

            elif user_choose == 7:
                print('Your total outcome list: ')
                print(outcome.data)
                print(spliter)
        except ValueError:
            print('You need to input a number!')
            print(spliter)


if __name__ == '__main__':
    main()
