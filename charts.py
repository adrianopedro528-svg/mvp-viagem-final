import plotly.express as px
import pandas as pd

def plot_accumulation_curve(df_curve: pd.DataFrame, meta_brl: float):
    """Plota a curva de evolução do patrimônio vs Meta."""
    fig = px.line(
        df_curve, 
        x="Mês", 
        y=["Saldo Acumulado", "Total Investido"],
        title="Curva de Acumulação de Patrimônio",
        labels={"value": "Valor (R$)", "variable": "Legenda"},
        color_discrete_map={"Saldo Acumulado": "green", "Total Investido": "gray"}
    )
    
    
    fig.add_hline(y=meta_brl, line_dash="dash", line_color="red", annotation_text="Meta da Viagem")
    
    return fig