with open("opcoes_menu.txt", encoding="utf-8") as msg:
    mensagem_menu = msg.read()
mensagem_menu += "\n\n=> "

saldo = 0
numero_saques = 0
extrato = ""
LIMITE = 500
LIMITE_SAQUES = 3

while True:
    opcao = input(mensagem_menu).lower()

    match opcao:
        case "d":
            if opcao == "d":
                try:
                    valor = float(input("Informe o valor do depósito: "))
                except ValueError:
                    print("Operação falhou! valor informado inválido.")
                    continue

                if valor > 0:
                    saldo += valor
                    extrato += f"Depósito: R$ {valor:.2f}\n".replace(".", ",")
            else:
                print("Operação falhou! O valor informado é inválido")

        case "s":
            try:
                valor = float(input("Informe o valor do saque: "))
            except ValueError:
                print("Operação falhou! valor informado inválido.")
                continue
            excedeu_saldo = valor > saldo
            excedeu_limite = valor > LIMITE
            excedeu_saques = numero_saques >= LIMITE_SAQUES

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
            else:
                print("Operação falhou! O valor informado é inválido")
    
        case "e":
            print("\n=============== EXTRATO ===============")
            print("Não foram realizados movimentações." 
                  if not extrato else extrato)
            print(f"\nSaldo: R$ {saldo:.2f}".replace(".", ","))
            print("=========================================")

        case "q":
            break

        case _:
            print("Operação inválida, "
                  "por favor selecione novamente a operação desejada.")