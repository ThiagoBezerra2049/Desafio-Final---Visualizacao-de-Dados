import streamlit as st
import pandas as pd
import plotly.express as px

# Título
st.title("📊 Acesso à Saúde no Brasil - Estabelecimentos do CNES")

# Carregar dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv("cnes_estabelecimentos.csv", sep=";", encoding="latin1", low_memory=False)
    return df

df = carregar_dados()

# Exibir amostra
st.subheader("Pré-visualização dos dados")
st.dataframe(df.head())

# Seleção de colunas principais
colunas_utilizadas = [
    "CNES", "NO_FANTASIA", "TP_UNIDADE", "DS_TIPO_UNIDADE", "CO_MUNICIPIO_GESTOR", 
    "NO_MUNICIPIO", "CO_UF", "NO_UF", "TP_ESTABELECIMENTO", "DS_TP_ESTABELECIMENTO",
    "TP_GESTAO", "DS_TP_GESTAO", "CO_CATEGORIA_UNIDADE", "DS_CATEGORIA_UNIDADE"
]

df = df[[col for col in colunas_utilizadas if col in df.columns]]

# Filtro por estado
ufs = df["NO_UF"].dropna().unique()
estado = st.selectbox("Selecione um estado para análise", sorted(ufs))

df_estado = df[df["NO_UF"] == estado]

# Gráfico 1: Tipos de unidade no estado
st.subheader(f"Distribuição por Tipo de Unidade - {estado}")
tipo_unidade = df_estado["DS_TIPO_UNIDADE"].value_counts().reset_index()
fig1 = px.bar(tipo_unidade, x="index", y="DS_TIPO_UNIDADE", labels={"index": "Tipo", "DS_TIPO_UNIDADE": "Quantidade"}, color="index")
st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Categoria administrativa (privado, público, filantrópico)
st.subheader(f"Distribuição por Categoria Administrativa - {estado}")
if "DS_CATEGORIA_UNIDADE" in df_estado.columns:
    categoria = df_estado["DS_CATEGORIA_UNIDADE"].value_counts().reset_index()
    fig2 = px.pie(categoria, names="index", values="DS_CATEGORIA_UNIDADE", title="Categoria da Unidade")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Coluna de categoria administrativa não está disponível neste dataset.")

# Conclusão
st.markdown("""
### 📌 Insights
- A distribuição desigual de estabelecimentos entre categorias pode revelar fragilidades no acesso público à saúde.
- Alguns estados contam com uma proporção elevada de unidades privadas em áreas críticas.

👉 Considere cruzar com dados de população ou leitos para uma análise mais aprofundada!
""")
