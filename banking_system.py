from datetime import date
from abc import ABC, abstractmethod
import time

## CLASSE CLIENTE
class Client:
    def __init__(self, address, accounts = []):
        self._address = address
        self._accounts = accounts

    def carry_out_transaction(self, account, transaction):
        pass

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
            my_accounts += f"{account.agency}-{account.number}\n"

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

## CLASSE TRANSAÇÃO
class Transaction(ABC):
    @abstractmethod
    def register(account):
        pass

class Deposit(Transaction):
    def __init__(self, value):
        self._value = value

    def register(self, account):
        account.deposit(self._value)

class To_Withdraw(Transaction):
    def __init__(self, value):
        self._value = value
    def register(account):
        pass
## CLASSE HISTÓRICO
class Historic:
    def add_transation(self, transation):
        pass
## CLASSE CONTA
class Account:
    def __init__(self, client, number, agency = "0001", balance = 0, historic = None):
        self._balance = balance
        self._historic = historic
        self._client = client
        self._number = number
        self._agency = agency
    @property
    def balance(self):
        return self._balance
    
    @property
    def agency(self):
        return self.agency
    
    @property
    def number(self):
        return self._number

    @classmethod
    def new_account(cls, client, number):
        print(f"\nNova conta cadastrada com sucesso!\nNúmero da conta: {number}")
        return cls(client, number)
    
    def to_withdraw(self, *, value):
        while(value > 500 or value < 0):
            value = float(input("""\nValor inválido! O limite máximo para saque é de R$500,00 e o valor mínimo é de R$1,00! Tente novamente: R$"""))

        if(value > self._balance):
            print("\nVocê não possui saldo suficiente para realizar o saque!")
            return False

        else: 
            self._balance -= value
            print("\nSaque realizado!")
            return True
        
    def deposit(self, value, /):
        while(value <= 0):
            value = float(input("\nValor inválido! Tente novamente: R$ "))

        print("\nDepósito realizado!")

        return True
    
    def __str__(self):
        return f"Cliente: {self._client} - Conta: {self._agency}-{self._number}"
    
class Current_Account(Account):
    def __init__(self, client, number, limit = 500, withdrawal_limit = 3, agency = "0001", balance = 0, historic = None):
        super().__init__(client, number, agency, balance, historic)
        self._limit = limit
        self._withdawal_limit = withdrawal_limit

## Testando...

def check_user_exists(cpf):
    user_exists = False
    client = None

    for user in clients:
        if(user.cpf == cpf):
            user_exists = True
            client = user

    return user_exists, client

clients = [Physical_Person("49281656833", "Maria", "15/04/2004", "R. Joaquim Antonio da Rocha, 222 - Tinga - Caraguatatuba/SP")]
client = None

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

# Exibindo menu ao usuário
while(choice != 5):
    choice = int(input(menu))
    print(line)

    if(choice == 0):
        account = Current_Account.new_account(client, account_number)
        client.add_account(account)
        account_number += 1
        time.sleep(2)

    elif(choice == 1):
        account = None
        account_number = int(input("Informe o número da conta na qual deseja realizar o depósito: "))

        for account_client in client.accounts:
            if(account_number == account_client.number):
                account = account_client

        if(account != None):

            value = float(input("""
                Opção DEPÓSITO selecionada
                        
                Digite aqui o valor a ser depositado: R$ """))

            deposit = Deposit(value)
            deposit.register(account)       

        else:
            print("Conta corrente não encontrada!")

        time.sleep(2)

    elif(choice == 2):
        if(date_last_withdrawal != date.today()):
            number_withdraws = 0

        if(number_withdraws == 3 and date_last_withdrawal == date.today()):
            print("Você atingiu seu limite de 3 aques diários!")
            time.sleep(3)
        
        else: 
            date_last_withdrawal = date.today()

            value = float(input("""
            Opção SAQUE selecionada
                            
            Digite aqui o valor a ser sacado: R$"""))

            time.sleep(2)

        ## CHAMAR A FUNÇÃO DE SAQUE
        result = to_withdraw(date_last_withdrawal=date_last_withdrawal,balance=balance, value=0, bank_statement=withdrawals, limit=500, number_withdraws=qt_withdrawals, limit_withdraws=3)

        balance = result[0]
        withdrawals = result[1]
        qt_withdrawals = result[2]
        date_last_withdrawal = result[3]

        time.sleep(2)

    elif (choice == 3):
        print(show_bank_statement(balance, deposits=deposits, withdrawals=withdrawals))    
    
        time.sleep(4)

    elif(choice == 4):
        cpf = input("Infome seu cpf: ")
        print(show_my_data(users, accounts, cpf))

        time.sleep(4)

    elif (choice == 5):
        print("Obrigado por utilizar nosso sistema!")

    else:
        print("Opção inválida!")
        time.sleep(3)

def show_bank_statement(balance, /, *, deposits, withdrawals):
    return (f"""        MEU EXTRATO 
              
        Depósitos realizados: {deposits}
        Saques realizados: {withdrawals}

        Saldo atual: R${balance:.2f}""")