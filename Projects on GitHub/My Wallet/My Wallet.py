from datetime import datetime
import pandas as pd
from speech_app import speaker

current_datetime = (a := datetime.now()).strftime("%H:%M:%S %d-%m-%Y")


def money_in():
    speaker('Enter the price of income: ')
    income_sum = float(input('Enter the price of income: '))
    speaker('Enter a description of your income: ')
    income_description = input(f'Enter a description of your income: ')
    income_data = {'summa': [income_sum], 'description': [income_description], 'date': [current_datetime]}
    overwrite_income_data_csv(income_data)
    print(f"In your wallet added {income_sum:.2f}€ for {income_description}.")
    speaker(f"In your wallet added {income_sum:.2f}€ for {income_description}.")
    print('---' * 20)
    return income_data


def money_out():
    speaker('Enter the price of outcome: ')
    outcome_sum = float(input('Enter the price of outcome: '))
    speaker('Enter a description of your outcome: ')
    outcome_description = input(f'Enter a description of your outcome: ')
    outcome_data = {'summa': [outcome_sum], 'description': [outcome_description], 'date': [current_datetime]}
    overwrite_outcome_data_csv(outcome_data)
    speaker(f"You spent {outcome_sum:.2f}€ to {outcome_description}.")
    print('---' * 20)


def balance():
    speaker(f" 1 - View wallet balance.\n"
            f" 2 - View total income.\n"
            f" 3 - View total outcome.\n"
            f"Select the action you need and input the command number: ")
    user_choose = int(input(f" 1 - View wallet balance.\n"
                            f" 2 - View total income.\n"
                            f" 3 - View total outcome.\n"
                            f"Select the action you need and input the command number: "))
    try:
        if user_choose == 1:
            print(f'In your wallet is: {Wallet.wallet_balance:.2f}€')
            speaker(f'In your wallet is: {Wallet.wallet_balance:.2f}€')
        elif user_choose == 2:
            print(f'Your total income is: {Wallet.wallet_total_income:.2f}€')
            speaker(f'Your total income is: {Wallet.wallet_total_income:.2f}€')
        elif user_choose == 3:
            print(f'Your total outcome is: {Wallet.wallet_total_outcome:.2f}€')
            speaker(f'Your total outcome is: {Wallet.wallet_total_outcome:.2f}€')
        else:
            print('You entered the wrong command. Please enter 1, 2 or 3.')
            speaker('You entered the wrong command. Please enter 1, 2 or 3.')
    except ValueError:
        print('Your wallet is empty!')
        speaker('Your wallet is empty!')


def save_income_data_csv():
    get_wallet_data(Wallet.template_wallet_data).to_csv('wallet_income_data.csv', mode='w', index=False, header=True)


def save_outcome_data_csv():
    get_wallet_data(Wallet.template_wallet_data).to_csv('wallet_outcome_data.csv', mode='w', index=False, header=True)


def overwrite_income_data_csv(func):
    get_wallet_data(func).to_csv('wallet_income_data.csv', mode='a', index=False, header=False)


def overwrite_outcome_data_csv(func):
    get_wallet_data(func).to_csv('wallet_outcome_data.csv', mode='a', index=False, header=False)


def new_datas_csv():
    save_income_data_csv()
    save_outcome_data_csv()


def read_income_data_csv():
    read_csv = pd.read_csv('wallet_income_data.csv', delimiter=',')
    return read_csv


def read_outcome_data_csv():
    read_csv = pd.read_csv('wallet_outcome_data.csv', delimiter=',')
    return read_csv


def get_wallet_data(func):
    df = pd.DataFrame(func)
    return df


class Wallet:
    template_wallet_data = {'summa': [], 'description': [], 'date': []}
    try:
        wallet_total_income = sum(read_income_data_csv()['summa'])
        wallet_total_outcome = sum(read_outcome_data_csv()['summa'])
        wallet_balance = wallet_total_income - wallet_total_outcome
    except ValueError:
        wallet_total_income = 0.00
        wallet_total_outcome = 0.00
        wallet_balance = 0.00


balance()
