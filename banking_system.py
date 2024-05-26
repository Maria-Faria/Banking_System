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

depositos = ""
saques = ""

while(choice != 4):
    choice = int(input(menu))

    if(choice == 1):
        print(line)
        value = float(input("""
        Opção DEPÓSITO selecionada
                      
        Digite aqui o valor a ser depositado: R$ """))

        while(value <= 0):
            value = float(input("Valor inválido! Tente novamente: R$ "))
        
        depositos += f"R${value:.2f}; "
    
    else:
        break