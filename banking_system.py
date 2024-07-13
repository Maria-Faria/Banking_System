from datetime import datetime
from abc import ABC, abstractmethod
from pathlib import Path
import time

## CLASSE CLIENTE
class Client:
    def __init__(self, address, accounts = []):
        self._address = address
        self._accounts = accounts

    def carry_out_transaction(self, account, transaction, operation, number_withdraws = 0):
        if(transaction.type == 'deposit'):
            transaction.register(account=account, operation=operation)
        
        else:
            transaction.register(account=account, number_withdraws=number_withdraws, operation=operation)

    def add_account(self, account):
        self._accounts.append(account)

    @property
    def accounts(self):
        return self._accounts


class Physical_Person(Client):
    def __init__(self, cpf, name, birth_date, address, accounts = []):
        self._cpf = cpf
        self._name = name
        self._birth_date = birth_date
        super().__init__(address, accounts)

    def show_my_data(self):
        my_accounts = ""

        for account in self._accounts:
            my_accounts += f"{account.agency}-{account.number} . . . . Saldo disponível: R${account.balance:.2f}\n\t    "

        return f"""
            Seus dados:

            CPF: {self._cpf}
            Nome: {self._name}
            Data de nascimento: {self._birth_date}
            Endereço: {self._address}

            >>

            Suas contas:

            {my_accounts}
            """
    
    @property
    def cpf(self):
        return self._cpf
    
    def __str__(self):
        return f"""
        CPF: {self._cpf}
        Nome: {self._name}
        Data de nascimento: {self._birth_date}
        Endereço: {self._address}
        """

## CLASSE TRANSAÇÃO
class Transaction(ABC):
    @abstractmethod
    def register(account):
        pass

class Deposit(Transaction):
    def __init__(self, value, date, type = "deposit"):
        self._value = value
        self._type = type
        self._date = date

    @property
    def type(self):
        return self._type
    
    @property
    def value(self):
        return self._value
    
    @property
    def date(self):
        return self._date
    
    def register(self, account, operation):
        account.deposit(self._value, self, operation=operation)

class To_Withdraw(Transaction):
    def __init__(self, value, date, type = "withdraw"):
        self._value = value
        self._type = type
        self._date = date

    @property
    def type(self):
        return self._type
    
    @property
    def value(self):
        return self._value
    
    @property
    def date(self):
        return self._date
    
    def register(self, account, operation, number_withdraws):
        account.to_withdraw(value = self._value, number_withdraws = number_withdraws, transaction = self, operation = operation)

## CLASSE HISTÓRICO
class Historic:
    def __init__(self, content = ""):
        self._content = content
        self._transactions = []

    def add_transation(self, transaction):
        if((transaction.date.strftime('%d/%m/%Y') == date_now.strftime('%d/%m/%Y')) and (transaction.type == "withdraw")):
            self._transactions.append(transaction)

        signal = "-" if transaction.type == "withdraw" else "+" 
        self._content += f"{signal} R${transaction.value:.2f} ...... {transaction.date.strftime('%d/%m/%Y %H:%M')}\n"

    @property
    def content(self):
        return self._content
    
    @property
    def transactions(self):
        return self._transactions
    
## CLASSE CONTA
class Account:
    def __init__(self, client, number, agency = "0001", balance = 0):
        self._balance = balance
        self._historic = Historic()
        self._client = client
        self._number = number
        self._agency = agency
    @property
    def balance(self):
        return self._balance
    
    @property
    def agency(self):
        return self._agency
    
    @property
    def number(self):
        return self._number
    
    #decorador de logs
    def log_transaction(func):
        ROOT_PATH = Path(__file__).parent
        def show_date(*args, **kwargs):
            file = open(ROOT_PATH / "log.txt", "a", encoding="utf-8")
            file.write("*************************************\n")

            file.write(f"Data da operação: {date_now.strftime('%d/%m/%Y %H:%M')}\n")
            file.write(f"Operação realizada: {kwargs['operation']}\n")

            if(kwargs['operation'] == "Criação de conta"):
                file.write(f"Dados do cliente: {args[1]}\n")
                file.write(f"Número da conta criada: {args[2]}\n")

            elif(kwargs['operation'] == "Depósito"):
                file.write(f"Valor depositado: R${args[1]:.2f}\n")

            else:
                file.write(f"Valor sacado: R${kwargs['value']:.2f}\n")

            file.close()
            print(f"\nData da operação: {date_now.strftime('%d/%m/%Y')}")
            return func(*args, **kwargs)

        return show_date

    @classmethod
    @log_transaction
    def new_account(cls, client, number, operation):
        print(f"Nova conta cadastrada com sucesso!\nNúmero da conta: {number}")
        return cls(client, number)
    
    @log_transaction
    def to_withdraw(self, *, value, transaction, operation):
        while(value > 500 or value < 0):
            value = float(input("""\nValor inválido! O limite máximo para saque é de R$500,00 e o valor mínimo é de R$1,00! Tente novamente: R$"""))

        if(value > self._balance):
            print("\nVocê não possui saldo suficiente para realizar o saque!")
            return False

        else: 
            self._balance -= value
            self._historic.add_transation(transaction)
            print("Saque realizado!")
            return True
        
    @log_transaction
    def deposit(self, value, transaction, /, operation):
        while(value <= 0):
            value = float(input("\nValor inválido! Tente novamente: R$ "))

        self._balance += value
        self._historic.add_transation(transaction)
        print("Depósito realizado com sucesso!")

        return True
    
    @property
    def historic(self):
        print(f"\nExtrato da conta {self.agency}-{self.number}")
        print("----------------------------------")
        return self._historic.content + f"\n\nSaldo disponível: R${self.balance:.2f}"
        
