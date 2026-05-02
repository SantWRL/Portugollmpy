# 🌿 Tupi-Logic: Tradutor e Interpretador Neural de Portugol

Este projeto é uma **Prova de Conceito (PoC)** de uma Inteligência Artificial desenvolvida do zero em Python e PyTorch. O sistema é capaz de entender comandos em Linguagem Natural (Português), traduzi-los para uma sintaxe estruturada (Portugol) utilizando uma Rede Neural Recorrente (Seq2Seq), e em seguida, executar o código gerado em tempo real através de um interpretador local.

## ✨ Novidades e Melhorias da Última Versão

A arquitetura e o fluxo de treinamento receberam melhorias profundas para maximizar a assertividade da IA e expandir as capacidades lógicas do interpretador:

- **Mecanismo de Atenção (Bahdanau Attention):** O Decoder agora analisa toda a frase do usuário dinamicamente em vez de depender de um único vetor comprimido.
- **Encoder Bidirecional:** A IA compreende o contexto lendo a frase da esquerda para a direita e da direita para a esquerda.
- **Beam Search:** A geração da sintaxe em Portugol foi otimizada para avaliar múltiplos caminhos de tradução em paralelo, encontrando a sintaxe mais perfeita em vez de adivinhar palavra por palavra.
- **Treinamento Profissional:** Split de Treino/Validação (80/20), *Early Stopping*, *Gradient Clipping*, *Dropout (0.3)* e salvamento automático do `tupi_melhor.pth` (baseado na *validation loss*).
- **Interpretador Robusto:**
  - Operadores lógicos completos: `>`, `<`, `>=`, `<=`, `==`, `!=`.
  - Matemática avançada e captura de tela: `+`, `-`, `*`, `/`, e `leia()`.
  - Suporte à **reatribuição de variáveis** (ex: `x = x + 5`) e laços condicionais avançados com **`enquanto`** (while loop com trava de segurança).

---

## 🚀 Funcionalidades

- **Gerador de Dataset (Data Augmentation):** Cria automaticamente ~2.100 exemplos de treinamento cobrindo dezenas de variações semânticas para evitar o *overfitting*.
- **Tradução Neural (Seq2Seq):** Uma rede neural baseada em GRU Bidirecional com Atenção que converte português coloquial em Portugol.
- **Interpretador de Portugol:** Um motor de execução baseado em Expressões Regulares (Regex) que gerencia variáveis, loops condicionais, IO e operações matemáticas.
- **Execução 100% Local:** Não depende de APIs externas ou internet para funcionar.

---

## 📁 Estrutura do Projeto

```text
Portugollmpy/
│
├── dataset/
│   └── dados.json          # Dataset gerado dinamicamente para o treinamento
│
├── modelos_salvos/         
│   ├── tupi_modelo.pth     # Último checkpoint salvo do modelo
│   └── tupi_melhor.pth     # Melhor modelo salvo durante a validação (Early Stop)
│
└── src/
    ├── config.py           # Configurações globais e hiperparâmetros
    ├── gerar_dataset.py    # Script que gera frases aleatórias para o aprendizado
    ├── vocabulario.py      # Transforma palavras (Tokens) em números e vice-versa
    ├── modelo.py           # Arquitetura Matemática da IA (Bidirecional + Atenção)
    ├── treinar.py          # Pipeline de treinamento (com validação e agendador LR)
    ├── interpretador.py    # Motor que lê o Portugol e executa ações na máquina
    └── inferencia.py       # Loop principal de chat e execução (com Beam Search)
```

---

## ⚙️ Pré-requisitos e Instalação

Certifique-se de ter o **Python 3.8+** instalado em sua máquina.

1. Clone este repositório ou baixe a pasta do projeto.
2. Instale as dependências executando no terminal:

```bash
pip install torch tqdm
```

---

## 🏃 Como Rodar o Projeto

Para testar o ciclo completo da aplicação, abra o terminal na pasta `src` e execute os três passos na ordem abaixo:

### Passo 1: Gerar a Base de Conhecimento
Gera mais de 2.000 exemplos variados de comandos (operações matemáticas, reatribuições, laços e prints) para dar robustez à IA.
```bash
python gerar_dataset.py
```

### Passo 2: Treinar a Rede Neural
Inicia o treinamento da IA ao longo de 500 épocas usando mini-batches de 64. O modelo valida automaticamente a perda e salva a melhor versão.
```bash
python treinar.py
```

### Passo 3: Iniciar a Inferência e Conversa
Abre o terminal interativo. O modelo gera o Portugol usando Beam Search, e o interpretador executa.
```bash
python inferencia.py
```

---

## 💻 Exemplos de Uso

Abaixo está um exemplo real de como o sistema traduz a linguagem natural, processa a lógica e salva informações na memória:

```text
--- Tupi-Logic IA: Assistente e Execucao ---
   (Beam Search + Atencao + Encoder Bidirecional)
Digite 'sair' para encerrar.

Usuario (Portugues): crie a variavel contador como 10
IA (Portugol): inteiro contador = 10
----------------------------------------
[Var] 'contador' = 10
----------------------------------------

Usuario (Portugues): incremente contador em 5
IA (Portugol): contador = contador + 5
----------------------------------------
[Var] 'contador' = 15
----------------------------------------

Usuario (Portugues): repita enquanto contador for menor que 20
IA (Portugol): enquanto ( contador < 20 ) faca
----------------------------------------
[Loop] enquanto contador < 20:
  -> Iteracao 1 (contador = 15)
  -> Iteracao 2 (contador = 16)
  -> Iteracao 3 (contador = 17)
  -> Iteracao 4 (contador = 18)
  -> Iteracao 5 (contador = 19)
----------------------------------------
```

---

## 🧠 Como Funciona por debaixo dos panos?

1. **Processamento (Vocabulário):** A frase do usuário entra (é normalizada para retirar acentos/maiúsculas) e o módulo `vocabulario.py` transforma cada palavra em um ID numérico (Tensor).
2. **Entendimento (Encoder Bidirecional):** O modelo `GRU` lê a sequência em ambas as direções, capturando o contexto da frase, e produz estados ocultos para cada palavra.
3. **Tradução (Decoder com Atenção):** Utilizando *Bahdanau Attention*, o Decoder "olha" para toda a frase codificada e prevê a equivalência no Portugol utilizando a estratégia *Beam Search* para encontrar o melhor caminho geracional.
4. **Execução (Interpretador):** O `interpretador.py` intercepta essa saída, utiliza Expressões Regulares (Regex) para identificar a ação e utiliza dicionários e loops do Python para refletir a lógica na memória da máquina de forma segura.

---

*Desenvolvido como Prova de Conceito (PoC) para tradução e interpretação de Linguagem Natural em Lógica de Programação com Redes Neurais Avançadas.*
