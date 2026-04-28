
```
# 🌿 Tupi-Logic: Tradutor e Interpretador Neural de Portugol

Este projeto é uma **Prova de Conceito (PoC)** de uma Inteligência Artificial desenvolvida do zero em Python e PyTorch. O sistema é capaz de entender comandos em Linguagem Natural (Português), traduzi-los para uma sintaxe estruturada (Portugol) utilizando uma Rede Neural Recorrente (Seq2Seq), e em seguida, executar o código gerado em tempo real através de um interpretador local.

## 🚀 Funcionalidades

- **Gerador de Dataset (Data Augmentation):** Cria automaticamente milhares de exemplos de treinamento para evitar o *overfitting* da IA.
- **Tradução Neural (Seq2Seq):** Uma rede neural baseada em GRU com arquitetura Encoder-Decoder que converte português coloquial em Portugol.
- **Interpretador de Portugol:** Um motor de execução baseado em Expressões Regulares (Regex) que possui gerenciamento de memória (variáveis), execução de laços de repetição, condicionais e operações matemáticas.
- **Execução 100% Local:** Não depende de APIs externas ou internet para funcionar.

---

## 📁 Estrutura do Projeto

```text
Portugol2Ruby/
│
├── dataset/
│   └── dados.json          # Dataset gerado dinamicamente para o treinamento
│
├── modelos_salvos/         
│   └── tupi_modelo.pth     # Pesos (Cérebro) da Rede Neural após o treinamento
│
└── src/
    ├── gerar_dataset.py    # Script que gera frases aleatórias para o aprendizado
    ├── vocabulario.py      # Transforma palavras (Tokens) em números e vice-versa
    ├── modelo.py           # Arquitetura Matemática da IA (Encoder / Decoder)
    ├── treinar.py          # Script que treina a IA baseada no dados.json
    ├── interpretador.py    # Motor que lê o Portugol e executa ações na máquina
    └── inferencia.py       # Loop principal de chat e execução (O Aplicativo Final)
```

---

## ⚙️ Pré-requisitos e Instalação

Certifique-se de ter o **Python 3.8+** instalado em sua máquina.

1. Clone este repositório ou baixe a pasta do projeto.
2. Instale o PyTorch executando no terminal:

```bash
pip install torch
```

---

## 🏃 Como Rodar o Projeto

Para testar o ciclo completo da aplicação, abra o terminal na pasta `src` e execute os três passos na ordem abaixo:

### Passo 1: Gerar a Base de Conhecimento
Gera milhares de exemplos variados de comandos (operações matemáticas, variáveis, prints) para dar robustez à IA.
```bash
python gerar_dataset.py
```

### Passo 2: Treinar a Rede Neural
Inicia o treinamento da IA ao longo de 500 épocas. O erro matemático irá cair e os pesos da rede neural serão salvos na pasta `modelos_salvos`.
```bash
python treinar.py
```

### Passo 3: Iniciar a Inferência e Conversa
Abre o terminal interativo onde você pode digitar em português. O modelo gera o Portugol, e o interpretador executa.
```bash
python inferencia.py
```

---

## 💻 Exemplos de Uso

Abaixo está um exemplo real de como o sistema traduz a linguagem natural, processa a lógica e salva informações na memória:

```text
--- Tupi-Logic IA: Assistente e Execução ---
Digite 'sair' para encerrar.

🗣️ Usuário (Português): crie a variavel x como 20
🤖 IA (Portugol): inteiro x = 20
----------------------------------------
⚙️  [Interpretador]: Variável 'x' criada com o valor 20.
----------------------------------------

🗣️ Usuário (Português): crie a variavel y como 30
🤖 IA (Portugol): inteiro y = 30
----------------------------------------
⚙️  [Interpretador]: Variável 'y' criada com o valor 30.
----------------------------------------

🗣️ Usuário (Português): some x com y
🤖 IA (Portugol): x + y
----------------------------------------
⚙️  [Interpretador]: O resultado de x + y é 50
----------------------------------------

🗣️ Usuário (Português): se x for maior que 10
🤖 IA (Portugol): se ( x > 10 ) entao
----------------------------------------
⚙️  [Interpretador]: Condição VERDADEIRA (x = 20 > 10).
----------------------------------------
```

---

## 🧠 Como Funciona por debaixo dos panos?

1. **Processamento (Vocabulário):** A frase do usuário entra e o módulo `vocabulario.py` transforma cada palavra em um ID numérico (Tensor).
2. **Entendimento (Codificador):** O modelo `GRU` analisa a sequência de números e gera um "Context Vector" (um resumo matemático da intenção da frase).
3. **Tradução (Decodificador):** Outro `GRU` pega esse resumo e tenta prever, palavra por palavra, qual seria a equivalência na sintaxe do Portugol.
4. **Execução (Interpretador):** O `interpretador.py` intercepta essa saída, utiliza Expressões Regulares (Regex) para identificar a ação e utiliza estruturas de dicionários e loops do próprio Python para refletir a lógica na memória da máquina.

---

*Desenvolvido como Prova de Conceito (PoC) para tradução e interpretação de Linguagem Natural em Lógica de Programação.*
```
