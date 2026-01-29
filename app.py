import streamlit as st
import pandas as pd
import numpy as np
from src import data_bcb, finance, charts

#cabeçalho
st.set_page_config(page_title="MVP Viagem", layout="wide")
st.title("Planejamento Financeiro para Viagens Internacionais ✈️")
st.subheader("Estimativa de tempo para atingir meta em moeda estrangeira com base em Selic e câmbio.")

#sidebar
with st.sidebar:
    st.header("Parâmetros da Viagem")
    
    meta_moeda = st.number_input("Custo da Viagem (Moeda Estrangeira)", value=3000.0, min_value=100.0)
    moeda = st.selectbox("Moeda", ["USD", "EUR"])
    
    st.divider()
    
    st.header("Capacidade de Poupança")
    aporte_mensal = st.number_input("Aporte Mensal (R$)", value=500.0, min_value=50.0)
    
    st.divider()
    
    st.header("Configuração de Mercado")
    
    # Câmbio
    usar_cambio_auto = st.checkbox("Câmbio Automático (BCB)", value=True)
    cambio_api = data_bcb.get_exchange_rate(moeda)
    
    if usar_cambio_auto and cambio_api:
        taxa_cambio = cambio_api
        st.success(f"Cotação Atual ({moeda}): R$ {taxa_cambio:.4f}")
    else:
        taxa_cambio = st.number_input(f"Câmbio Manual (R$/{moeda})", value=5.50, format="%.4f")

    # Selic
    usar_selic_auto = st.checkbox("Selic Automática (BCB)", value=True)
    selic_mensal_api = data_bcb.get_latest_selic_monthly()
    
    if usar_selic_auto and selic_mensal_api:
        taxa_mensal_base = selic_mensal_api
        st.success(f"Selic Mensal Atual: {taxa_mensal_base*100:.4f}%")
    else:
        selic_anual_manual = st.number_input("Selic Anual Manual (%)", value=10.0)
        taxa_mensal_base = finance.annual_to_monthly_rate(selic_anual_manual / 100)

    horizonte_max = 240 # Trava de segurança

#Cenários e Cálculos
# Converter custo para BRL
meta_brl = meta_moeda * taxa_cambio

# Definir Cenários
cenarios = {
    "Base": {
        "taxa": taxa_mensal_base,
        "meta": meta_brl,
        "cor": "blue"
    },
    "Conservador": {
        "taxa": taxa_mensal_base * 0.8, 
        "meta": meta_moeda * (taxa_cambio * 1.1),
        "cor": "orange"
    },
    "Estresse": {
        "taxa": taxa_mensal_base * 0.6,
        "meta": meta_moeda * (taxa_cambio * 1.2),
        "cor": "red"
    }
}

# dash


tab1, tab2, tab3 = st.tabs(["Cenário Base", "Cenário Conservador", "Cenário Estresse"])

def render_cenario(nome_cenario):
    dados = cenarios[nome_cenario]
    r = dados['taxa']
    meta = dados['meta']
    
    # NPER
    meses_necessarios = finance.nper(aporte_mensal, meta, r)
    
    # Trava visual
    if meses_necessarios > horizonte_max:
        meses_necessarios = horizonte_max
        msg_tempo = f"+ de {horizonte_max} meses"
    else:
        msg_tempo = f"{meses_necessarios:.1f} meses ({meses_necessarios/12:.1f} anos)"

    #KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Meta em BRL", f"R$ {meta:,.2f}")
    c2.metric("Taxa Mensal Considerada", f"{r*100:.3f}%")
    c3.metric("Tempo Estimado", msg_tempo)

    #Gerar Curva
    n_plot = int(meses_necessarios) + 2
    df_curve = finance.build_accumulation_curve(aporte_mensal, r, n_plot)
    
  
    st.plotly_chart(charts.plot_accumulation_curve(df_curve, meta), use_container_width=True)
    
  
    total_aportado = df_curve.iloc[-1]['Total Investido']
    juros = df_curve.iloc[-1]['Saldo Acumulado'] - total_aportado
    
    st.info(f"""
    **Análise do {nome_cenario}:**
    Com um aporte de R$ {aporte_mensal:,.2f}, você atinge a meta de R$ {meta:,.2f} em aproximadamente **{msg_tempo}**.
    Neste período, você terá aportado R$ {total_aportado:,.2f} e ganho R$ {juros:,.2f} em juros brutos.
    """)


with tab1: render_cenario("Base")
with tab2: render_cenario("Conservador")
with tab3: render_cenario("Estresse")

st.divider()

# Limitações
st.warning("""
**Limitações do Modelo:**
1. **Taxa Constante:** Assume que a Selic se manterá a mesma por todo o período, o que não ocorre na prática.
2. **Câmbio:** A cotação é fixada no valor de hoje (ou simulada nos cenários), ignorando a volatilidade diária.
3. **Inflação:** O modelo calcula valores nominais, não descontando a inflação (IPCA) do período.
4. **Impostos:** O cálculo de juros é bruto. Considere descontar IR (15% a 22.5%) dependendo do investimento.
""")