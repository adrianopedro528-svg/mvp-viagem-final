MVP VIAGEM - PLANEJAMENTO FINANCEIRO

COMO RODAR O PROJETO:

Instale as dependências: pip install -r requirements.txt

Execute o aplicativo: streamlit run app.py

DESCRIÇÃO: Este MVP foi desenvolvido para atender aos requisitos de simulação financeira de viagens internacionais. O projeto realiza:

Coleta automática de Selic e Câmbio via API do Banco Central.

Cálculo de NPER (tempo para atingir a meta) e Valor Futuro.

Comparação de cenários (Base, Conservador e Estresse).

Geração de curvas de acumulação de patrimônio.

ESTRUTURA: O código segue arquitetura modular na pasta /src para separar coleta de dados, lógica financeira e gráficos.