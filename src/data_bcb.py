import pandas as pd
import requests
import streamlit as st
from datetime import datetime

# URL APIs do Banco Central
URL_SELIC = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"
URL_DOLAR = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados/ultimos/1?formato=json"
URL_EURO = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.21619/dados/ultimos/1?formato=json"

@st.cache_data(ttl=3600) 
def get_latest_selic_monthly() -> float:
    """Retorna a taxa Selic mensal equivalente (baseada na meta anual)."""
    try:
        response = requests.get(URL_SELIC, timeout=5)
        response.raise_for_status()
        dados = response.json()
        selic_anual = float(dados[0]['valor']) / 100
        
        selic_mensal = (1 + selic_anual)**(1/12) - 1
        return selic_mensal
    except Exception as e:
        print(f"Erro ao buscar Selic: {e}")
        return None 
        
@st.cache_data(ttl=3600)
def get_exchange_rate(moeda="USD") -> float:
    """Busca cotação PTAX de venda mais recente para USD ou EUR."""
    url = URL_DOLAR if moeda == "USD" else URL_EURO
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        dados = response.json()
        return float(dados[0]['valor'])
    except Exception as e:
        print(f"Erro ao buscar Câmbio: {e}")

        return None
