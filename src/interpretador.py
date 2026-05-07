import re
import unicodedata


class InterpretadorPortugol:
    def __init__(self):
        self.variaveis = {}
        self.output = []

    def transpolar_linha(self, codigo):
        """Converte uma linha de Portugol para Python."""
        linha = codigo.strip().lower()
        if not linha: return ""

        # 0. Easter Egg: Saudações
        if linha in ["oi", "ola", "ola!", "oi!", "hello"]:
            return "print('Olá! Eu sou o Tupi-Logic. Em que posso ajudar no seu código?')"

        # 1. Declaracao: inteiro x = 10 -> x = 10
        m = re.match(r"(inteiro|real)\s+(\w+)\s*=\s*(.*)", linha)
        if m:
            tipo, nome, valor = m.groups()
            return f"{nome} = {valor}"

        # 2. Escreva: escreva ( 'oi' ) -> print ( 'oi' )
        m = re.match(r"escreva\s*\(\s*(.*?)\s*\)", linha)
        if m:
            alvo = m.group(1)
            if "=" in alvo and not ("'" in alvo or '"' in alvo):
                return f"# Erro: Nao use '=' dentro de escreva. Use 'inteiro {alvo.split('=')[0].strip()} = ...' primeiro."
            return f"print({alvo})"

        # 3. Leia: leia ( x ) -> x = input()
        m = re.match(r"leia\s*\(\s*(\w+)\s*\)", linha)
        if m:
            nome = m.group(1)
            return f"{nome} = float(input()) if '.' in (val := input()) else int(val)"

        # 4. Condicional: se ( cond ) entao acao [senao acao]
        m = re.match(r"se\s*\(\s*(.*?)\s*\)\s*entao\s+(.*?)(?:\s+senao\s+(.*))?$", linha)
        if m:
            cond, acao_entao, acao_senao = m.groups()
            py_cond = cond.replace("==", "==").replace("!=", "!=").replace("<=", "<=").replace(">=", ">=")
            if "=" in py_cond and "==" not in py_cond and "!=" not in py_cond and "<=" not in py_cond and ">=" not in py_cond:
                py_cond = py_cond.replace("=", "==")
            
            py_entao = self.transpolar_linha(acao_entao)
            res = f"if {py_cond}:\n    {py_entao}"
            if acao_senao:
                py_senao = self.transpolar_linha(acao_senao)
                res += f"\nelse:\n    {py_senao}"
            return res

        # 5. Loop enquanto: enquanto ( x < 10 ) faca acao
        m = re.match(r"enquanto\s*\(\s*(.*?)\s*\)\s*faca\s+(.*)", linha)
        if m:
            cond, acao = m.groups()
            py_cond = cond.replace("=", "==") if "=" in cond and "==" not in cond else cond
            py_acao = self.transpolar_linha(acao)
            return f"while {py_cond}:\n    {py_acao}\n    if len(getattr(self, 'loop_safety', [])) > 100: break\n    self.loop_safety.append(1)"

        # 6. Loop para: para i de 1 ate N faca
        m = re.match(r"para\s+(\w+)\s+de\s+(\d+)\s+ate\s+(\d+)\s+faca", linha)
        if m:
            var, start, end = m.groups()
            return f"for {var} in range({start}, {end} + 1): print(f'[Exec] Iteracao {{{var}}}')"

        # 7. Atribuicao generica: x = y + 1
        if "=" in linha:
            return linha

        # 8. Operacao solta: x + 1 -> print(x + 1)
        if any(op in linha for op in "+-*/") and "=" not in linha:
            return f"print({linha})"

        return f"# {linha} (Nao reconhecido)"

    def executar(self, codigo):
        self.output = []
        self.loop_safety = [] # Evita loops infinitos acidentais
        py_code = self.transpolar_linha(codigo)
        
        # LOG DE DEBUG (Aparece no seu terminal)
        print(f"\n[DEBUG] Portugol: {codigo}")
        print(f"[DEBUG] Python: \n{py_code}\n")

        if not py_code or py_code.startswith("#"):
            self.output.append(f"[?] Nao entendi ou nao sei transpolar: '{codigo}'")
            return self.output

        import io
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        try:
            with redirect_stdout(f):
                # Executa no contexto das nossas variaveis
                exec(py_code, {"__builtins__": __builtins__, "self": self}, self.variaveis)
            
            self.variaveis.pop('__builtins__', None)
            self.variaveis.pop('self', None)
            
            out = f.getvalue().strip()
            if out:
                for line in out.split('\n'):
                    self.output.append(f"[Out] {line}")
            else:
                self.output.append(f"[Exec] OK")
                
        except NameError as e:
            var_name = str(e).split("'")[1] if "'" in str(e) else str(e)
            self.output.append(f"[Erro] Variável '{var_name}' não existe. Tente criá-la com 'crie a variável {var_name} como 0'.")
            print(f"[ERRO] NameError: {e}")
        except SyntaxError as e:
            self.output.append(f"[Erro] Sintaxe inválida no comando. Verifique parênteses ou aspas.")
            print(f"[ERRO] SyntaxError: {e}")
        except Exception as e:
            print(f"[ERRO] Erro na execucao Python: {e}")
            self.output.append(f"[Erro] Falha técnica: {e}")
            
        return self.output