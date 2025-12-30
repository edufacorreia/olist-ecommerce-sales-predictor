-- Tabela Central de Pedidos
CREATE TABLE olist_orders_dataset (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    order_status VARCHAR(20),
    order_purchase_timestamp DATETIME
);

-- Itens de cada Pedido (Um pedido pode ter vários itens)
CREATE TABLE olist_order_items_dataset (
    order_id VARCHAR(50),
    order_item_id INT,
    product_id VARCHAR(50),
    seller_id VARCHAR(50), -- Nomes das Houses de GoT aqui
    price DECIMAL(10, 2),
    freight_value DECIMAL(10, 2),
    PRIMARY KEY (order_id, order_item_id)
);

-- Avaliações (Crucial para a Q4)
CREATE TABLE olist_order_reviews_dataset (
    review_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50),
    review_score INT,
    review_creation_date DATETIME
);