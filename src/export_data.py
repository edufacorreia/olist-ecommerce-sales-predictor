import pandas as pd
import os
from data_loader import load_olist_data

def export_project_csvs():
    """
    Gera e exporta as diferentes versoes dos dados para a pasta /data.
    """
    print("Iniciando processo de exportacao de CSVs...")
    
    # Garantir que a pasta data existe
    data_path = "/home/eduardo/data_science_projects/olist/ecommerce_sales_predictor/data"
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    # 1. Carregamento dos dados brutos
    datasets = load_olist_data()
    df_orders = datasets['orders']
    df_items = datasets['items']
    df_reviews = datasets['reviews']

    # --- CSV 1: Bruto Completo (Merge sem filtros) ---
    # Uniao de todas as tabelas principais para ter o estado "cru" do dataset
    df_bruto = pd.merge(df_orders, df_items, on='order_id', how='left')
    df_bruto = pd.merge(df_bruto, df_reviews[['order_id', 'review_score']], on='order_id', how='left')
    df_bruto.to_csv(f"{data_path}/olist_bruto_completo.csv", index=False)
    print("CSV Bruto exportado.")

    # --- CSV 2: Dados com Correcoes ---
    # Aplicando filtros de status e remocao de outliers (2016)
    df_corrigido = df_bruto[df_bruto['order_status'] == 'delivered'].copy()
    df_corrigido['order_purchase_timestamp'] = pd.to_datetime(df_corrigido['order_purchase_timestamp'])
    
    # Removendo meses de teste de 2016
    df_corrigido = df_corrigido[~df_corrigido['order_purchase_timestamp'].dt.strftime('%Y-%m').isin(['2016-09', '2016-12'])]
    
    # Imputacao de mediana nos reviews vazios
    df_corrigido['review_score'] = df_corrigido['review_score'].fillna(df_corrigido['review_score'].median())
    
    df_corrigido.to_csv(f"{data_path}/olist_dados_corrigidos.csv", index=False)
    print("CSV com Correcoes exportado.")

    # --- CSV 3: Dados com Novo Atributo ---
    # Adicionando a coluna de Periodo de Analise (Expansao vs Estagnacao)
    df_corrigido['periodo_analise'] = 'Outro'
    df_corrigido.loc[df_corrigido['order_purchase_timestamp'].dt.year == 2017, 'periodo_analise'] = 'Expansao (2017)'
    df_corrigido.loc[(df_corrigido['order_purchase_timestamp'] >= '2018-02-01') & 
                     (df_corrigido['order_purchase_timestamp'] <= '2018-08-31'), 'periodo_analise'] = 'Estagnacao (2018)'
    
    df_corrigido.to_csv(f"{data_path}/olist_com_novo_atributo.csv", index=False)
    print("CSV com Novo Atributo exportado.")

    # --- CSV 4: Reduzido (Focado em Insights) ---
    # Apenas as colunas utilizadas nos graficos e conclusoes
    colunas_foco = [
        'order_id', 'order_purchase_timestamp', 'review_score', 
        'price', 'freight_value', 'periodo_analise'
    ]
    df_reduzido = df_corrigido[colunas_foco]
    df_reduzido.to_csv(f"{data_path}/olist_reduzido_insights.csv", index=False)
    print("CSV Reduzido para Insights exportado.")

    print("\nTodos os arquivos foram salvos em: " + data_path)

if __name__ == "__main__":
    export_project_csvs()