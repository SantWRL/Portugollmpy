import torch
import torch.nn as nn

class Codificador(nn.Module):
    def __init__(self, tam_vocab, tam_embedding, tam_oculto):
        super(Codificador, self).__init__()
        self.embedding = nn.Embedding(tam_vocab, tam_embedding)
        self.rnn = nn.GRU(tam_embedding, tam_oculto, batch_first=True)

    def forward(self, x):
        embs = self.embedding(x)
        _, oculto = self.rnn(embs)
        return oculto

class Decodificador(nn.Module):
    def __init__(self, tam_vocab, tam_embedding, tam_oculto):
        super(Decodificador, self).__init__()
        self.embedding = nn.Embedding(tam_vocab, tam_embedding)
        self.rnn = nn.GRU(tam_embedding, tam_oculto, batch_first=True)
        self.fc = nn.Linear(tam_oculto, tam_vocab)

    def forward(self, x, oculto):
        x = x.unsqueeze(1)
        embs = self.embedding(x)
        saida, oculto = self.rnn(embs, oculto)
        previsao = self.fc(saida.squeeze(1))
        return previsao, oculto

class TupiLogicSeq2Seq(nn.Module):
    def __init__(self, codificador, decodificador):
        super(TupiLogicSeq2Seq, self).__init__()
        self.codificador = codificador
        self.decodificador = decodificador

    def forward(self, fonte, alvo, forcar_ensino=0.5):
        tamanho_lote = fonte.shape[0]
        tamanho_max_alvo = alvo.shape[1]
        tam_vocab_alvo = self.decodificador.fc.out_features

        previsoes = torch.zeros(tamanho_lote, tamanho_max_alvo, tam_vocab_alvo).to(fonte.device)
        
        oculto = self.codificador(fonte)
        entrada = alvo[:, 0]
        
        for t in range(1, tamanho_max_alvo):
            previsao, oculto = self.decodificador(entrada, oculto)
            previsoes[:, t] = previsao
            
            melhor_palavra = previsao.argmax(1) 
            
            import random
            entrada = alvo[:, t] if random.random() < forcar_ensino else melhor_palavra
            
        return previsoes