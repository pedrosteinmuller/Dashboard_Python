import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.strftime("%Y-%m")
    return df.sort_values("Date")

df = load_data()

# Sidebar Filtros
month = st.sidebar.selectbox("Mês", df["Month"].unique())
city = st.sidebar.multiselect("Cidade", df["City"].unique(), default=df["City"].unique())

df_filtered = df[(df["Month"] == month) & (df["City"].isin(city))]

# KPIs
st.markdown("## 📊 Dashboard de Vendas do Supermercado")
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

col_kpi1.metric("Faturamento Total", f"R$ {df_filtered['Total'].sum():,.2f}")
col_kpi2.metric("Ticket Médio", f"R$ {df_filtered['Total'].mean():,.2f}")
col_kpi3.metric("Número de Vendas", f"{df_filtered.shape[0]:,}")

# Layout de gráficos
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# Faturamento por dia
fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="Faturamento por Dia", 
                  text_auto=True, hover_data=["Total"])
col1.plotly_chart(fig_date, use_container_width=True)

# Faturamento por tipo de produto
product_total = df_filtered.groupby("Product line")[["Total"]].sum().reset_index()
fig_prod = px.bar(product_total, x="Total", y="Product line", color="Product line", 
                  title="Faturamento por Tipo de Produto", orientation="h", text_auto=True)
col2.plotly_chart(fig_prod, use_container_width=True)

# Faturamento por filial
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.bar(city_total, x="City", y="Total", title="Faturamento por Filial", text_auto=True)
col3.plotly_chart(fig_city, use_container_width=True)

# Faturamento por tipo de pagamento
fig_kind = px.pie(df_filtered, values="Total", names="Payment", title="Faturamento por Tipo de Pagamento")
col4.plotly_chart(fig_kind, use_container_width=True)

# Avaliação por cidade
city_rating = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
fig_rating = px.bar(city_rating, x="City", y="Rating", title="Avaliação Média por Cidade", text_auto=True)
col5.plotly_chart(fig_rating, use_container_width=True)
