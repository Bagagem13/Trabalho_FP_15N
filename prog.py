# GRUPO: 15N

# Desenvolvam o trabalho neste ficheiro.
# Podem criar outros ficheiros e importá-los aqui.

import sys


# ---------------------------------------------------------------
# DADOS
# ---------------------------------------------------------------
# ementa: código -> dicionário com os dados do artigo
EMENTA_EXEMPLO = {
    "E01": {"nome": "Sopa do dia", "categoria": "entrada", "preco": 2.50, "doses": 10},
    "E02": {"nome": "Pastéis de bacalhau", "categoria": "entrada", "preco": 3.80, "doses": 8},
    "P01": {"nome": "Bacalhau à Brás", "categoria": "prato", "preco": 9.90, "doses": 4},
    "P02": {"nome": "Frango assado", "categoria": "prato", "preco": 8.50, "doses": 6},
    "S01": {"nome": "Pudim", "categoria": "sobremesa", "preco": 2.80, "doses": 5},
    "B01": {"nome": "Água 0,5L", "categoria": "bebida", "preco": 1.20, "doses": 20},
}

# pedido: código -> quantidade pedida
PEDIDO_EXEMPLO = {"E01": 2, "P01": 1}

CATEGORIAS = ["entrada", "prato", "sobremesa", "bebida"]   # ordem na fatura
LIMITE_ENTREGA_GRATIS = 20.0
TAXA_ENTREGA = 2.50


# ---------------------------------------------------------------
# FICHEIROS
# ---------------------------------------------------------------
def ler_ementa(nome_ficheiro):
    """Abre o ficheiro, salta a 1.ª linha (cabeçalho) e devolve o
    dicionário da ementa. Linhas inválidas são avisadas e ignoradas.
    Se o ficheiro não existir, avisa e devolve None (ou {})."""
    ementa = {}

    try:
        with open(nome_ficheiro, "r", encoding="utf-8") as ficheiro:
            next(ficheiro, None)

            for linha in ficheiro:
                texto = linha.strip()
                if not texto:
                    print("Linha inválida ignorada:", texto)
                    continue

                campos = [campo.strip() for campo in texto.split(",")]
                if len(campos) != 5:
                    print("Linha inválida ignorada:", texto)
                    continue

                codigo, nome, categoria, preco_texto, doses_texto = campos

                try:
                    preco = float(preco_texto)
                    doses = int(doses_texto)
                except ValueError:
                    print("Linha inválida ignorada:", texto)
                    continue

                if (
                    not codigo
                    or not nome
                    or categoria not in CATEGORIAS
                    or codigo in ementa
                    or preco < 0
                    or doses < 0
                ):
                    print("Linha inválida ignorada:", texto)
                    continue

                ementa[codigo] = {
                    "nome": nome,
                    "categoria": categoria,
                    "preco": preco,
                    "doses": doses,
                }

    except FileNotFoundError:
        print("Erro: ficheiro não encontrado:", nome_ficheiro)
    except OSError as erro:
        print("Erro ao abrir o ficheiro:", erro)

    return ementa


def guardar_ementa(ementa, nome_ficheiro):
    """Escreve o cabeçalho e uma linha por artigo, no MESMO formato
    do ficheiro original, com as doses atualizadas."""
    pass


# ---------------------------------------------------------------
# VALIDAÇÃO DE INPUTS
# ---------------------------------------------------------------
def pedir_inteiro_positivo(mensagem):
    """Pede um número ao utilizador até ele escrever um inteiro > 0.
    Usa try/except ValueError. Devolve o inteiro."""
    while True:
        texto = input(mensagem).strip()
        try:
            valor = int(texto)
            if valor > 0:
                return valor
            print("Erro: introduza um número inteiro positivo.")
        except ValueError:
            print("Erro: introduza um número inteiro positivo.")


# ---------------------------------------------------------------
# CONSULTAR A EMENTA
# ---------------------------------------------------------------
def pedir_filtros():
    """Pergunta um filtro de cada vez (vazio = ignorar):
    categoria, preço máximo, só disponíveis, texto no nome.
    Devolve um dicionário, ex.: {"categoria": "prato", "preco_max": 9.0}"""
    pass


def passa_filtros(artigo, filtros):
    """Devolve True se o artigo cumprir todos os filtros ativos."""
    if not filtros:
        return True

    categoria = filtros.get("categoria")
    if categoria and artigo["categoria"].lower() != str(categoria).lower():
        return False

    preco_max = filtros.get("preco_max")
    if preco_max is not None and artigo["preco"] > preco_max:
        return False

    apenas_disponiveis = filtros.get("disponiveis", filtros.get("so_disponiveis", False))
    if apenas_disponiveis and artigo["doses"] <= 0:
        return False

    texto = filtros.get("texto")
    if texto and str(texto).lower() not in artigo["nome"].lower():
        return False

    return True


