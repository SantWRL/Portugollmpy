"""config.py — Configurações centralizadas do Tupi-Logic."""
from pathlib import Path

# ── Caminhos ─────────────────────────────────────────────────────────────────
BASE_DIR            = Path(__file__).parent.parent
CAMINHO_DATASET     = BASE_DIR / "dataset" / "dados.json"
CAMINHO_MODELO      = BASE_DIR / "modelos_salvos" / "tupi_modelo.pth"
CAMINHO_MODELO_BEST = BASE_DIR / "modelos_salvos" / "tupi_melhor.pth"  # melhor val loss

# ── Arquitetura ───────────────────────────────────────────────────────────────
TAM_EMBEDDING = 64
TAM_OCULTO    = 128
DROPOUT       = 0.3   # regularização

# ── Treinamento ───────────────────────────────────────────────────────────────
EPOCAS        = 500
LR            = 0.01
BATCH_SIZE    = 64
FORCAR_ENSINO = 0.5
LOG_INTERVALO = 50
MAX_NORM      = 1.0   # gradient clipping
VAL_SPLIT     = 0.2   # 20% para validação
PATIENCE      = 50    # early stopping (épocas sem melhora)

# ── Inferência ────────────────────────────────────────────────────────────────
MAX_SAIDA  = 20
BEAM_WIDTH = 3        # beam search
