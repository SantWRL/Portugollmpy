import re
import unicodedata


class InterpretadorPortugol:
    def __init__(self):
        self.variaveis = {}

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _resolver(self, token):
        if token.lstrip('-').isdigit():
            return int(token)
        if token in self.variaveis:
            return self.variaveis[token]
        raise KeyError(token)

    def _calcular(self, v1, op, v2):
        a, b = self._resolver(v1), self._resolver(v2)
        if   op == '+': return a + b
        elif op == '-': return a - b
        elif op == '*': return a * b
        elif op == '/':
            if b == 0: raise ZeroDivisionError
            r = a / b
            return int(r) if r == int(r) else round(r, 4)

    # ── Execucao ──────────────────────────────────────────────────────────────
    def executar(self, codigo):
        codigo = codigo.strip()

        # Declaracao: inteiro x = 10
        m = re.match(r"inteiro\s+(\w+)\s*=\s*(-?\d+)", codigo)
        if m:
            nome, valor = m.group(1), int(m.group(2))
            self.variaveis[nome] = valor
            print(f"[Var] '{nome}' = {valor}")
            return

        # Escreva string: escreva ( 'texto' )
        m = re.match(r"escreva\s*\(\s*'(.*?)'\s*\)", codigo)
        if m:
            print(f"[Out] {m.group(1)}")
            return

        # Escreva numero/variavel: escreva ( x )
        m = re.match(r"escreva\s*\(\s*(\w+)\s*\)", codigo)
        if m:
            alvo = m.group(1)
            try:
                print(f"[Out] {self._resolver(alvo)}")
            except KeyError:
                print(f"[Erro] Variavel '{alvo}' nao existe.")
            return

        # Leia: leia ( x )
        m = re.match(r"leia\s*\(\s*(\w+)\s*\)", codigo)
        if m:
            nome = m.group(1)
            try:
                self.variaveis[nome] = int(input(f"[In] Valor para '{nome}': "))
                print(f"[Var] '{nome}' = {self.variaveis[nome]}")
            except ValueError:
                print("[Erro] Digite um numero inteiro.")
            return

        # Reatribuicao com expressao: x = y + 5  /  x = x + 1
        m = re.match(r"(\w+)\s*=\s*(\w+)\s*([+\-*/])\s*(\w+)", codigo)
        if m:
            dest, v1, op, v2 = m.group(1), m.group(2), m.group(3), m.group(4)
            try:
                resultado = self._calcular(v1, op, v2)
                self.variaveis[dest] = resultado
                print(f"[Var] '{dest}' = {resultado}")
            except KeyError as e:
                print(f"[Erro] Variavel '{e.args[0]}' nao existe.")
            except ZeroDivisionError:
                print("[Erro] Divisao por zero.")
            return

        # Operacao aritmetica simples: x + y
        m = re.match(r"(\w+)\s*([+\-*/])\s*(\w+)", codigo)
        if m:
            v1, op, v2 = m.group(1), m.group(2), m.group(3)
            ops = {'+': 'soma', '-': 'subtracao', '*': 'multiplicacao', '/': 'divisao'}
            try:
                print(f"[Calc] {ops[op]} de {v1} {op} {v2} = {self._calcular(v1, op, v2)}")
            except KeyError as e:
                print(f"[Erro] Variavel '{e.args[0]}' nao existe.")
            except ZeroDivisionError:
                print("[Erro] Divisao por zero.")
            return

        # Loop para: para i de 1 ate N faca
        m = re.match(r"para i de 1 ate (\d+) faca", codigo)
        if m:
            n = int(m.group(1))
            print(f"[Loop] Repetindo {n} vezes...")
            for i in range(1, n + 1):
                print(f"  -> Execucao {i}")
            return

        # Loop enquanto: enquanto ( x < 10 ) faca
        m = re.match(r"enquanto\s*\(\s*(\w+)\s*(>=|<=|!=|==|>|<)\s*(\w+)\s*\)\s*faca", codigo)
        if m:
            var, op_str, lim_tok = m.group(1), m.group(2), m.group(3)
            ops_cond = {
                '>':  lambda a, b: a > b,  '<':  lambda a, b: a < b,
                '>=': lambda a, b: a >= b, '<=': lambda a, b: a <= b,
                '==': lambda a, b: a == b, '!=': lambda a, b: a != b,
            }
            try:
                lim   = self._resolver(lim_tok)
                val   = self.variaveis.get(var, 0)
                iters = 0
                print(f"[Loop] enquanto {var} {op_str} {lim}:")
                while ops_cond[op_str](val, lim) and iters < 100:
                    iters += 1
                    print(f"  -> Iteracao {iters} ({var} = {val})")
                    val += 1   # incremento padrao para evitar loop infinito
                if iters == 100:
                    print("  [Aviso] Limite de 100 iteracoes atingido.")
            except KeyError as e:
                print(f"[Erro] Variavel '{e.args[0]}' nao existe.")
            return

        # Condicionais: se ( x > 10 ) entao
        ops_cond = {
            '>=': lambda a, b: a >= b, '<=': lambda a, b: a <= b,
            '!=': lambda a, b: a != b, '==': lambda a, b: a == b,
            '>':  lambda a, b: a > b,  '<':  lambda a, b: a < b,
        }
        m = re.match(r"se\s*\(\s*(\w+)\s*(>=|<=|!=|==|>|<)\s*(\w+)\s*\)\s*entao", codigo)
        if m:
            esq, op_str, dir_ = m.group(1), m.group(2), m.group(3)
            try:
                ve, vd = self._resolver(esq), self._resolver(dir_)
                estado = "VERDADEIRA" if ops_cond[op_str](ve, vd) else "FALSA"
                print(f"[Cond] {estado}: {esq}={ve} {op_str} {dir_}={vd}")
            except KeyError as e:
                print(f"[Erro] Variavel '{e.args[0]}' nao existe.")
            return

        print(f"[?] Nao sei executar: '{codigo}'")