# Lista para armazenar os projetos
projetos = []

def input_obrigatorio(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor == "":
            print("❌ Este campo é obrigatório.")
        else:
            return valor

def cadastrar_projeto():
    print("\n📌 Cadastro de novo projeto")
    nome = input_obrigatorio("Nome do projeto: ")
    turma = input_obrigatorio("Turma (ex: 3ºA): ")

    turno = ""
    while turno not in ["Manhã", "Tarde", "Noite"]:
        turno = input("Turno (Manhã/Tarde/Noite): ").strip().capitalize()
        if turno not in ["Manhã", "Tarde", "Noite"]:
            print("❌ Turno inválido. Digite Manhã, Tarde ou Noite.")

    alunos = []
    print("\nDigite os nomes dos alunos:")
    for i in range(6):
        while True:
            aluno = input(f"Aluno {i+1}: ").strip()
            if i < 4:
                if aluno == "":
                    print("❌ Este campo é obrigatório.")
                else:
                    alunos.append(aluno)
                    break
            else:
                alunos.append(aluno if aluno != "" else "—")
                break

    descricao = input_obrigatorio("\nDescrição do projeto: ")

    projeto = {
        "nome": nome,
        "turma": turma,
        "turno": turno,
        "alunos": alunos,
        "descricao": descricao,
        "votos": 0
    }

    projetos.append(projeto)
    print(f"\n✅ Projeto '{nome}' cadastrado com sucesso!")

def exibir_projetos():
    if not projetos:
        print("\n⚠️ Nenhum projeto cadastrado.")
        return
    print("\n📋 Projetos disponíveis:")
    for i, p in enumerate(projetos, start=1):
        print(f"\n{i}. {p['nome']} ({p['turma']} - {p['turno']})")
        print(f"   Alunos: {', '.join(p['alunos'])}")
        print(f"   Descrição: {p['descricao']}")
        print(f"   Votos: {p['votos']}")

def votar():
    if not projetos:
        print("\n⚠️ Nenhum projeto disponível para votar.")
        return
    exibir_projetos()
    try:
        escolha = int(input("\nDigite o número do projeto que deseja votar: "))
        if 1 <= escolha <= len(projetos):
            projetos[escolha - 1]["votos"] += 1
            print(f"✅ Voto registrado para: {projetos[escolha - 1]['nome']}")
        else:
            print("❌ Número inválido.")
    except ValueError:
        print("❌ Entrada inválida. Digite um número.")

def mostrar_resultados():
    if not projetos:
        print("\n⚠️ Nenhum projeto para mostrar resultados.")
        return
    print("\n📊 Resultados da votação:")
    for p in projetos:
        print(f"{p['nome']} ({p['turma']} - {p['turno']}): {p['votos']} voto(s)")

# Loop principal
def menu():
    while True:
        print("\n--- MENU ---")
        print("1. Cadastrar novo projeto")
        print("2. Exibir projetos")
        print("3. Votar em projeto")
        print("4. Mostrar resultados")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_projeto()
        elif opcao == "2":
            exibir_projetos()
        elif opcao == "3":
            votar()
        elif opcao == "4":
            mostrar_resultados()
        elif opcao == "5":
            print("👋 Encerrando o aplicativo. Até mais!")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

# Iniciar o programa
menu()
