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
    choice = int(input(menu))
    print(line)

    if(choice == 1):
        value = float(input("""
        Opção DEPÓSITO selecionada
                      
        Digite aqui o valor a ser depositado: R$ """))

        while(value <= 0):
            value = float(input("\nValor inválido! Tente novamente: R$ "))

        print("\nDepósito realizado!")
        
        deposits += f"R${value:.2f}; "
        balance += value
    
        time.sleep(2)

    elif(choice == 2):

        if(date_last_withdrawal != date.today()):
            qt_withdrawals = 0

        if(qt_withdrawals == 3 and date_last_withdrawal == date.today()):
            print("Você atingiu seu limite de 3 saques diários!")
            time.sleep(3)
        
        else: 
            date_last_withdrawal = date.today()

            value = float(input("""
            Opção SAQUE selecionada
                                
            Digite aqui o valor a ser sacado: R$"""))

            while(value > 500 or value < 0):
                value = float(input("""\nValor inválido! O limite máximo para saque é de R$500,00 e o valor mínimo é de R$1,00! Tente novamente: R$"""))

            if(value > balance):
                print("\nVocê não possui saldo suficiente para realizar o depósito!")

            else: 
                print("\nSaque realizado!")

                qt_withdrawals += 1
                withdrawals += f"R${value:.2f}; "
                balance -= value

            time.sleep(2)

    elif (choice == 3):
        print(f"""        MEU EXTRATO 
              
        Depósitos realizados: {deposits}
        Saques realizados: {withdrawals}

        Saldo atual: R${balance:.2f}""")
    
        time.sleep(4)

    elif(choice != 4):
        print("Opção inválida!")