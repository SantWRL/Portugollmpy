import json
import random
from config import CAMINHO_DATASET


def gerar_dataset():
    dados = []

    nomes_vars   = ["x", "y", "z", "a", "b", "contador", "total", "idade", "nota", "peso", "preco", "altura", "pontos", "saldo", "nivel"]
    verbos_print = ["escreva", "mostre", "imprima", "exiba", "apresente", "mostre na tela", "diga", "fale"]
    verbos_var   = ["crie a variavel", "defina", "faca", "declare", "inicie", "estabeleca", "atribua", "defina o valor de", "setar"]
    ligacoes     = ["como", "igual a", "recebendo", "valendo", "sendo", "com o valor"]
    verbos_loop  = ["repita", "faca um loop de", "itere", "execute", "cicle", "rode"]
    verbos_cond  = ["se", "caso", "verifique se", "teste se", "se por acaso"]
    textos       = ["ola mundo", "bom dia", "teste", "sucesso", "bem vindo", "erro no sistema", "concluido", "inicio", "parado", "ok", "processando"]

    # 1. Print texto
    for _ in range(150):
        t = random.choice(textos)
        dados.append({"pt": f"{random.choice(verbos_print)} {t}",
                      "portugol": f"escreva ( '{t}' )"})

    # 2. Print numero
    for _ in range(200):
        is_real = random.random() > 0.7
        n = str(round(random.uniform(0, 100), 2)) if is_real else str(random.randint(0, 100))
        pt = f"{random.choice(verbos_print)} {n}"
        dados.append({"pt": pt, "portugol": f"escreva ( {n} )"})

    # 3. Declaracao de variavel
    for _ in range(400):
        nome = random.choice(nomes_vars)
        is_real = random.random() > 0.5
        valor = str(round(random.uniform(0, 100), 2)) if is_real else str(random.randint(0, 100))
        tipo = "real" if is_real else "inteiro"
        dados.append({"pt": f"{random.choice(verbos_var)} {nome} {random.choice(ligacoes)} {valor}",
                      "portugol": f"{tipo} {nome} = {valor}"})

    # 4. Operacoes Matematicas
    ops = [("+", "mais"), ("-", "menos"), ("*", "vezes"), ("/", "dividido por")]
    for _ in range(400):
        v1, v2 = random.sample(nomes_vars, 2)
        op_sym, op_pt = random.choice(ops)
        t = random.choice([f"calcule {v1} {op_pt} {v2}", f"{v1} {op_pt} {v2}", f"quanto e {v1} {op_pt} {v2}"])
        dados.append({"pt": t, "portugol": f"{v1} {op_sym} {v2}"})

    # 5. Incremento / Decremento
    for _ in range(200):
        nome = random.choice(nomes_vars)
        n = str(random.randint(1, 10))
        dados.append({"pt": f"incremente {nome} em {n}", "portugol": f"{nome} = {nome} + {n}"})
        dados.append({"pt": f"decremente {nome} em {n}", "portugol": f"{nome} = {nome} - {n}"})

    # 6. Loop para
    for _ in range(200):
        n = str(random.randint(1, 10))
        dados.append({"pt": f"{random.choice(verbos_loop)} {n} vezes",
                      "portugol": f"para i de 1 ate {n} faca"})

    # 7. Loop enquanto
    ops_map = {"menor que": "<", "maior que": ">", "igual a": "==", "diferente de": "!="}
    for _ in range(200):
        nome = random.choice(nomes_vars)
        val  = str(random.randint(0, 20))
        op_str, op_sym = random.choice(list(ops_map.items()))
        acao_pt = f"mostre {nome}"
        acao_pg = f"escreva ( {nome} )"
        t = f"enquanto {nome} for {op_str} {val} faca {acao_pt}"
        dados.append({"pt": t, "portugol": f"enquanto ( {nome} {op_sym} {val} ) faca {acao_pg}"})

    # 8. Condicionais
    for _ in range(400):
        nome, val = random.choice(nomes_vars), str(random.randint(0, 100))
        op_str, op_sym = random.choice(list(ops_map.items()))
        acao = random.choice(["ok", "erro", "sim", "nao"])
        
        # Simples
        dados.append({"pt": f"se {nome} {op_str} {val} entao mostre {acao}",
                      "portugol": f"se ( {nome} {op_sym} {val} ) entao escreva ( '{acao}' )"})
        
        # Com Senao
        dados.append({"pt": f"se {nome} {op_str} {val} mostre sim senao mostre nao",
                      "portugol": f"se ( {nome} {op_sym} {val} ) entao escreva ( 'sim' ) senao escreva ( 'nao' )"})

    random.shuffle(dados)
    CAMINHO_DATASET.parent.mkdir(parents=True, exist_ok=True)
    with open(CAMINHO_DATASET, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

    print(f"[OK] Dataset expandido gerado: {len(dados)} exemplos")


if __name__ == "__main__":
    gerar_dataset()