from datetime import datetime
import pandas as pd



def money_in():
    income_sum = float(input('Input income value: '))
    income_description = input(f'Input description of income: ')
    Wallet.wallet_data['summa'].append(income_sum)
    Wallet.wallet_data['description'].append(income_description)
    Wallet.wallet_data['date'].append(Wallet.current_datetime)
    overwrite_income_data_csv()
    print(f"In your wallet added {income_sum:.2f}€ for {income_description}.")
    print('---' * 20)


def money_out():
    outcome_sum = float(input('Input outcome value: '))
    outcome_description = input(f'Input description of outcome: ')
    overwrite_outcome_data_csv()
    print(f"You spent {outcome_sum:.2f}€ to {outcome_description}.")
    print('---' * 20)


def balance():
    wallet_balance = sum(read_wallet_data_csv()['summa'])
    print(f'In your wallet is: {wallet_balance:.2f}€')


def save_income_data_csv():
    get_wallet_data().to_csv('wallet_income_data.csv', mode='w', index=False, header=True)


def save_outcome_data_csv():
    get_wallet_data().to_csv('wallet_outcome_data.csv', mode='w', index=False, header=True)


def overwrite_income_data_csv():
    get_wallet_data().to_csv('wallet_income_data.csv', mode='a', index=False, header=False)


def overwrite_outcome_data_csv():
    get_wallet_data().to_csv('wallet_outcome_data.csv', mode='a', index=False, header=False)


def new_datas_csv():
    save_income_data_csv()
    save_outcome_data_csv()


def read_wallet_data_csv():
    read_csv = pd.read_csv('../../pythonProject1/ООП/wallet_income_data.csv', delimiter=',')
    return read_csv


def get_wallet_data():
    df = pd.DataFrame(Wallet.wallet_data)
    return df


class Wallet:
    current_datetime = (a := datetime.now()).strftime("%H:%M:%S %d-%m-%Y")
    wallet_data = {'summa': [], 'description': [], 'date': []}


wallet = Wallet()

new_datas_csv()

