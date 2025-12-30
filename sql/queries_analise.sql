-- Q1: Tendencia de Vendas Mensais e Faturamento
-- Objetivo: Identificar sazonalidade e crescimento historico
SELECT 
    TO_CHAR(order_purchase_timestamp, 'YYYY-MM') AS periodo,
    COUNT(DISTINCT o.order_id) AS total_pedidos,
    ROUND(SUM(i.price)::numeric, 2) AS faturamento_mensal
FROM olist_orders_dataset o
JOIN olist_order_items_dataset i ON o.order_id = i.order_id
WHERE o.order_status = 'delivered'
GROUP BY periodo
ORDER BY periodo;

-- Q2: Relacao entre Nota de Avaliacao e Desempenho Financeiro
-- Objetivo: Quantificar o impacto da satisfacao no faturamento total
SELECT 
    r.review_score AS nota,
    COUNT(DISTINCT o.order_id) AS quantidade_pedidos,
    ROUND(SUM(i.price)::numeric, 2) AS faturamento_total,
    ROUND(AVG(i.price)::numeric, 2) AS ticket_medio
FROM olist_orders_dataset o
JOIN olist_order_items_dataset i ON o.order_id = i.order_id
JOIN olist_order_reviews_dataset r ON o.order_id = r.order_id
GROUP BY r.review_score
ORDER BY r.review_score DESC;

-- Query Adicional: Top 5 Categorias por Faturamento
-- Util para enriquecer a discussao dos resultados no trabalho
SELECT 
    t.product_category_name_english AS categoria,
    COUNT(i.product_id) AS itens_vendidos,
    ROUND(SUM(i.price)::numeric, 2) AS faturamento_total
FROM olist_order_items_dataset i
JOIN olist_products_dataset p ON i.product_id = p.product_id
JOIN product_category_name_translation t ON p.product_category_name = t.product_category_name
GROUP BY categoria
ORDER BY faturamento_total DESC
LIMIT 5;