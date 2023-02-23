from typing import List, Tuple, Dict, Union


def menu():
    """Exibir mensagem de menu."""
    mensagem_menu: str = "\n" + " Menu ".center(30, "#")
    with open("opcoes_menu.txt", encoding="utf-8") as msg:
        mensagem_menu += "\n" + msg.read()
    mensagem_menu += "\n\n=> "
    return input(mensagem_menu).lower()


def depositar(saldo: float, valor: float, extrato: str, /):
    """Executar operação depósito do cliente.

    Args:
        saldo (float): Saldo bancário da conta do cliente.
        valor (float): Valor a ser depositado.
        extrato (str): Extrato bancário do cliente.

    Returns:
        (Tuple[float, str]): Tupla contendo saldo e extrato do cliente, 
                             respectivamente.
    """
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n".replace(".", ",")
        print("\nDepósito realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido")
    
    return saldo, extrato


def sacar(*, saldo: float, valor: float, extrato: str, 
          limite: float, numero_saques: int, limite_saques: int):
    """_summary_

    Args:
        saldo (float): Saldo bancário da conta do cliente.
        valor (float): Valor a ser depositado.
        extrato (str): Extrato bancário do cliente.
        limite (float): Valor limite permitido no saque.
        numero_saques (int): Número de saques permitidos.
        limite_saques (int): Limite de saques permitidos.

    Returns:
        (Tuple[float, str]): Tupla contendo saldo e extrato do cliente, 
                             respectivamente..
    """
    excedeu_saldo: bool = valor > saldo
    excedeu_limite: bool = valor > LIMITE
    excedeu_saques: bool = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("\nSaque realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido")
    
    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    """Exibir extrato do usuário.

    Args:
        saldo (float): Saldo bancário da conta do cliente.
        valor (float): Valor a ser depositado.
    """
    print("\n=============== EXTRATO ===============")
    print("Não foram realizados movimentações." 
            if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}".replace(".", ","))
    print("=========================================")


def filtrar_usuario(cpf: str, usuarios: List):
    """Filtrar usuário.

    Args:
        cpf (str): cpf a ser buscado para o filtro.
        usuarios (List): Lista de usuários cadastrados

    Returns:
        (Unio[Dict, None]): Dicionário com dados do usuário encontrado. 
                            Return None caso não seja encontrado.
    """
    usuarios_filtrados: List[dict] = [usuario for usuario in usuarios 
                                      if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_usuario(usuarios: List):
    """Cadastrar conta usuário.

    Args:
        usuarios (List): Lista contendo usuários já cadastrados.
    """
    cpf: str = input("Informe o CPF (Somente números): ")
    usuario: Union[Dict, None] = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\n Já existe usuários com esse CPF!")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento: str= input("Informe a data de nascimento (dd-mm-aaa): ")
    logradouro: str = input("Informe o logradouro (logradouro, número): ")
    bairro: str = input("Informe o bairro: ")
    cidade: str = input("Informe a cidade: ")
    uf: str = input("Informe a sigla da UF: ")
    endereco: str = f"{logradouro} - {bairro} - {cidade}/{uf}"
    
    usuario = {"nome": nome, "data_nascimento": data_nascimento, 
               "cpf": cpf, "endereco": endereco}
    usuarios.append(usuario)
    print("Usuário criado com sucesso!")


def criar_conta(agencia: str, numero_conta: str, usuarios: List):
    """Criar conta para o usuário

    Args:
        agencia (str): agencia relacionado ao usuário
        numero_conta (str): Némro da conta relacionado ao usuário.
        usuarios (List): Lista contendo usuários já cadastrados.

    Returns:
        Union[Dict, None]: Dicionário contendo dados do usuário caso 
                           haja sucesso. None caso falhe.
    """
    cpf: str = input("Informe o CPF do usuário: ")
    usuario: Union[Dict, None] = filtrar_usuario(cpf, usuarios)
    if usuarios:
        print("\nConta criada com sucesso!")
        return {"agencia": agencia, 
                "numero_conta": numero_conta, 
                "usuario": usuario}
    
    print("\n Usuário não encontrado, fluxo de criação de conta encerrado.")


def listar_contas(contas: List):
    for conta in contas:
        texto_conta = f"Agência: {conta['agencia']}\n"
        texto_conta += f"CC: {conta['numero_conta']}\n"
        texto_conta += f"Titular: {conta['usuario']['nome']}\n"
        print("="*100)
        print(texto_conta)


LIMITE: int = 500
LIMITE_SAQUES: int = 3
AGENCIA: str = "0001"
saldo: float = 0
numero_saques: int = 0
extrato: str = ""
usuarios: List = []
contas: List = []
numero_conta: int = 1

while True:
    opcao: str = menu()

    match opcao:
        case "d":
            try:
                valor: float = float(input("Informe o valor do depósito: "))
            except ValueError:
                print("Operação falhou! valor informado inválido.")
                continue
            saldo, extrato = depositar(saldo, valor, extrato)

        case "s":
            try:
                valor: float = float(input("Informe o valor do saque: "))
            except ValueError:
                print("Operação falhou! valor informado inválido.")
                continue
            saldo, extrato = sacar(saldo=saldo, valor=valor, extrato=extrato,
                                   limite=LIMITE, numero_saques=numero_saques,
                                   limite_saques=LIMITE_SAQUES)
    
        case "e":
            exibir_extrato(saldo, extrato=extrato)

        case "nu":
            criar_usuario(usuarios)
        
        case "cc":
            conta: Union[Dict, None] = criar_conta(AGENCIA, 
                                                   numero_conta,
                                                   usuarios)

            if conta:
                contas.append(conta)
                numero_conta += 1
        
        case "lc":
            listar_contas(contas)

        case "q":
            break

        case _:
            print("Operação inválida, "
                  "por favor selecione novamente a operação desejada.")
