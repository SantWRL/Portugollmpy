import re

class InterpretadorPortugol:
    def __init__(self):
        self.variaveis = {}

    def executar(self, codigo):
        codigo = codigo.strip()

        # Atribuição: inteiro x = 10
        match_var = re.match(r"inteiro\s+(\w+)\s*=\s*(\d+)", codigo)
        if match_var:
            nome = match_var.group(1)
            valor = int(match_var.group(2))
            self.variaveis[nome] = valor
            print(f"⚙️  [Interpretador]: Variável '{nome}' criada com o valor {valor}.")
            return

        # Escreva String: escreva ( 'ola mundo' )
        match_escreva_str = re.match(r"escreva\s*\(\s*'(.*?)'\s*\)", codigo)
        if match_escreva_str:
            texto = match_escreva_str.group(1)
            print(f"💻 [Terminal]: {texto}")
            return

        # Escreva Número/Variável: escreva ( 5 ) ou escreva ( x )
        match_escreva_num = re.match(r"escreva\s*\(\s*(\w+)\s*\)", codigo)
        if match_escreva_num:
            alvo = match_escreva_num.group(1)
            if alvo.isdigit():
                print(f"💻 [Terminal]: {alvo}")
            elif alvo in self.variaveis:
                print(f"💻 [Terminal]: {self.variaveis[alvo]}")
            else:
                print(f"❌ [Erro]: Variável '{alvo}' não existe na memória!")
            return

        # Soma: x + y
        match_soma = re.match(r"(\w+)\s*\+\s*(\w+)", codigo)
        if match_soma:
            v1, v2 = match_soma.groups()
            val1 = self.variaveis.get(v1, 0) if not v1.isdigit() else int(v1)
            val2 = self.variaveis.get(v2, 0) if not v2.isdigit() else int(v2)
            print(f"⚙️  [Interpretador]: O resultado de {v1} + {v2} é {val1 + val2}")
            return

        # Loop: para i de 1 ate X faca
        match_loop = re.match(r"para i de 1 ate (\d+) faca", codigo)
        if match_loop:
            vezes = int(match_loop.group(1))
            print(f"⚙️  [Interpretador]: Iniciando repetição de {vezes} passos...")
            for i in range(1, vezes + 1):
                print(f"   🔄 Execução {i}")
            return

        # Condição: se ( x > 10 ) entao
        match_se = re.match(r"se\s*\(\s*(\w+)\s*>\s*(\d+)\s*\)\s*entao", codigo)
        if match_se:
            var = match_se.group(1)
            limite = int(match_se.group(2))
            valor_atual = self.variaveis.get(var, 0)
            
            if valor_atual > limite:
                print(f"⚙️  [Interpretador]: Condição VERDADEIRA ({var} = {valor_atual} > {limite}).")
            else:
                print(f"⚙️  [Interpretador]: Condição FALSA ({var} = {valor_atual} NÃO > {limite}).")
            return

        print(f"⚠️ [Interpretador]: Não sei como executar '{codigo}'.")