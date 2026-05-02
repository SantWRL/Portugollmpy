import json
import random
from config import CAMINHO_DATASET


def gerar_dataset():
    dados = []

    nomes_vars   = ["x", "y", "z", "a", "b", "contador", "total", "idade", "nota", "peso"]
    verbos_print = ["escreva", "mostre", "imprima", "exiba", "apresente", "exporte"]
    verbos_var   = ["crie a variavel", "defina", "faca", "declare", "inicie",
                    "estabeleca", "atribua"]
    ligacoes     = ["como", "igual a", "recebendo", "valendo", "sendo", "com o valor"]
    verbos_loop  = ["repita", "faca um loop de", "itere", "execute", "cicle"]
    verbos_cond  = ["se", "caso", "verifique se", "teste se"]

    # 1. Print texto
    textos = ["ola mundo", "bom dia", "teste", "sucesso", "bem vindo",
              "erro no sistema", "concluido", "inicio", "parado", "ok"]
    for _ in range(150):
        dados.append({"pt": f"{random.choice(verbos_print)} {random.choice(textos)}",
                      "portugol": f"escreva ( '{random.choice(textos)}' )"})

    # 2. Print numero
    for _ in range(200):
        n = str(random.randint(0, 100))
        pt = f"{random.choice(verbos_print)} o numero {n}" if random.random() > .5 \
             else f"{random.choice(verbos_print)} {n}"
        dados.append({"pt": pt, "portugol": f"escreva ( {n} )"})

    # 3. Declaracao de variavel
    for _ in range(250):
        nome, valor = random.choice(nomes_vars), str(random.randint(0, 100))
        dados.append({"pt": f"{random.choice(verbos_var)} {nome} {random.choice(ligacoes)} {valor}",
                      "portugol": f"inteiro {nome} = {valor}"})

    # 4. Soma
    for _ in range(150):
        v1, v2 = random.sample(nomes_vars, 2)
        t = random.choice([f"some {v1} com {v2}", f"{v1} mais {v2}",
                           f"adicione {v1} e {v2}", f"calcule {v1} mais {v2}"])
        dados.append({"pt": t, "portugol": f"{v1} + {v2}"})

    # 5. Subtracao
    for _ in range(120):
        v1, v2 = random.sample(nomes_vars, 2)
        t = random.choice([f"subtraia {v2} de {v1}", f"{v1} menos {v2}",
                           f"calcule {v1} menos {v2}", f"diminua {v2} de {v1}"])
        dados.append({"pt": t, "portugol": f"{v1} - {v2}"})

    # 6. Multiplicacao
    for _ in range(120):
        v1, v2 = random.sample(nomes_vars, 2)
        t = random.choice([f"multiplique {v1} por {v2}", f"{v1} vezes {v2}",
                           f"calcule {v1} vezes {v2}", f"produto de {v1} e {v2}"])
        dados.append({"pt": t, "portugol": f"{v1} * {v2}"})

    # 7. Divisao
    for _ in range(120):
        v1, v2 = random.sample(nomes_vars, 2)
        t = random.choice([f"divida {v1} por {v2}", f"{v1} dividido por {v2}",
                           f"quociente de {v1} por {v2}"])
        dados.append({"pt": t, "portugol": f"{v1} / {v2}"})

    # 8. Leia
    verbos_leia = ["leia", "obtenha", "capture", "leia a variavel"]
    for _ in range(100):
        nome = random.choice(nomes_vars)
        t = random.choice([f"{random.choice(verbos_leia)} {nome}",
                           f"leia o valor de {nome}",
                           f"obtenha {nome} do usuario",
                           f"peca ao usuario o valor de {nome}"])
        dados.append({"pt": t, "portugol": f"leia ( {nome} )"})

    # 9. Reatribuicao: x = x + 1
    verbos_incr = ["incremente", "aumente", "some 1 a", "adicione 1 a"]
    verbos_decr = ["decremente", "diminua", "subtraia 1 de"]
    for _ in range(120):
        nome = random.choice(nomes_vars)
        n    = str(random.randint(1, 10))
        # incremento
        dados.append({"pt": random.choice([
            f"incremente {nome} em {n}",
            f"aumente {nome} de {n}",
            f"adicione {n} a {nome}"]),
            "portugol": f"{nome} = {nome} + {n}"})
        # decremento
        dados.append({"pt": random.choice([
            f"decremente {nome} em {n}",
            f"diminua {nome} de {n}",
            f"subtraia {n} de {nome}"]),
            "portugol": f"{nome} = {nome} - {n}"})

    # 10. Loop para
    for _ in range(150):
        n = str(random.randint(1, 50))
        dados.append({"pt": f"{random.choice(verbos_loop)} {n} vezes",
                      "portugol": f"para i de 1 ate {n} faca"})

    # 11. Loop enquanto
    ops_map = {"menor que": "<", "maior que": ">", "igual a": "==",
               "diferente de": "!=", "menor ou igual a": "<=", "maior ou igual a": ">="}
    for _ in range(100):
        nome = random.choice(nomes_vars)
        val  = str(random.randint(0, 20))
        op_str, op_sym = random.choice(list(ops_map.items()))
        t = random.choice([
            f"repita enquanto {nome} for {op_str} {val}",
            f"faca um loop enquanto {nome} {op_str} {val}",
            f"enquanto {nome} for {op_str} {val} continue"])
        dados.append({"pt": t, "portugol": f"enquanto ( {nome} {op_sym} {val} ) faca"})

    # 12. Condicionais: >
    for _ in range(150):
        nome, val = random.choice(nomes_vars), str(random.randint(0, 100))
        dados.append({"pt": f"{random.choice(verbos_cond)} {nome} for maior que {val}",
                      "portugol": f"se ( {nome} > {val} ) entao"})

    # 13. Condicionais: <
    for _ in range(100):
        nome, val = random.choice(nomes_vars), str(random.randint(0, 100))
        dados.append({"pt": f"{random.choice(verbos_cond)} {nome} for menor que {val}",
                      "portugol": f"se ( {nome} < {val} ) entao"})

    # 14. Condicionais: ==
    for _ in range(100):
        nome, val = random.choice(nomes_vars), str(random.randint(0, 100))
        dados.append({"pt": f"{random.choice(verbos_cond)} {nome} for igual a {val}",
                      "portugol": f"se ( {nome} == {val} ) entao"})

    # 15. Condicionais: !=
    for _ in range(80):
        nome, val = random.choice(nomes_vars), str(random.randint(0, 100))
        dados.append({"pt": f"{random.choice(verbos_cond)} {nome} for diferente de {val}",
                      "portugol": f"se ( {nome} != {val} ) entao"})

    random.shuffle(dados)

    CAMINHO_DATASET.parent.mkdir(parents=True, exist_ok=True)
    with open(CAMINHO_DATASET, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

    print(f"[OK] Dataset gerado: {len(dados)} exemplos")
    print(f"     Salvo em: {CAMINHO_DATASET}")


if __name__ == "__main__":
    gerar_dataset()