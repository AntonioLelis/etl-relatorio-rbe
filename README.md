# 🏥 ETL - Transformador de Relatórios RBE

[![Aceder à Aplicação](https://img.shields.io/badge/Aceder%20App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://etl-relatorio-rbe.streamlit.app/)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458.svg?logo=pandas&logoColor=white)

Uma ferramenta de Extração, Transformação e Carregamento (ETL) desenvolvida para normalizar relatórios desestruturados (formato RBE) de sistemas de gestão em saúde, convertendo-os em bases de dados limpas e prontas para consumo no Power BI, Tableau ou bancos de dados relacionais.

## 📌 O Problema
Sistemas legados frequentemente exportam relatórios em formatos visuais ("para leitura humana") ao invés de formatos tabulares. O relatório bruto RBE gera um arquivo `.csv` onde cabeçalhos e valores estão misturados na mesma linha (ex: `ID, Unidade, Profissional, 1, US Vitoria, João...`), tornando impossível a criação direta de dashboards ou cruzamento de dados.

## 💡 A Solução
Este projeto resolve o gargalo de dados através de uma aplicação web local com interface amigável. A ferramenta automatiza o Data Wrangling:
1. **Lê** o arquivo `.csv` bruto, identificando a estrutura bagunçada.
2. **Transforma** e limpa os dados, convertendo formatos numéricos brasileiros (ex: `61,11%` para `0.6111`) e pivotando colunas.
3. **Carrega** (Exporta) o resultado final em `.xlsx` ou `.csv` limpo, no formato tabular tradicional.

## 🚀 Funcionalidades
- **Interface Gráfica Simples:** Desenvolvida em Streamlit para que usuários finais (sem conhecimento em programação) possam realizar a conversão com apenas 2 cliques.
- **Processamento Otimizado:** Utiliza iteração direta em arrays NumPy (`df.values`) para garantir alta performance, processando milhares de linhas em segundos.
- **Métricas em Tempo Real:** Dashboard integrado que exibe o resumo dos dados processados (total de linhas, unidades distintas, profissionais).
- **Configuração Desacoplada:** O mapeamento de colunas é feito através de um arquivo `config.json`. Se o layout do sistema de origem mudar, basta atualizar o JSON, sem necessidade de alterar o código-fonte.

## 🛠️ Como executar o projeto

### Pré-requisitos
- Python 3.8 ou superior instalado.
- Gerenciador de pacotes `pip`.

### Instalação

1. Clone este repositório:
```bash
git clone [https://github.com/AntonioLelis/etl-relatorio-rbe.git](https://github.com/AntonioLelis/etl-relatorio-rbe.git)
cd etl-relatorio-rbe
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```
3. Execute a aplicação:
```bash
streamlit run app.py
```
### ⚙️ Arquivo de Configuração (config.json)
A extração funciona baseada em índices mapeados. Se o sistema exportador for atualizado, ajuste os índices neste arquivo:JSON{

```json  
{"indices": {
    "unidade": 5,
    "profissional": 6,
    "ocupacao": 7,
    "descricao": 9,
    "tipo": 11,
    "config": 14,
    "bloq": 16,
    "ofer": 18,
    "agend": 20,
    "disp": 22,
    "perc_ocup": 24,
    "faltas": 27,
    "perc_faltas": 29
  }
}
```
### 📊 Estrutura de Saída (Output)
O arquivo final gerado conterá a seguinte estrutura, perfeitamente compreensível pelo Power BI

### 👨‍💻 Autor

#### Antonio Augusto de Almeida Lelis

Vitória, ES - Brasil
GitHub: @AntonioLelis

Este projeto foi desenvolvido para simplificar rotinas de inteligência de negócios e análise de dados.






