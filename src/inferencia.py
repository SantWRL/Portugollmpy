import unicodedata
import torch
from vocabulario import Vocabulario
from modelo import Codificador, Decodificador, TupiLogicSeq2Seq
from interpretador import InterpretadorPortugol
from config import (
    CAMINHO_MODELO_BEST, CAMINHO_MODELO,
    TAM_EMBEDDING, TAM_OCULTO, DROPOUT,
    MAX_SAIDA, BEAM_WIDTH
)


# ── J. Normalizacao de entrada ────────────────────────────────────────────────
def normalizar(frase):
    """Lowercases e remove acentos para maior robustez."""
    frase = frase.lower().strip()
    frase = unicodedata.normalize('NFD', frase)
    return ''.join(c for c in frase if unicodedata.category(c) != 'Mn')


def carregar_modelo(caminho):
    checkpoint = torch.load(caminho, weights_only=False)

    vocab_pt = Vocabulario()
    vocab_pt.stoi = checkpoint['vocab_pt_stoi']
    vocab_pt.itos = checkpoint['vocab_pt_itos']
    vocab_pt.idx  = checkpoint.get('vocab_pt_idx', len(vocab_pt.stoi))

    vocab_portugol = Vocabulario()
    vocab_portugol.stoi = checkpoint['vocab_portugol_stoi']
    vocab_portugol.itos = checkpoint['vocab_portugol_itos']
    vocab_portugol.idx  = checkpoint.get('vocab_portugol_idx', len(vocab_portugol.stoi))

    enc    = Codificador(len(vocab_pt),       TAM_EMBEDDING, TAM_OCULTO, DROPOUT)
    dec    = Decodificador(len(vocab_portugol), TAM_EMBEDDING, TAM_OCULTO, DROPOUT)
    modelo = TupiLogicSeq2Seq(enc, dec)
    modelo.load_state_dict(checkpoint['modelo_state_dict'])
    modelo.eval()

    return modelo, vocab_pt, vocab_portugol


# ── C. Beam Search ────────────────────────────────────────────────────────────
def traduzir_com_beam(frase, modelo, vocab_pt, vocab_portugol, beam_width=BEAM_WIDTH):
    """Gera Portugol usando Beam Search (melhor que greedy argmax)."""
    modelo.eval()
    with torch.no_grad():
        tokens      = vocab_pt.codificar(normalizar(frase))
        tensor_font = torch.tensor(tokens).unsqueeze(0)

        saidas_enc, oculto_ini = modelo.codificador(tensor_font)

        SOS = vocab_portugol.stoi["<SOS>"]
        EOS = vocab_portugol.stoi["<EOS>"]

        # Cada beam: (log_prob_acumulada, lista_tokens, oculto)
        beams      = [(0.0, [SOS], oculto_ini)]
        concluidos = []

        for _ in range(MAX_SAIDA):
            if not beams:
                break
            novos = []
            for log_prob, seq, oculto in beams:
                if seq[-1] == EOS:
                    concluidos.append((log_prob, seq))
                    continue
                entrada  = torch.tensor([seq[-1]])
                prev, novo_oculto, _ = modelo.decodificador(entrada, oculto, saidas_enc)
                lp       = torch.log_softmax(prev, dim=1)
                topk_p, topk_i = lp.topk(beam_width)
                for p, idx in zip(topk_p[0].tolist(), topk_i[0].tolist()):
                    novos.append((log_prob + p, seq + [idx], novo_oculto))

            beams = sorted(novos, key=lambda x: x[0], reverse=True)[:beam_width]

        concluidos += [(lp, seq) for lp, seq, _ in beams]

        if not concluidos:
            return ""
        _, melhor = max(concluidos, key=lambda x: x[0])
        melhor = [t for t in melhor if t not in (SOS, EOS)]
        return vocab_portugol.decodificar(melhor)


if __name__ == "__main__":
    # Tenta o melhor modelo primeiro, senao usa o final
    caminho = CAMINHO_MODELO_BEST if CAMINHO_MODELO_BEST.exists() else CAMINHO_MODELO

    print("[INFO] Carregando modelo...")
    try:
        modelo, vocab_pt, vocab_portugol = carregar_modelo(caminho)
        if caminho == CAMINHO_MODELO_BEST:
            print("[OK] Usando modelo com melhor val loss.")
    except FileNotFoundError:
        print(f"[ERRO] Modelo nao encontrado em: {caminho}")
        print("       Execute: python gerar_dataset.py && python treinar.py")
        exit(1)

    interpretador = InterpretadorPortugol()
    print("\n--- Tupi-Logic IA: Assistente e Execucao ---")
    print("   (Beam Search + Atencao + Encoder Bidirecional)")
    print("Digite 'sair' para encerrar.\n")

    while True:
        try:
            prompt = input("Usuario (Portugues): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando...")
            break

        if not prompt:
            continue
        if prompt.lower() == 'sair':
            print("Ate mais!")
            break

        resultado = traduzir_com_beam(prompt, modelo, vocab_pt, vocab_portugol)
        print(f"IA (Portugol): {resultado}")
        print("-" * 40)
        interpretador.executar(resultado)
        print("-" * 40 + "\n")