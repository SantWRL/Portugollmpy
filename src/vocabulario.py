class Vocabulario:
    def __init__(self):
        # Tokens especiais: <PAD> (preenchimento), <SOS> (início), <EOS> (fim), <UNK> (desconhecido)
        self.stoi = {"<PAD>": 0, "<SOS>": 1, "<EOS>": 2, "<UNK>": 3}
        self.itos = {0: "<PAD>", 1: "<SOS>", 2: "<EOS>", 3: "<UNK>"}
        self.idx = 4

    def adicionar_frase(self, frase):
        for palavra in frase.split():
            if palavra not in self.stoi:
                self.stoi[palavra] = self.idx
                self.itos[self.idx] = palavra
                self.idx += 1

    def codificar(self, frase):
        # Transforma texto em números, adicionando as tags de início e fim
        tokens = [self.stoi.get(palavra, self.stoi["<UNK>"]) for palavra in frase.split()]
        return [self.stoi["<SOS>"]] + tokens + [self.stoi["<EOS>"]]

    def decodificar(self, tokens):
        # Transforma números de volta em texto
        palavras = []
        for token in tokens:
            if token == self.stoi["<EOS>"]:
                break
            if token not in [self.stoi["<SOS>"], self.stoi["<PAD>"]]:
                palavras.append(self.itos.get(token, "<UNK>"))
        return " ".join(palavras)

    def __len__(self):
        return len(self.stoi)