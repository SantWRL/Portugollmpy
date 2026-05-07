# 🌿 Tupi-Logic: Tradutor e Interpretador Neural de Portugol

Este projeto é uma **Prova de Conceito (PoC)** de uma Inteligência Artificial desenvolvida do zero em Python e PyTorch. O sistema é capaz de entender comandos em Linguagem Natural (Português), traduzi-los para uma sintaxe estruturada (Portugol) utilizando uma Rede Neural Recorrente (Seq2Seq), e em seguida, executar o código gerado em tempo real através de um interpretador local.

## ✨ Novidades e Melhorias (v2.0)

A arquitetura e o fluxo de treinamento receberam melhorias profundas para maximizar a assertividade da IA e expandir as capacidades lógicas do interpretador:

- **Interface Web Moderna:** Agora conta com uma Web UI em React/Vite para visualização de memória, tradução em tempo real e logs interativos.
- **Mecanismo de Atenção (Bahdanau Attention):** O Decoder analisa toda a frase do usuário dinamicamente.
- **Encoder Bidirecional:** Compreensão de contexto aprimorada.
- **Beam Search:** Tradução otimizada para encontrar a melhor sintaxe possível.
- **Interpretador Robusto:** Suporte a loops (`enquanto`), condicionais (`se/senao`), matemática e variáveis.

---

## 🚀 Funcionalidades

- **Web UI Interativa:** Visualize o estado das variáveis e a tradução neural instantaneamente.
- **Gerador de Dataset:** Cria automaticamente milhares de exemplos para evitar overfitting.
- **Tradução Neural:** Baseada em GRU Bidirecional com Atenção.
- **Execução 100% Local:** Segurança e privacidade total.

---

## 📁 Estrutura do Projeto

```text
Portugollmpy/
│
├── web-ui/                 # Frontend React (Vite)
├── dataset/                # Dados de treinamento
├── modelos_salvos/         # Checkpoints da IA
├── src/
│   ├── api/                # Backend Flask para integração com o Web UI
│   ├── interpretador.py    # Motor de execução do Portugol
│   ├── modelo.py           # Arquitetura da Rede Neural
│   └── ...
└── run_project.py          # Script mestre para rodar tudo de uma vez
```

---

## ⚙️ Instalação e Requisitos

### Pré-requisitos
- **Python 3.8+**
- **Node.js 18+** (para o Web UI)

### Passo 1: Instalar dependências do Python
```bash
pip install torch tqdm flask flask-cors requests
```

### Passo 2: Rodar o Projeto (Automático)
O script `run_project.py` cuida de gerar o dataset, treinar a IA (se necessário) e subir os servidores.

```bash
python run_project.py
```

---

## 💻 Como Usar (Web UI)

Ao rodar o `run_project.py`, acesse **`http://localhost:5173`** no seu navegador.

1. Digite um comando como: `crie a variavel pontos como 50`
2. Veja a tradução para Portugol: `inteiro pontos = 50`
3. O terminal mostrará a execução e a barra lateral mostrará a variável `pontos` salva.
4. Experimente: `se pontos for maior que 20 entao mostre ok`

---

## 🧠 Como Funciona?

1. **Vocabulário:** Transforma palavras em IDs numéricos.
2. **Encoder:** Processa a frase em ambas as direções.
3. **Decoder + Atenção:** Traduz para Portugol focando nas palavras mais relevantes.
4. **Interpretador:** Usa Regex e um motor de estado Python para executar a lógica.

---

*Desenvolvido como Prova de Conceito para tradução de Linguagem Natural em Lógica de Programação.*

