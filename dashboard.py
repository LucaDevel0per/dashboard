import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Dashboard de Finanãs Pesoais", layout="wide") #define título da aba e layout (largura total).
st.title("Dashboard de Finanças Pessoais") #exibe o título principal na interface.

# carregar dados
@st.cache_data # az com que a função seja executada apenas uma vez
def carregar_dados():
    df = pd.read_csv("financas_pessoais_2024.csv", parse_dates=["Data"]) #converte a coluna "Data" em formato de data.
    return df

df = carregar_dados()

# Filtros interativos
st.sidebar.header("🔎 Filtros")
tipo_selecionado = st.sidebar.selectbox("Tipo de Transação", ["Todas", "Despesa", "Receita"])

# Filtrar os dados
if tipo_selecionado != "Todas":
    df = df[df["Tipo"] == tipo_selecionado]

# Gráfico de pizza - Distribuição por categoria
st.subheader("📌 Distribuição por Categoria")
# Agrupar e ordenar categorias por valor
df_categoria = df.groupby("Categoria")["Valor"].sum().reset_index()
df_categoria = df_categoria.sort_values(by="Valor", ascending=False)

# Criar gráfico de pizza melhorado
fig_pizza = px.pie(
    df_categoria,
    names="Categoria",
    values="Valor",
    title=f'Distribuição de {"Todas as Transações" if tipo_selecionado == "Todas" else tipo_selecionado + "s"}',
    hole=0.4,
    color_discrete_sequence=px.colors.qualitative.Set3,
)

# Adicionar percentuais e valores no rótulo
fig_pizza.update_traces(
    textinfo='label+percent+value',
    textfont_size=14,
    pull=[0.05]*len(df_categoria)  # "afasta" levemente os setores
)

# Centralizar título e melhorar layout
fig_pizza.update_layout(
    title_x=0.5,
    legend_title="Categoria",
    legend=dict(font=dict(size=12))
)

st.plotly_chart(fig_pizza, use_container_width=True)

# Agrupar dados por mês e tipo
df["AnoMes"] = df["Data"].dt.to_period("M").astype(str)

df_mes = df.groupby(["AnoMes", "Tipo"])["Valor"].sum().reset_index()

# Gráfico de barras
st.subheader("📅 Evolução Mensal de Receitas e Despesas")

fig_barras = px.bar(
    df_mes,
    x="AnoMes",
    y="Valor",
    color="Tipo",
    barmode="group",
    text_auto=".2s",
    title="Receitas e Despesas por Mês",
    color_discrete_map={"Receita": "#2ecc71", "Despesa": "#e74c3c"},
)

fig_barras.update_layout(
    xaxis_title="Mês",
    yaxis_title="Valor (R$)",
    title_x=0.5,
    xaxis=dict(tickangle=-45),
    legend_title="Tipo de Transação"
)

st.plotly_chart(fig_barras, use_container_width=True)

# 📥 Mostrar tabela e permitir download
st.sidebar.markdown("---")
mostrar_tabela = st.sidebar.checkbox("📄 Mostrar tabela de dados")

if mostrar_tabela:
    st.subheader("📋 Tabela com os dados filtrados")
    st.dataframe(df, use_container_width=True)

    # Gerar CSV para download
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Baixar CSV",
        data=csv,
        file_name="dados_filtrados.csv",
        mime="text/csv"
    )

st.sidebar.markdown("[🌐 GitHub do Projeto](https://github.com/seu-usuario/seu-repo)")


# st.dataframe(df.sample(5)) #mostra a tabela interativa para analisarmos os dados.