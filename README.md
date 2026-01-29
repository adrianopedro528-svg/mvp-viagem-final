# ✈️ MVP: Planejamento Financeiro para Viagens Internacionais

Este projeto é um **Produto Viável Mínimo (MVP)** acadêmico desenvolvido para auxiliar no planejamento financeiro de viagens ao exterior. A aplicação simula o tempo necessário para atingir uma meta em moeda estrangeira (Dólar ou Euro), utilizando dados reais do mercado financeiro brasileiro.

## 📋 Descrição do Projeto

O sistema funciona como uma calculadora de viabilidade financeira. Diferente de planilhas estáticas, ele conecta-se automaticamente ao Banco Central para obter taxas atualizadas e projeta cenários de risco.

**Principais Funcionalidades:**
* **Conexão API:** Coleta automática da Taxa Selic e Câmbio PTAX.
* **Cálculo de NPER:** Estimativa matemática do tempo de investimento necessário.
* **Análise de Cenários:** Comparação entre cenários Base, Conservador e de Estresse.
* **Visualização:** Gráficos interativos da curva de acumulação de patrimônio.

## 🛠️ Estrutura do Código

O projeto foi desenvolvido em Python seguindo uma arquitetura modular para facilitar a manutenção e organização:

```text
mvp_viagem/
├── app.py              # Interface principal (Streamlit)
├── requirements.txt    # Dependências do projeto
├── README.md           # Documentação
└── src/                # Módulos de lógica (Core)
    ├── data_bcb.py     # Coleta e cache de dados do Banco Central
    ├── finance.py      # Motor de matemática financeira
    └── charts.py       # Gerador de gráficos (Plotly)


    Como Rodar o Projeto
Siga os passos abaixo para executar a aplicação na sua máquina local:

Instale as dependências: Certifique-se de estar na pasta do projeto e execute:
pip install -r requirements.txt

Execute a aplicação:
streamlit run app.py


Acesse no navegador: O Streamlit abrirá automaticamente uma aba no seu navegador (geralmente em http://localhost:8501).
Metodologia e Limitações
Metodologia

O cálculo do tempo para atingir a meta utiliza a fórmula financeira de Número de Períodos (NPER) para uma série de pagamentos constantes com juros compostos:
NPER = log((FV * i + PMT) / (PMT + PV * i)) / log(1 + i)

FV: Valor Futuro (Meta da viagem convertida para Reais)

PMT: Aporte mensal

i: Taxa de juros mensal equivalente

Limitações do Modelo
Taxa Livre de Risco: O modelo assume que a Taxa Selic atual se manterá constante por todo o período.

Inflação: Os valores apresentados são nominais e não descontam a inflação (IPCA).

Volatilidade Cambial: A conversão da meta utiliza a cotação "spot" (atual) ou simulada nos cenários, sem prever flutuações diárias do câmbio.