class Current_Account(Account):
    def __init__(self, client, number, limit = 500, withdrawal_limit = 3, agency = "0001", balance = 0):
        super().__init__(client, number, agency, balance)
        self._limit = limit
        self._withdrawal_limit = withdrawal_limit

    def to_withdraw(self, *, value, number_withdraws, transaction, operation):
        if(len(self._historic.transactions) == self._withdrawal_limit):
            print(f"\nVocê atingiu seu limite de {self._withdrawal_limit} saques diários!")
            time.sleep(3)
        
        else:
            super().to_withdraw(value=value, transaction=transaction, operation=operation)

    def __str__(self):
        print(self._client)
        return f"""
        CPF do cliente: {self._client.cpf}
        """
## Testando...

def check_user_exists(cpf):
    user_exists = False
    client = None

    for user in clients:
        if(user.cpf == cpf):
            user_exists = True
            client = user

    return user_exists, client

def search_account(client):
    for account_client in client.accounts:
        if(account_number == account_client.number):
            account = account_client
            return account
        
    return None

clients = [Physical_Person("49281656833", "Maria", "15/04/2004", "R. Joaquim Antonio da Rocha, 222 - Tinga - Caraguatatuba/SP")]
client = None

number_withdraws = 0
date_now = datetime.now()

## Iniciando o sistema
initial_menu = int(input("""
Bem vindo(a) ao Snake Bank!
*****************************************

Você já possui cadastro em nosso banco?

    [1] Sim
    [2] Não

    => """))

## Usuário ainda não possui cadastro no banco
if(initial_menu == 2):
    user_exists = False
    print("\nOk, vamos criar seu cadastro!\n")

    name = input("Digite seu nome: ")
    date_of_birth = input("Digite sua data de nascimento: ")
    cpf = input("Digite seu CPF: ")
    
    #verificar se há somente números no CPF
    while(cpf.isdigit() == False):
        cpf = input("\nCPF deve conter apenas números, por favor digite novamente: ")

    street = input("Digite o nome da rua onde você mora: ")
    number = input("Digite o número da sua casa: ")
    neighborhood = input("Digite o nome do bairro onde você mora: ")
    city = input("Digite o nome da cidade onde você mora: ")
    state = input("Digite a sigla do estado onde você mora: ")

    #Verificando sigla do estado
    while(len(state)> 2):
        state = input("\nInforme somente a sigla de seu estado: ")

    #Formatando o endereço
    address = f"{street}, {number} - {neighborhood} - {city}/{state}"

    #Verificar se o CPF já foi cadastrado anteriormente
    user_exists = check_user_exists(cpf)[0]

    # Caso o CPF não seja encontrado nos resgistros
    if(not user_exists):
        client = Physical_Person(address=address, cpf=cpf, name=name, birth_date=date_of_birth)
        clients.append(client)
        print("\nParabéns, seu cadastro foi registrado com sucesso!")

    else:
        client = check_user_exists(cpf)[1]
        print("\nUsuário já cadastrado!")

    time.sleep(2)

    # Exibindo dados do cliente
    print(client.show_my_data())
    
else:
    cpf = input("\nDigite seu CPF: ")
    
    user_exists = check_user_exists(cpf)[0]

    if(user_exists):
        client = check_user_exists(cpf)[1]
        print(client.show_my_data())

    else:
        print("\nUsuário não encontrado!")

print("**************************************")
time.sleep(4)

menu = """
    Selecione uma opção:

    [0] Criar uma conta corrente
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Visualizar meus dados
    [5] Sair

    => """

line = "*****************************************"
choice = -1
account_number = 1

if(client != None):
    # Exibindo menu ao usuário
    while(choice != 5):
        choice = int(input(menu))
        print(line)

        if(choice == 0):
            account = Current_Account.new_account(client, account_number, operation="Criação de conta")
            client.add_account(account)
            account_number += 1
            time.sleep(2)

        elif(choice == 1):
            account = None
            account_number = int(input("Informe o número da conta na qual deseja realizar o depósito: "))

            account = search_account(client)

            if(account != None):
                value = float(input("""
                    Opção DEPÓSITO selecionada
                            
                    Digite aqui o valor a ser depositado: R$ """))

                deposit = Deposit(value, datetime.now())
                client.carry_out_transaction(account, deposit, operation="Depósito")

            else:
                print("Conta corrente não encontrada!")

            time.sleep(2)

        elif(choice == 2):
            account = None
            account_number = int(input("Informe o número da conta na qual deseja realizar o saque: "))

            account = search_account(client)

            if(account != None):

                value = float(input("""
                    Opção SAQUE selecionada
                                    
                    Digite aqui o valor a ser sacado: R$"""))
                
                to_withdraw = To_Withdraw(value, datetime.now())
                client.carry_out_transaction(account, to_withdraw, operation="Saque")
                number_withdraws += 1
                
            else:
                print("Conta corrente não encontrada!")

            time.sleep(2)

        elif (choice == 3):
            account = None
            account_number = int(input("Informe o número da conta da qual deseja visualizar o extrato: "))

            account = search_account(client)

            if(account != None):
                print(account.historic)

            else:
                print("Conta corrente não econtrada!")

            time.sleep(4)

        elif(choice == 4):
            print(client.show_my_data())
            time.sleep(4)

        elif (choice == 5):
            print("Obrigado por utilizar nosso sistema!")

        else:
            print("Opção inválida!")
            time.sleep(3)