import json
import torch
import torch.nn as nn
import torch.optim as optim
from vocabulario import Vocabulario
from modelo import Codificador, Decodificador, TupiLogicSeq2Seq

def preencher_lote(sequencias, pad_idx):
    max_len = max(len(s) for s in sequencias)
    return [s + [pad_idx] * (max_len - len(s)) for s in sequencias]

def treinar():
    with open("../dataset/dados.json", "r", encoding="utf-8") as f:
        dados = json.load(f)

    vocab_pt = Vocabulario()
    vocab_portugol = Vocabulario()

    for item in dados:
        vocab_pt.adicionar_frase(item["pt"])
        vocab_portugol.adicionar_frase(item["portugol"])

    TAM_EMBEDDING = 64
    TAM_OCULTO = 128
    
    codificador = Codificador(len(vocab_pt), TAM_EMBEDDING, TAM_OCULTO)
    decodificador = Decodificador(len(vocab_portugol), TAM_EMBEDDING, TAM_OCULTO)
    modelo = TupiLogicSeq2Seq(codificador, decodificador)

    otimizador = optim.Adam(modelo.parameters(), lr=0.01)
    criterio = nn.CrossEntropyLoss(ignore_index=vocab_portugol.stoi["<PAD>"])

    pt_codificado = [vocab_pt.codificar(item["pt"]) for item in dados]
    portugol_codificado = [vocab_portugol.codificar(item["portugol"]) for item in dados]

    fonte_tensores = torch.tensor(preencher_lote(pt_codificado, vocab_pt.stoi["<PAD>"]))
    alvo_tensores = torch.tensor(preencher_lote(portugol_codificado, vocab_portugol.stoi["<PAD>"]))

    # AUMENTAMOS PARA 500 ÉPOCAS PARA ELA MEMORIZAR BEM
    epocas = 500 
    print("Iniciando treinamento da Mente...")
    for epoca in range(epocas):
        otimizador.zero_grad()
        
        saida = modelo(fonte_tensores, alvo_tensores)
        
        saida_dim = saida.shape[-1]
        
        # AQUI ESTAVA O BUG! Agora fatiamos a dimensão certa (as palavras) [:, 1:]
        saida_achatada = saida[:, 1:].reshape(-1, saida_dim)
        alvo_achatado = alvo_tensores[:, 1:].reshape(-1)
        
        perda = criterio(saida_achatada, alvo_achatado)
        perda.backward()
        otimizador.step()
        
        if (epoca + 1) % 50 == 0:
            print(f"Época [{epoca+1}/{epocas}], Erro: {perda.item():.4f}")

    print("Salvando o modelo...")
    torch.save({
        'modelo_state_dict': modelo.state_dict(),
        'vocab_pt_stoi': vocab_pt.stoi,
        'vocab_pt_itos': vocab_pt.itos,
        'vocab_portugol_stoi': vocab_portugol.stoi,
        'vocab_portugol_itos': vocab_portugol.itos
    }, "../modelos_salvos/tupi_modelo.pth")
    print("Treinamento concluído e salvo em 'modelos_salvos'!")

if __name__ == "__main__":
    treinar()