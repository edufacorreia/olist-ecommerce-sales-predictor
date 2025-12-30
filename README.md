# Ecommerce Sales Predictor - Análise Exploratória (Olist)

## 1. Visão Geral da Análise
Este projeto apresenta uma Análise Exploratória de Dados (AED) realizada sobre o dataset público da Olist, o maior marketplace do Brasil. O foco principal foi identificar padrões de sazonalidade e entender como a percepção de qualidade do cliente influencia o faturamento, fornecendo a base estratégica para futuros modelos de Sales Forecasting.

## 2. Problema e Objetivos
**Problema:** A dificuldade de prever picos de demanda e o impacto da reputação dos produtos na conversão de vendas, gerando ineficiência na gestão de estoque e logística.

**Objetivo Geral:** Analisar o comportamento de consumo e a resiliência operacional do ecossistema Olist entre 2016 e 2018.

### Questões de Pesquisa:

**Como as vendas se comportaram temporalmente e quais os meses de maior pico? (Q1)**

**Existe uma correlação direta entre o Review Score e o desempenho financeiro? (Q2)**

## 3. Metodologia de dados (ETL)
A preparação dos dados seguiu um pipeline rigoroso para garantir a integridade da análise:

**Seleção:** Foco nas tabelas de Pedidos, Itens e Avaliações, filtrando apenas transações com status delivered.

**Limpeza:** Normalização de campos datetime64 e tratamento de valores ausentes em Review Scores através de imputação pela mediana.

**Engenharia de Atributos:** Criação de colunas categóricas para distinguir as fases de Expansão (2017) e Estagnação (2018), além da extração de métricas de faturamento por período.

## 4. Principais Insights e Resultados
Os resultados da análise revelaram padrões críticos para a gestão do negócio:

### 4.1. Sazonalidade e Maturidade (Q1)
Pico Histórico: O mês de Novembro de 2017 apresentou o volume máximo de vendas, validando a influência massiva da Black Friday.

Platô de 2018: Observou-se uma queda drástica na volatilidade MoM (mês a mês), indicando que a plataforma atingiu a maturidade do seu canal orgânico.

### 4.2. Qualidade vs. Faturamento (Q2)
Dominância da Satisfação: Notas 4 e 5 concentram mais de 70% do faturamento total.

O Paradoxo do Ticket Médio: Curiosamente, pedidos com Nota 1 possuem o maior Ticket Médio (R$ 127), sugerindo que consumidores de produtos premium são mais críticos em relação a falhas na experiência.

## 5. Conclusões e Trabalhos Futuros
A análise prova que a Olist manteve uma consistência de qualidade de ~98,8% mesmo durante a transição para o platô de vendas de 2018. O próximo passo deste projeto envolverá o desenvolvimento de um modelo preditivo utilizando algoritmos de séries temporais para antecipar demandas regionais.

---
*Projeto desenvolvido para fins acadêmicos - 2025*