from datetime import datetime
import pandas as pd


class Wallet:
    def __init__(self, name):
        self.name = name

    def add_data(self):
        current_datetime = (datetime.now()).strftime("%H:%M:%S %d-%m-%Y")
        summa = float(input(f'Enter the amount of {self.name}: '))
        description = input(f'Enter a description of your {self.name}: ')
        template_data = {'summa': [summa], 'description': [description], 'date': [current_datetime]}

        if self.name == 'income':
            print(f"In your wallet added {summa:.2f}€ for {description}.")
            print('---' * 20)
        else:
            print(f"You spent {summa:.2f}€ to {description}.")
            print('---' * 20)
        return template_data

    def save_data_csv(self, data):
        data.to_csv(f'{self.name}.csv', mode='w', index=False, header=True)

    def overwrite_data_csv(self, data):
        data.to_csv(f'{self.name}.csv', mode='a', index=False, header=False)

    def read_data_csv(self):
        read_csv = pd.read_csv(f'{self.name}.csv', delimiter=',')
        return read_csv

    def get_total_amount(self, data):
        value = sum(data['summa'])
        return value

    def get_panel_data(self, template_data):
        df = pd.DataFrame(template_data)
        return df


def main():
    income = Wallet('income')
    outcome = Wallet('outcome')
    template_data = {'summa': [], 'description': [], 'date': []}
    while True:
        try:
            income_summa = income.get_total_amount(income.read_data_csv())
            outcome_summa = outcome.get_total_amount(outcome.read_data_csv())
        except FileNotFoundError:
            income.save_data_csv(income.get_panel_data(template_data))
            outcome.save_data_csv(outcome.get_panel_data(template_data))
            income_summa = 0.00
            outcome_summa = 0.00
        user_choose = int(input(f" 1 - Add income.\n"
                                f" 2 - Add outcome.\n"
                                f" 3 - View wallet balance.\n"
                                f" 4 - View total income.\n"
                                f" 5 - View total outcome.\n"
                                f" 6 - View total income list.\n"
                                f" 7 - View total outcome list.\n"
                                f"Select the action you need and input the command number: "))
        print('---' * 20)

        if user_choose == 1:
            income.overwrite_data_csv(income.get_panel_data(income.add_data()))

        elif user_choose == 2:
            outcome.overwrite_data_csv(outcome.get_panel_data(outcome.add_data()))

        elif user_choose == 3:
            print(f'In your wallet is: {income_summa - outcome_summa:.2f}€')
            print('---' * 20)

        elif user_choose == 4:
            print(f'Your total income is: {income_summa:.2f}€')
            print('---' * 20)

        elif user_choose == 5:
            print(f'Your total outcome is: {outcome_summa:.2f}€')
            print('---' * 20)

        elif user_choose == 6:
            print('Your total income list: ')
            print(income.read_data_csv())
            print('---' * 20)

        elif user_choose == 7:
            print('Your total outcome list: ')
            print(outcome.read_data_csv())
            print('---' * 20)


if __name__ == '__main__':
    main()
