# /home/eduardo/data_science_projects/olist/ecommerce_sales_predictor/src/visualization.py

import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_visualizations(df):
    """
    Gera e salva graficos de analise exploratoria para as questoes Q1 e Q2.
    Inclui analise de sazonalidade, faturamento por nota e ticket medio.

    Args:
        df (pd.DataFrame): DataFrame processado contendo vendas e reviews.
    """
    
    print("Iniciando geracao de visualizacoes...")
    
    # Configuracao de caminho e estilo
    plot_path = "/home/eduardo/data_science_projects/olist/ecommerce_sales_predictor/plots"
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)

    sns.set_theme(style="whitegrid")

    # --- Q1: Tendencia Historica com Media e Pico ---
    plt.figure(figsize=(15, 7))
    
    # Preparacao dos dados da serie
    sales_trend = df.groupby('order_purchase_year_month').size()
    media_vendas = sales_trend.mean()
    max_vendas = sales_trend.max()
    mes_pico = sales_trend.idxmax()

    # Plotagem
    sales_trend.plot(kind='line', marker='o', color='royalblue', linewidth=2, label='Pedidos por Mes')
    plt.axhline(y=media_vendas, color='red', linestyle='--', alpha=0.7, label=f'Media: {media_vendas:.2f}')

    # Anotacao do Pico (Black Friday)
    plt.annotate(f'Pico: {max_vendas}\n(Black Friday)', 
                 xy=(mes_pico.to_timestamp(), max_vendas), 
                 xytext=(mes_pico.to_timestamp(), max_vendas + 500),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1),
                 horizontalalignment='center', fontweight='bold')

    plt.title('Q1 - Evolucao Mensal de Pedidos (2017-2018)', fontsize=14, pad=40)
    plt.xlabel('Periodo (Ano-Mes)')
    plt.ylabel('Total de Pedidos')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{plot_path}/grafico_q1_sazonalidade_detalhado.png")
    print("Grafico Q1 salvo.")

    # --- Q2: Participacao no Faturamento por Nota ---
    plt.figure(figsize=(10, 6))
    faturamento_nota = df.groupby('review_score')['price'].sum().sort_index(ascending=False)
    
    sns.barplot(x=faturamento_nota.index, y=faturamento_nota.values, palette='viridis')
    
    plt.title('Q2 - Faturamento Acumulado por Nota de Avaliacao', fontsize=14, pad=40)
    plt.xlabel('Nota (Review Score)')
    plt.ylabel('Faturamento Total (R$)')
    plt.tight_layout()
    plt.savefig(f"{plot_path}/grafico_q2_faturamento_nota.png")
    print("Grafico Q2 salvo.")

    # --- Insight Extra: Ticket Medio por Nota ---
    plt.figure(figsize=(10, 6))
    ticket_medio = df.groupby('review_score')['price'].mean().sort_index()
    
    sns.lineplot(x=ticket_medio.index, y=ticket_medio.values, marker='s', color='darkorange', linewidth=3)
    
    plt.title('Relacao entre Nota de Avaliacao e Ticket Medio', fontsize=14, pad=40)
    plt.xlabel('Nota (Review Score)')
    plt.ylabel('Ticket Medio (R$)')
    plt.tight_layout()
    plt.savefig(f"{plot_path}/grafico_insight_ticket_medio.png")
    print("Grafico de Ticket Medio salvo.")

    # --- Analise de Fase: Expansao vs Estagnacao ---
    plt.figure(figsize=(10, 6))
    fases = df[df['periodo_analise'] != 'Outro'].groupby('periodo_analise')['price'].sum()
    
    fases.plot(kind='bar', color=['salmon', 'skyblue'])
    plt.title('Comparativo de Faturamento: Expansao vs Estagnacao', fontsize=14, pad=40)
    plt.ylabel('Faturamento Total (R$)')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f"{plot_path}/grafico_comparativo_fases.png")
    print("Grafico comparativo de fases salvo.")

if __name__ == "__main__":
    from data_loader import load_olist_data
    from preprocessing import preprocess_data
    
    datasets = load_olist_data()
    df_final = preprocess_data(datasets)
    generate_visualizations(df_final)