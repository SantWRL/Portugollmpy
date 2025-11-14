# Gerencia_de_projetos
# Sistema de Cálculo e Acompanhamento de IMC

![Badge de Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Badge de Licença](https://img.shields.io/badge/license-MIT-blue)
![Badge de Pull Requests](https://img.shields.io/badge/PRs-bem--vindas-brightgreen)

Projeto da disciplina de **Gerência de Projetos** do Bacharelado em Sistemas de Informação da Universidade Federal do Piauí (UFPI).

O objetivo é criar uma aplicação web para auxiliar nutricionistas e profissionais de saúde no cálculo automático do Índice de Massa Corporal (IMC) e no acompanhamento da evolução dos pacientes.

## 📊 Visão Geral do Projeto

A aplicação visa facilitar o registro, organização e análise do IMC, fornecendo classificação automática baseada nos padrões da Organização Mundial da Saúde (OMS) e permitindo o acompanhamento longitudinal dos dados do paciente.

## ✨ Funcionalidades Principais

* **Cálculo de IMC:** Entrada de peso (kg) e altura (m/cm) com classificação automática (Abaixo do peso, Peso normal, Sobrepeso, Obesidade Graus I, II e III).
* **Gestão de Pacientes:** Cadastro completo (nome, idade, gênero) e histórico de medições.
* **Acompanhamento Temporal:** Geração de gráficos de evolução do IMC e comparação entre medições.
* **Relatórios e Exportação:** Relatórios individuais e exportação em PDF e Excel.

## 💻 Arquitetura e Tecnologias

O sistema será uma aplicação web responsiva, compatível com navegadores desktop e mobile (iOS 12.0+ e Android 8.0+).

| Componente | Tecnologia |
| :--- | :--- |
| **Frontend** | HTML, CSS, Javascript |
| **Backend** | Javascript |
| **Banco de Dados**| MySQL |

## 🛠️ Gerência de Configuração

Para garantir a integridade e rastreabilidade do projeto, seguimos um Plano de Gerência de Configuração.

* **Ferramenta:** Git.
* **Repositório:** GitHub.
* **Automação:** GitHub Actions para build, testes e deploy automatizados.

### Estratégia de Branches (Git Flow)

Utilizamos o Git Flow como estratégia de *branching*:

| Branch | Descrição |
| :--- | :--- |
| `main` | Código em produção. |
| `develop` | Branch de desenvolvimento para integração. |
| `feature/*` | Desenvolvimento de novas funcionalidades. |
| `hotfix/*` | Correções críticas em produção. |
| `release/*` | Preparação de novas versões. |

### Processo de Mudança

Todo o controle de mudanças é gerenciado pelo GitHub:

1.  **Solicitação:** Criação de uma *Issue* no GitHub.
2.  **Análise:** Avaliação de impacto pela equipe.
3.  **Aprovação:** Validação pelo líder do projeto.
4.  **Implementação:** Desenvolvimento em uma *branch* `feature/*`.
5.  **Revisão:** *Code review* (*Pull Request*) por outro membro.
6.  **Testes:** Execução de testes.
7.  **Integração:** *Merge* para a *branch* `develop`.

## 📂 Estrutura do Repositório

A estrutura de diretórios do projeto está organizada da seguinte forma:
projeto-imc/ 
├── src/ │ 
├── frontend/
│ ├── backend/
│ └── database/
├── docs/ │ 
├── requisitos/
│ ├── tecnicos/
│ └── manuais/
├── tests/
└── config/

## 👥 Equipe

* Jordann Jeferson da Silva
* Ivonildo Florencio de Brito
* Patrick do Nascimento Santos
* Victor Rodrigues Luz

**Professor:** Evandro José da Rocha e Silva
