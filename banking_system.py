from datetime import date
import time

menu = """
Bem vindo(a) ao Snake Bank!
*****************************************
    Selecione uma opção:

    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Sair

    => """

line = "*****************************************"
choice = 0

deposits = ""
withdrawals = ""

qt_withdrawals = 0
date_last_withdrawal = ""

balance = 0

while(choice != 4):
    time.sleep(2)
    choice = int(input(menu))
    print(line)

    if(choice == 1):
        value = float(input("""
        Opção DEPÓSITO selecionada
                      
        Digite aqui o valor a ser depositado: R$ """))

        while(value <= 0):
            value = float(input("Valor inválido! Tente novamente: R$ "))

        print("Depósito realizado!")
        
        deposits += f"R${value:.2f}; "
        balance += value
    
    elif(choice == 2):

        if(date_last_withdrawal != date.today()):
            qt_withdrawals = 0

        if(qt_withdrawals == 3 and date_last_withdrawal == date.today()):
            print("Você atingiu seu limite de 3 saques diários!")
            time.sleep(3)
        
        else: 
            date_last_withdrawal = date.today()
            qt_withdrawals += 1

            value = float(input("""
            Opção SAQUE selecionada
                                
            Digite aqui o valor a ser sacado: R$"""))

            while(value > 500):
                value = float(input("""\nValor inválido! O limite máximo para saque é de R$500,00! Tente novamente: R$"""))

            print("Saque realizado!")

            withdrawals += f"Saques: R${value:.2f}; "
            balance -= value
    else:
        break