def mostrar_ementa(ementa, filtros=None):
    """Imprime a ementa em tabela (código, nome, categoria, preço, doses),
    só com os artigos que passam nos filtros."""
    artigos = [
        (codigo, artigo)
        for codigo, artigo in ementa.items()
        if passa_filtros(artigo, filtros)
    ]

    print(f"{'Código':<8} {'Nome':<35} {'Categoria':<12} {'Preço':>8} {'Doses':>8}")
    print("-" * 75)

    if not artigos:
        print("Nenhum artigo corresponde aos filtros.")
        return

    for codigo, artigo in artigos:
        print(
            f"{codigo:<8} "
            f"{artigo['nome']:<35} "
            f"{artigo['categoria']:<12} "
            f"{artigo['preco']:>7.2f} € "
            f"{artigo['doses']:>5}"
        )


# ---------------------------------------------------------------
# PEDIDO
# ---------------------------------------------------------------
def adicionar_ao_pedido(ementa, pedido):
    """Pede código e quantidade. Valida: código existe, quantidade válida,
    (já pedido + nova quantidade) <= doses. Se o artigo já estiver no
    pedido, soma à quantidade existente."""
    
    codigo = input("Código do artigo: ").strip().upper()

    if codigo not in ementa:
        print("Erro: código inexistente.")
        return

    artigo = ementa[codigo]
    quantidade = pedir_inteiro_positivo("Quantidade: ")
    quantidade_no_pedido = pedido.get(codigo, 0)

    if quantidade_no_pedido + quantidade > artigo["doses"]:
        print("Erro: quantidade superior às doses disponíveis.")
        return

    pedido[codigo] = quantidade_no_pedido + quantidade
    print(
        f"Adicionado ao pedido: {artigo['nome']} "
        f"(quantidade: {pedido[codigo]})."
    )


def calcular_desconto(ementa, pedido):
    """Aplica a regra de desconto promocional (a definir e documentar
    no README). Devolve o valor do desconto em euros."""
    pass


def calcular_totais(ementa, pedido):
    """Devolve (subtotal, desconto, taxa_entrega, total).
    Taxa de 2,50 € se o valor (já com desconto) for < 20 €.
    Pedido vazio -> sem taxa. É usada pelo pedido E pela fatura."""
    pass


def mostrar_pedido(ementa, pedido):
    """Lista nomes, quantidades, subtotal, desconto, taxa e total.
    Se o pedido estiver vazio, avisa."""
    pass


def pagar_e_faturar(ementa, pedido):
    """Se o pedido estiver vazio, avisa e sai.
    Senão: imprime a fatura por categoria, abate as doses vendidas
    na ementa e esvazia o pedido (pedido.clear())."""
    pass


def imprimir_fatura(ementa, pedido):
    """Tabela formatada, organizada por categoria (ordem de CATEGORIAS),
    com nome, quantidade, preço unitário, subtotal da linha, e no fim
    subtotal, desconto, taxa de entrega e total."""
    pass


# ---------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------
def mostrar_menu():
    """Imprime as opções do menu."""
    print("\n=== RESTAURANTE TAKE-AWAY ===")
    print("1 - Ver ementa")
    print("2 - Adicionar artigo ao pedido")
    print("3 - Ver pedido")
    print("4 - Pagar e emitir fatura")
    print("0 - Terminar e guardar")


def main():
    """Lê o ficheiro (argumento da linha de comando ou 'ementa.txt'),
    corre o ciclo do menu e, ao sair, guarda as doses atualizadas."""
    ficheiro = sys.argv[1] if len(sys.argv) > 1 else "ementa.txt"
    ementa = ler_ementa(ficheiro)
    if not ementa:
        print("Não foi possível carregar a ementa.")
        return

    pedido = {}

    while True:
        mostrar_menu()
        opcao = input("Opção: ").strip()

        if opcao == "1":
            mostrar_ementa(ementa, pedir_filtros())
        elif opcao == "2":
            adicionar_ao_pedido(ementa, pedido)
        elif opcao == "3":
            mostrar_pedido(ementa, pedido)
        elif opcao == "4":
            pagar_e_faturar(ementa, pedido)
        elif opcao == "0":
            guardar_ementa(ementa, ficheiro)
            print("Até à próxima!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()