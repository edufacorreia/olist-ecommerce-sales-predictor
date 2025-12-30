import kagglehub
import pandas as pd
import os

def load_olist_data():
    """
    Faz o download do dataset da Olist e carrega os arquivos CSV em um dicionário.
    """
    print("Iniciando download/checagem do dataset via kagglehub...")
    # Baixa a última versão e retorna o caminho da pasta
    path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
    
    datasets = {}
    # Lista dos arquivos que utilizaremos para as Q1 e Q4
    files = {
        'customers': 'olist_customers_dataset.csv',
        'items': 'olist_order_items_dataset.csv',
        'payments': 'olist_order_payments_dataset.csv',
        'reviews': 'olist_order_reviews_dataset.csv',
        'orders': 'olist_orders_dataset.csv',
        'products': 'olist_products_dataset.csv',
        'sellers': 'olist_sellers_dataset.csv',
        'categories': 'product_category_name_translation.csv'
    }

    for key, filename in files.items():
        file_path = os.path.join(path, filename)
        if os.path.exists(file_path):
            datasets[key] = pd.read_csv(file_path)
            print(f"{filename} carregado com sucesso.")
        else:
            print(f"Erro: {filename} não encontrado no caminho {path}")

    return datasets

if __name__ == "__main__":
    data = load_olist_data()
    print("\nResumo do carregamento:")
    for name, df in data.items():
        print(f"- {name}: {df.shape[0]} linhas e {df.shape[1]} colunas.")