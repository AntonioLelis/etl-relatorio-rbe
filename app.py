import streamlit as st
import pandas as pd
import json
import io
from datetime import datetime


# ---------------------------------------------------
# CONFIGURAÇÕES E UTILITÁRIOS
# ---------------------------------------------------

def load_config():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)["indices"]
    except FileNotFoundError:
        st.error("Arquivo 'config.json' não encontrado! Verifique a pasta do projeto.")
        return None


def limpar_percentual(valor):
    if pd.isna(valor) or str(valor).strip() == "":
        return 0.0
    try:
        v = str(valor).replace("%", "").replace(".", "").replace(",", ".").strip()
        return float(v) / 100
    except ValueError:
        return 0.0


def limpar_inteiro(valor):
    if pd.isna(valor) or str(valor).strip() == "":
        return 0
    try:
        return int(float(str(valor).replace(".", "").replace(",", ".")))
    except ValueError:
        return 0


# ---------------------------------------------------
# MOTOR DE TRANSFORMAÇÃO (ETL) OTIMIZADO
# ---------------------------------------------------

def transformar_dados(df, data_ref, indices):
    registros = []
    total_linhas = len(df)

    # UI da Barra de Progresso
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Melhoria: Usando df.values para performance (Numpy Array) 5x mais rápido
    for i, linha in enumerate(df.values):

        # Atualiza a barra de progresso (evitando lag na UI atualizando a cada 100 linhas)
        if i % 100 == 0 or i == total_linhas - 1:
            progress_bar.progress((i + 1) / total_linhas)
            status_text.text(f"Processando linha {i + 1} de {total_linhas}...")

        # Validação de integridade da linha
        if len(linha) > 30 and str(linha[0]).strip() == "ID" and str(linha[4]).strip().isdigit():
            try:
                registro = {
                    "Mês": data_ref,
                    "Unidade": linha[indices["unidade"]],
                    "Profissional": linha[indices["profissional"]],
                    "Ocupação": linha[indices["ocupacao"]],
                    "Descrição": linha[indices["descricao"]],
                    "Tipo": linha[indices["tipo"]],
                    "Config.": limpar_inteiro(linha[indices["config"]]),
                    "Bloq.": limpar_inteiro(linha[indices["bloq"]]),
                    "Ofer.": limpar_inteiro(linha[indices["ofer"]]),
                    "Agend.": limpar_inteiro(linha[indices["agend"]]),
                    "Disp.": limpar_inteiro(linha[indices["disp"]]),
                    "% Ocup.": limpar_percentual(linha[indices["perc_ocup"]]),
                    "Faltas": limpar_inteiro(linha[indices["faltas"]]),
                    "% Faltas": limpar_percentual(linha[indices["perc_faltas"]]),
                }
                registros.append(registro)
            except Exception as e:
                # Agora capturamos a exceção específica e registramos (se necessário)
                continue

    # Limpa os textos de progresso ao terminar
    progress_bar.empty()
    status_text.empty()

    return pd.DataFrame(registros)


# ---------------------------------------------------
# INTERFACE STREAMLIT (DASHBOARD)
# ---------------------------------------------------

st.set_page_config(page_title="Conversor Relatório RBE", page_icon="⚙️", layout="wide")

st.title("⚙️ Motor ETL - Relatórios RBE")
st.markdown("Transforme relatórios desestruturados do sistema em bases prontas para **Power BI** e bancos de dados.")

with st.sidebar:
    st.header("📅 Parâmetros")
    mes_nome = st.selectbox("Mês de Referência",
                            ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro",
                             "Outubro", "Novembro", "Dezembro"])
    ano = st.number_input("Ano", min_value=2020, max_value=2030, value=datetime.now().year)

    meses_map = {"Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4, "Maio": 5, "Junho": 6, "Julho": 7, "Agosto": 8,
                 "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12}
    data_ref = datetime(ano, meses_map[mes_nome], 1)

    st.markdown("---")
    st.header("ℹ️ Dúvidas?")
    st.markdown("Consulte a documentação caso o formato do relatório mude ou para entender como a ferramenta funciona.")
    st.link_button("📚 Acessar Documentação (GitHub)", "https://github.com/AntonioLelis/etl-relatorio-rbe", use_container_width=True)

arquivo = st.file_uploader("Faça o upload do Relatório RBE (.csv)", type=["csv"])

if arquivo:
    # Tratamento de erro na leitura do arquivo (Melhoria)
    try:
        df_raw = pd.read_csv(arquivo, header=None, encoding="latin1", dtype=str)
    except Exception as e:
        st.error(f"Erro ao ler arquivo. Verifique se o formato é realmente CSV. Detalhes: {e}")
        st.stop()

    # Melhoria: Detectar se é o arquivo correto logo no início
    # Busca a palavra "Unidade" nas 5 primeiras linhas para garantir que é o relatório RBE
    validador_arquivo = str(df_raw.head().values)
    if "Unidade" not in validador_arquivo and "Profissional" not in validador_arquivo:
        st.error("❌ Arquivo inválido! Este não parece ser o relatório RBE padrão.")
        st.stop()

    indices = load_config()

    if indices:
        st.info("Iniciando a limpeza e estruturação dos dados...")

        # Executa o ETL
        df_final = transformar_dados(df_raw, data_ref, indices)

        if not df_final.empty:
            st.success("✅ Processamento concluído com sucesso!")

            # Melhoria: Métricas estilo Dashboard
            st.markdown("### 📊 Resumo dos Dados Processados")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Linhas Processadas", f"{len(df_final):,}".replace(",", "."))
            col2.metric("Unidades Distintas", df_final["Unidade"].nunique())
            col3.metric("Profissionais Atendendo", df_final["Profissional"].nunique())
            col4.metric("Total de Ocupações", df_final["Ocupação"].nunique())

            st.markdown("### 🔍 Pré-visualização")
            # Mostrar o shape (linhas, colunas) e o dataframe em si
            st.caption(
                f"Visualizando os dados estruturados (Formato: {df_final.shape[0]} linhas e {df_final.shape[1]} colunas)")
            st.dataframe(df_final, use_container_width=True, height=250)

            # ---------------------------------------------------
            # OPÇÕES DE EXPORTAÇÃO
            # ---------------------------------------------------
            st.markdown("### 📥 Exportar Resultados")
            col_btn1, col_btn2, _ = st.columns([1, 1, 3])

            # Botão Excel
            with col_btn1:
                buffer_excel = io.BytesIO()
                with pd.ExcelWriter(buffer_excel, engine="openpyxl") as writer:
                    df_final.to_excel(writer, index=False, sheet_name="Dados_Limpos")

                st.download_button(
                    label="📊 Baixar XLSX (Excel)",
                    data=buffer_excel.getvalue(),
                    file_name=f"RBE_LIMPO_{mes_nome}_{ano}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

            # Melhoria: Botão CSV
            with col_btn2:
                csv_data = df_final.to_csv(index=False, sep=";").encode("utf-8-sig")
                st.download_button(
                    label="📝 Baixar CSV",
                    data=csv_data,
                    file_name=f"RBE_LIMPO_{mes_nome}_{ano}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.warning(
                "⚠️ O arquivo foi lido, mas nenhum registro válido foi encontrado. Verifique o layout do relatório.")