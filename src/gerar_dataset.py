import json
import random
import os

def gerar_dataset():
    dados = []

    verbos_print = ["escreva", "mostre", "imprima", "exiba"]
    textos = ["ola mundo", "bom dia", "teste", "sucesso", "bem vindo", "erro no sistema"]
    for _ in range(150):
        v = random.choice(verbos_print)
        t = random.choice(textos)
        dados.append({"pt": f"{v} {t}", "portugol": f"escreva ( '{t}' )"})

    for _ in range(200):
        v = random.choice(verbos_print)
        n = str(random.randint(0, 100))
        pt = f"{v} o numero {n}" if random.choice([True, False]) else f"{v} {n}"
        dados.append({"pt": pt, "portugol": f"escreva ( {n} )"})

    verbos_var = ["crie a variavel", "defina", "faca", "declare", "inicie"]
    nomes_vars = ["x", "y", "z", "a", "b", "contador", "total", "idade", "nota", "peso"]
    ligacoes = ["como", "igual a", "recebendo", "valendo"]
    for _ in range(250):
        v = random.choice(verbos_var)
        nome = random.choice(nomes_vars)
        valor = str(random.randint(0, 100))
        ligacao = random.choice(ligacoes)
        dados.append({"pt": f"{v} {nome} {ligacao} {valor}", "portugol": f"inteiro {nome} = {valor}"})

    for _ in range(150):
        v1 = random.choice(nomes_vars)
        v2 = random.choice(nomes_vars)
        if v1 != v2:
            pt = f"some {v1} com {v2}" if random.choice([True, False]) else f"{v1} mais {v2}"
            dados.append({"pt": pt, "portugol": f"{v1} + {v2}"})

    verbos_loop = ["repita", "faca um loop de", "itere"]
    for _ in range(150):
        n = str(random.randint(1, 50))
        v = random.choice(verbos_loop)
        dados.append({"pt": f"{v} {n} vezes", "portugol": f"para i de 1 ate {n} faca"})

    verbos_cond = ["se", "caso"]
    for _ in range(150):
        v = random.choice(verbos_cond)
        nome = random.choice(nomes_vars)
        valor = str(random.randint(0, 100))
        dados.append({"pt": f"{v} {nome} for maior que {valor}", "portugol": f"se ( {nome} > {valor} ) entao"})

    random.shuffle(dados)

    # Cria a pasta dataset se não existir
    os.makedirs("../dataset", exist_ok=True)
    
    with open("../dataset/dados.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

    print(f"✅ Novo dataset gerado com sucesso: {len(dados)} exemplos diferentes!")

if __name__ == "__main__":
    gerar_dataset()