import random
import torch
import torch.nn as nn
from config import FORCAR_ENSINO, DROPOUT


# ── A. Mecanismo de Atencao de Bahdanau ──────────────────────────────────────
class Atencao(nn.Module):
    """Calcula pesos de atencao sobre todas as saidas do encoder."""
    def __init__(self, tam_oculto):
        super().__init__()
        # Encoder bidirecional => saidas com dim tam_oculto*2
        self.attn = nn.Linear(tam_oculto * 3, tam_oculto)
        self.v    = nn.Linear(tam_oculto, 1, bias=False)

    def forward(self, oculto, saidas_enc):
        # oculto:     (1, batch, H)
        # saidas_enc: (batch, src_len, H*2)
        src_len    = saidas_enc.shape[1]
        oculto_exp = oculto.squeeze(0).unsqueeze(1).repeat(1, src_len, 1)
        energia    = torch.tanh(self.attn(torch.cat([oculto_exp, saidas_enc], dim=2)))
        pesos      = self.v(energia).squeeze(2)
        return torch.softmax(pesos, dim=1)   # (batch, src_len)


# ── B. Encoder Bidirecional com Dropout ──────────────────────────────────────
class Codificador(nn.Module):
    def __init__(self, tam_vocab, tam_embedding, tam_oculto, dropout=DROPOUT):
        super().__init__()
        self.embedding = nn.Embedding(tam_vocab, tam_embedding, padding_idx=0)
        self.dropout   = nn.Dropout(dropout)
        # bidirectional=True: captura contexto em ambas as direcoes
        self.rnn       = nn.GRU(tam_embedding, tam_oculto,
                                batch_first=True, bidirectional=True)
        # Projeta (forward + backward) -> tam_oculto para o decoder
        self.fc_oculto = nn.Linear(tam_oculto * 2, tam_oculto)

    def forward(self, x):
        embs          = self.dropout(self.embedding(x))
        saidas, oculto = self.rnn(embs)
        # saidas:  (batch, src_len, H*2)
        # oculto:  (2, batch, H) — 2 direcoes
        oculto = torch.tanh(
            self.fc_oculto(torch.cat([oculto[0], oculto[1]], dim=1))
        ).unsqueeze(0)                          # (1, batch, H)
        return saidas, oculto


# ── C. Decoder com Atencao e Dropout ─────────────────────────────────────────
class Decodificador(nn.Module):
    def __init__(self, tam_vocab, tam_embedding, tam_oculto, dropout=DROPOUT):
        super().__init__()
        self.embedding = nn.Embedding(tam_vocab, tam_embedding, padding_idx=0)
        self.dropout   = nn.Dropout(dropout)
        self.atencao   = Atencao(tam_oculto)
        # GRU recebe: embedding + contexto de atencao (H*2)
        self.rnn = nn.GRU(tam_embedding + tam_oculto * 2, tam_oculto, batch_first=True)
        # Saida final: hidden + contexto + embedding (conexao residual)
        self.fc  = nn.Linear(tam_oculto + tam_oculto * 2 + tam_embedding, tam_vocab)

    def forward(self, x, oculto, saidas_enc):
        x    = x.unsqueeze(1)
        embs = self.dropout(self.embedding(x))          # (batch, 1, emb)

        pesos    = self.atencao(oculto, saidas_enc).unsqueeze(1)  # (batch,1,src)
        contexto = torch.bmm(pesos, saidas_enc)                   # (batch,1,H*2)

        saida, oculto = self.rnn(torch.cat([embs, contexto], dim=2), oculto)

        previsao = self.fc(torch.cat([
            saida.squeeze(1),
            contexto.squeeze(1),
            embs.squeeze(1)
        ], dim=1))                                       # (batch, vocab)

        return previsao, oculto, pesos.squeeze(1)


# ── D. Seq2Seq ────────────────────────────────────────────────────────────────
class TupiLogicSeq2Seq(nn.Module):
    def __init__(self, codificador, decodificador):
        super().__init__()
        self.codificador   = codificador
        self.decodificador = decodificador

    def forward(self, fonte, alvo, forcar_ensino=FORCAR_ENSINO):
        batch         = fonte.shape[0]
        max_alvo      = alvo.shape[1]
        tam_vocab     = self.decodificador.fc.out_features
        previsoes     = torch.zeros(batch, max_alvo, tam_vocab).to(fonte.device)

        saidas_enc, oculto = self.codificador(fonte)
        entrada = alvo[:, 0]

        for t in range(1, max_alvo):
            previsao, oculto, _ = self.decodificador(entrada, oculto, saidas_enc)
            previsoes[:, t]     = previsao
            melhor              = previsao.argmax(1)
            entrada = alvo[:, t] if random.random() < forcar_ensino else melhor

        return previsoes