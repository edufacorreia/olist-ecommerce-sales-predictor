# /home/eduardo/data_science_projects/olist/ecommerce_sales_predictor/src/preprocessing.py

import pandas as pd
import numpy as np

def preprocess_data(datasets):
    """
    Executa a limpeza, integracao e engenharia de atributos dos dados da Olist.
    Seguindo o pipeline de ETL descrito na Secao 2.3 do projeto.

    Args:
        datasets (dict): Dicionario contendo os DataFrames originais.

    Returns:
        pd.DataFrame: DataFrame master unificado e tratado para analise.
    """
    
    print("Iniciando pre-processamento...")

    # 1. Selecao Estrategica e Copia de Dados
    df_orders = datasets['orders'].copy()
    df_items = datasets['items'].copy()
    df_reviews = datasets['reviews'].copy()

    # Filtro de Status (Secao 2.3.1): Privilegiando apenas pedidos entregues
    df_orders = df_orders[df_orders['order_status'] == 'delivered']

    # 2. Normalizacao Temporal (Secao 2.3.2)
    timestamp_cols = [
        'order_purchase_timestamp', 
        'order_approved_at', 
        'order_delivered_carrier_date', 
        'order_delivered_customer_date', 
        'order_estimated_delivery_date'
    ]
    
    for col in timestamp_cols:
        df_orders[col] = pd.to_datetime(df_orders[col])

    # 3. Expurgo de Outliers e Anomalias (Secao 2.3.2)
    # Criando coluna auxiliar para identificar meses de teste (Setembro e Dezembro de 2016)
    df_orders['temp_month_year'] = df_orders['order_purchase_timestamp'].dt.to_period('M').astype(str)
    
    # Removendo registros identificados como testes de integracao
    meses_outliers = ['2016-09', '2016-12']
    df_orders = df_orders[~df_orders['temp_month_year'].isin(meses_outliers)]
    df_orders.drop(columns=['temp_month_year'], inplace=True)

    # 4. Engenharia de Atributos Temporais (Secao 2.3.3)
    df_orders['order_purchase_year'] = df_orders['order_purchase_timestamp'].dt.year
    df_orders['order_purchase_month'] = df_orders['order_purchase_timestamp'].dt.month
    df_orders['order_purchase_year_month'] = df_orders['order_purchase_timestamp'].dt.to_period('M')

    # Criacao da coluna categórica periodo_analise para distinguir as fases do mercado
    df_orders['periodo_analise'] = 'Outro'
    
    # Fase de Expansao (2017)
    df_orders.loc[(df_orders['order_purchase_timestamp'] >= '2017-01-01') & 
                  (df_orders['order_purchase_timestamp'] <= '2017-12-31'), 'periodo_analise'] = 'Expansao (2017)'
    
    # Fase de Estagnacao (2018)
    df_orders.loc[(df_orders['order_purchase_timestamp'] >= '2018-02-01') & 
                  (df_orders['order_purchase_timestamp'] <= '2018-08-31'), 'periodo_analise'] = 'Estagnacao (2018)'

    # 5. Integracao Relacional (Joins - Secao 2.3.3)
    # Merge Pedidos + Itens
    df_master = pd.merge(df_orders, df_items, on='order_id', how='inner')
    
    # Merge com Reviews
    df_master = pd.merge(df_master, df_reviews[['order_id', 'review_score']], on='order_id', how='left')

    # 6. Tratamento de Dados Faltantes (Imputacao - Secao 2.3.2)
    # Imputando a mediana nos Review Scores ausentes
    df_master['review_score'] = df_master['review_score'].fillna(df_master['review_score'].median())

    print(f"Pre-processamento concluido. Dataset mestre gerado com {df_master.shape[0]} linhas.")
    
    return df_master

if __name__ == "__main__":
    from data_loader import load_olist_data
    raw_data = load_olist_data()
    df_final = preprocess_data(raw_data)
    
    print("\nVerificacao da Engenharia de Atributos (Periodos):")
    print(df_final['periodo_analise'].value_counts())
    
    print("\nVerificacao de Limpeza de Outliers (2016-09/12 devem estar ausentes):")
    print(df_final[df_final['order_purchase_year'] == 2016]['order_purchase_month'].unique())