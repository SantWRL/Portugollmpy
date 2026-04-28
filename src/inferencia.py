import torch
from vocabulario import Vocabulario
from modelo import Codificador, Decodificador, TupiLogicSeq2Seq
from interpretador import InterpretadorPortugol

def carregar_modelo_e_vocabs():
    checkpoint = torch.load("../modelos_salvos/tupi_modelo.pth")
    
    vocab_pt = Vocabulario()
    vocab_pt.stoi = checkpoint['vocab_pt_stoi']
    vocab_pt.itos = checkpoint['vocab_pt_itos']
    
    vocab_portugol = Vocabulario()
    vocab_portugol.stoi = checkpoint['vocab_portugol_stoi']
    vocab_portugol.itos = checkpoint['vocab_portugol_itos']

    TAM_EMBEDDING = 64
    TAM_OCULTO = 128
    codificador = Codificador(len(vocab_pt), TAM_EMBEDDING, TAM_OCULTO)
    decodificador = Decodificador(len(vocab_portugol), TAM_EMBEDDING, TAM_OCULTO)
    modelo = TupiLogicSeq2Seq(codificador, decodificador)
    
    modelo.load_state_dict(checkpoint['modelo_state_dict'])
    modelo.eval()
    
    return modelo, vocab_pt, vocab_portugol

def traduzir_para_portugol(frase, modelo, vocab_pt, vocab_portugol):
    modelo.eval()
    with torch.no_grad():
        tokens = vocab_pt.codificar(frase.lower())
        tensor_fonte = torch.tensor(tokens).unsqueeze(0)
        
        oculto = modelo.codificador(tensor_fonte)
        entrada_decoder = torch.tensor([vocab_portugol.stoi["<SOS>"]])
        
        palavras_geradas = []
        
        for _ in range(20):
            previsao, oculto = modelo.decodificador(entrada_decoder, oculto)
            melhor_palavra_idx = previsao.argmax(1).item()
            
            if melhor_palavra_idx == vocab_portugol.stoi["<EOS>"]:
                break
                
            palavras_geradas.append(melhor_palavra_idx)
            entrada_decoder = torch.tensor([melhor_palavra_idx])
            
        return vocab_portugol.decodificar(palavras_geradas)

if __name__ == "__main__":
    modelo, vocab_pt, vocab_portugol = carregar_modelo_e_vocabs()
    interpretador = InterpretadorPortugol()
    
    print("\n--- Tupi-Logic IA: Assistente e Execução ---")
    print("Digite 'sair' para encerrar.\n")
    
    while True:
        prompt = input("🗣️ Usuário (Português): ")
        if prompt.lower() == 'sair':
            break
            
        resultado_portugol = traduzir_para_portugol(prompt, modelo, vocab_pt, vocab_portugol)
        print(f"🤖 IA (Portugol): {resultado_portugol}")
        
        print("-" * 40)
        interpretador.executar(resultado_portugol)
        print("-" * 40 + "\n")