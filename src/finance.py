import numpy as np
import pandas as pd

def annual_to_monthly_rate(i_annual: float) -> float:
    """Converte taxa anual decimal (ex: 0.10) para mensal."""
    return (1 + i_annual) ** (1/12) - 1

def nper(pmt: float, fv: float, r: float) -> float:
    """
    Calcula número de períodos (meses) para atingir FV com aportes PMT.
    Fórmula: NPER = log((FV * r + PMT) / PMT) / log(1 + r)
    """
    if r <= 0:
        return fv / pmt if pmt > 0 else 999
    
    if pmt <= 0:
        return 999 # Evita divisão por zero
        
    try:
        numerador = np.log((fv * r + pmt) / pmt)
        denominador = np.log(1 + r)
        meses = numerador / denominador
        return float(meses)
    except:
        return 999.0

def future_value(pmt: float, r: float, n: int) -> float:
    """Calcula Valor Futuro dado PMT, taxa e meses."""
    if r <= 0:
        return pmt * n
    return pmt * (((1 + r) ** n - 1) / r)

def build_accumulation_curve(pmt: float, r: float, n: int) -> pd.DataFrame:
    """Gera DataFrame mês a mês com saldo acumulado e total investido."""
    data = []
    saldo = 0.0
    inv = 0.0
    
    # Adiciona o Mês 0 (ponto de partida)
    data.append({"Mês": 0, "Saldo Acumulado": 0.0, "Total Investido": 0.0})
    
    # Loop corrigido: itera de 1 até n (incluindo n)
    # Garante que 'n' seja um inteiro
    n_safe = int(n)
    
    for m in range(1, n_safe + 1):
        # Juros sobre o saldo anterior + novo aporte
        saldo = saldo * (1 + r) + pmt
        inv += pmt
        data.append({"Mês": m, "Saldo Acumulado": saldo, "Total Investido": inv})
        
    return pd.DataFrame(data)
