from datetime import date
import time

def deposit(deposits, balance, /):
    value = float(input("""
        Opção DEPÓSITO selecionada
                      
        Digite aqui o valor a ser depositado: R$ """))

    while(value <= 0):
        value = float(input("\nValor inválido! Tente novamente: R$ "))

    print("\nDepósito realizado!")
        
    deposits += f"R${value:.2f}; "
    balance += value

    return deposits, balance

def to_withdraw(*, date_last_withdrawal,balance, value, bank_statement, limit, number_withdraws, limit_withdraws):

    if(date_last_withdrawal != date.today()):
        number_withdraws = 0

    if(number_withdraws == limit_withdraws and date_last_withdrawal == date.today()):
        print(f"Você atingiu seu limite de {limit_withdraws} saques diários!")
        time.sleep(3)
        
    else: 
        date_last_withdrawal = date.today()

        value = float(input("""
        Opção SAQUE selecionada
                            
        Digite aqui o valor a ser sacado: R$"""))

        time.sleep(2)

    while(value > limit or value < 0):
        value = float(input(f"""\nValor inválido! O limite máximo para saque é de R${limit},00 e o valor mínimo é de R$1,00! Tente novamente: R$"""))

    if(value > balance):
        print("\nVocê não possui saldo suficiente para realizar o saque!")

    else: 
        print("\nSaque realizado!")

        number_withdraws += 1
        bank_statement += f"R${value:.2f}; "
        balance -= value

    return balance, bank_statement, number_withdraws, date_last_withdrawal

def show_bank_statement(balance, /, *, deposits, withdrawals):
    return (f"""        MEU EXTRATO 
              
        Depósitos realizados: {deposits}
        Saques realizados: {withdrawals}

        Saldo atual: R${balance:.2f}""")
    
def create_user(users, name, date_of_birth, cpf, street, number, neighborhood, city, state):
    while(len(state)> 2):
        state = input("\nInforme somente a sigla de seu estado: ")
        
    #verificar se há somente números no CPF
    while(cpf.isdigit() == False):
        cpf = input("\nCPF deve conter apenas números, por favor digite novamente: ")

    #verificar se o CPF já foi cadastrado
    for user in users:
        if(not cpf in user):
            #cadastrar novo usuário
            new_user = {cpf: {
                "name": name,
                "date_of_birth": date_of_birth,
                "address": f"{street}, {number} - {neighborhood} - {city}/{state}"
            }}
            users.append(new_user)

            if(users[0] == {}):
                users.pop(0)

    return users

users = [{}]
initial_menu = int(input("""
Bem vindo(a) ao Snake Bank!
*****************************************

Você já possui uma conta em nosso banco?

    [1] Sim
    [2] Não

    => """))

if(initial_menu == 2):
    print("\nOk, vamos criar sua conta!\n")

    name = input("Digite seu nome: ")
    date_of_birth = input("Digite sua data de nascimento: ")
    cpf = input("Digite seu CPF: ")
    street = input("Digite o nome da rua onde você mora: ")
    number = input("Digite o número da sua casa: ")
    neighborhood = input("Digite o nome do bairro onde você mora: ")
    city = input("Digite o nome da cidade onde você mora: ")
    state = input("Digite a sigla do estado onde você mora: ")

    create_user(users, name, date_of_birth, cpf, street, number, neighborhood, city, state)

    print("\nParabéns, sua conta foi criada com sucesso!")

    time.sleep(3)

menu = """

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
        result = deposit(deposits, balance)
    
        deposits = result[0]
        balance = result[1]

        time.sleep(2)

    elif(choice == 2):
        result = to_withdraw(date_last_withdrawal=date_last_withdrawal,balance=balance, value=0, bank_statement=withdrawals, limit=500, number_withdraws=qt_withdrawals, limit_withdraws=3)

        balance = result[0]
        withdrawals = result[1]
        qt_withdrawals = result[2]
        date_last_withdrawal = result[3]

        time.sleep(2)

    elif (choice == 3):
        print(show_bank_statement(balance, deposits=deposits, withdrawals=withdrawals))    
    
        time.sleep(4)

    elif (choice == 4):
        print("Obrigado por utilizar nosso sistema!")

    else:
        print("Opção inválida!")
        time.sleep(3)