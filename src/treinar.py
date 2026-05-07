import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset, random_split

from vocabulario import Vocabulario
from modelo import Codificador, Decodificador, TupiLogicSeq2Seq
from config import (
    CAMINHO_DATASET, CAMINHO_MODELO, CAMINHO_MODELO_BEST,
    TAM_EMBEDDING, TAM_OCULTO, DROPOUT,
    EPOCAS, LR, BATCH_SIZE, LOG_INTERVALO,
    MAX_NORM, VAL_SPLIT, PATIENCE
)

try:
    from tqdm import tqdm
    USA_TQDM = True
except ImportError:
    USA_TQDM = False
    print("Instale tqdm: pip install tqdm")


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def preencher_lote(seqs, pad_idx):
    max_len = max(len(s) for s in seqs)
    return [s + [pad_idx] * (max_len - len(s)) for s in seqs]


def avaliar(modelo, loader, criterio):
    """Calcula a perda media no conjunto de validacao (sem teacher forcing)."""
    modelo.eval()
    total = 0.0
    with torch.no_grad():
        for fonte, alvo in loader:
            fonte, alvo = fonte.to(device), alvo.to(device)
            saida = modelo(fonte, alvo, forcar_ensino=0.0)
            total += criterio(
                saida[:, 1:].reshape(-1, saida.shape[-1]),
                alvo[:, 1:].reshape(-1)
            ).item()
    return total / len(loader)


def treinar():
    # ── 1. Dados ──────────────────────────────────────────────────────────────
    with open(CAMINHO_DATASET, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # ── 2. Vocabularios ───────────────────────────────────────────────────────
    vocab_pt       = Vocabulario()
    vocab_portugol = Vocabulario()
    for item in dados:
        vocab_pt.adicionar_frase(item["pt"])
        vocab_portugol.adicionar_frase(item["portugol"])

    # ── 3. Tensores ───────────────────────────────────────────────────────────
    fonte_t = torch.tensor(preencher_lote(
        [vocab_pt.codificar(d["pt"]) for d in dados], vocab_pt.stoi["<PAD>"]))
    alvo_t  = torch.tensor(preencher_lote(
        [vocab_portugol.codificar(d["portugol"]) for d in dados], vocab_portugol.stoi["<PAD>"]))

    # ── 4. Train / Validation Split (80/20) ───────────────────────────────────
    dataset = TensorDataset(fonte_t, alvo_t)
    n_val   = int(len(dataset) * VAL_SPLIT)
    n_train = len(dataset) - n_val
    ds_train, ds_val = random_split(dataset, [n_train, n_val],
                                    generator=torch.Generator().manual_seed(42))

    loader_train = DataLoader(ds_train, batch_size=BATCH_SIZE, shuffle=True)
    loader_val   = DataLoader(ds_val,   batch_size=BATCH_SIZE)

    # ── 5. Modelo ─────────────────────────────────────────────────────────────
    enc   = Codificador(len(vocab_pt),       TAM_EMBEDDING, TAM_OCULTO, DROPOUT)
    dec   = Decodificador(len(vocab_portugol), TAM_EMBEDDING, TAM_OCULTO, DROPOUT)
    modelo = TupiLogicSeq2Seq(enc, dec).to(device)

    otimizador = optim.Adam(modelo.parameters(), lr=LR)
    criterio   = nn.CrossEntropyLoss(ignore_index=vocab_portugol.stoi["<PAD>"])
    scheduler  = optim.lr_scheduler.ReduceLROnPlateau(
        otimizador, mode='min', patience=20, factor=0.5)

    print("[INFO] Iniciando treinamento...")
    print(f"       Treino: {n_train} | Val: {n_val} | Batch: {BATCH_SIZE} | Epocas: {EPOCAS}\n")

    melhor_val       = float('inf')
    epocas_sem_melho = 0
    epocas_iter      = tqdm(range(EPOCAS), desc="Epocas") if USA_TQDM else range(EPOCAS)

    for epoca in epocas_iter:
        # ── Treino ────────────────────────────────────────────────────────────
        modelo.train()
        perda_treino = 0.0
        for fonte_b, alvo_b in loader_train:
            fonte_b, alvo_b = fonte_b.to(device), alvo_b.to(device)
            otimizador.zero_grad()
            saida = modelo(fonte_b, alvo_b)
            perda = criterio(
                saida[:, 1:].reshape(-1, saida.shape[-1]),
                alvo_b[:, 1:].reshape(-1)
            )
            perda.backward()
            # E. Gradient Clipping
            torch.nn.utils.clip_grad_norm_(modelo.parameters(), MAX_NORM)
            otimizador.step()
            perda_treino += perda.item()
        perda_treino /= len(loader_train)

        # ── Validacao ─────────────────────────────────────────────────────────
        perda_val = avaliar(modelo, loader_val, criterio)

        # F. LR Scheduler
        scheduler.step(perda_val)

        # Atualiza progresso
        if USA_TQDM:
            epocas_iter.set_postfix({"train": f"{perda_treino:.3f}", "val": f"{perda_val:.3f}"})
        elif (epoca + 1) % LOG_INTERVALO == 0:
            print(f"Epoca [{epoca+1}/{EPOCAS}] treino={perda_treino:.4f} val={perda_val:.4f}")

        # G. Salvar melhor modelo / Early Stopping
        if perda_val < melhor_val:
            melhor_val = perda_val
            epocas_sem_melho = 0
            CAMINHO_MODELO_BEST.parent.mkdir(parents=True, exist_ok=True)
            torch.save({'modelo_state_dict': modelo.state_dict(),
                        'vocab_pt_stoi': vocab_pt.stoi, 'vocab_pt_itos': vocab_pt.itos,
                        'vocab_pt_idx': vocab_pt.idx,
                        'vocab_portugol_stoi': vocab_portugol.stoi,
                        'vocab_portugol_itos': vocab_portugol.itos,
                        'vocab_portugol_idx': vocab_portugol.idx,
                        'melhor_val_loss': melhor_val},
                       CAMINHO_MODELO_BEST)
        else:
            epocas_sem_melho += 1
            if epocas_sem_melho >= PATIENCE:
                print(f"\n[Early Stop] Sem melhora por {PATIENCE} epocas. Parando na epoca {epoca+1}.")
                break

    # ── Salvar checkpoint final ───────────────────────────────────────────────
    print("\n[INFO] Salvando modelo final...")
    CAMINHO_MODELO.parent.mkdir(parents=True, exist_ok=True)
    torch.save({'modelo_state_dict': modelo.state_dict(),
                'vocab_pt_stoi': vocab_pt.stoi, 'vocab_pt_itos': vocab_pt.itos,
                'vocab_pt_idx': vocab_pt.idx,
                'vocab_portugol_stoi': vocab_portugol.stoi,
                'vocab_portugol_itos': vocab_portugol.itos,
                'vocab_portugol_idx': vocab_portugol.idx},
               CAMINHO_MODELO)
    print(f"[OK] Melhor val loss: {melhor_val:.4f} -> {CAMINHO_MODELO_BEST.name}")
    print(f"[OK] Modelo final    -> {CAMINHO_MODELO.name}")


if __name__ == "__main__":
    treinar()