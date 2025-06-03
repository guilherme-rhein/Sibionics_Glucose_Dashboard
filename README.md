# 📊 Dashboard de Glicemia

Este projeto é um painel interativo desenvolvido com **Streamlit** para visualização e análise dos dados de glicemia obtidos por dispositivos como o da **Sibionics**.

## ✨ Motivação

Apesar dos gráficos gerados pelo sistema de monitoramento contínuo de glicose serem úteis para o dia a dia, senti falta de uma **visão mais detalhada e de longo prazo** — algo que ajudasse de fato a acompanhar padrões ao lado do meu médico.

Partindo dessa dor pessoal, nasceu a ideia de desenvolver este projeto simples, porém funcional. O objetivo é auxiliar não só a mim, mas também outras pessoas que utilizam o mesmo tipo de aparelho e querem um acompanhamento mais claro e filtrável de seus dados de glicemia.

## ⚙️ Funcionalidades

- 📈 **Gráficos interativos** com evolução da glicemia ao longo do tempo
- 📊 **Boxplot e Heatmap por hora do dia**
- 🧮 **Métricas automáticas**: média, mínimo, máximo e total de leituras
- ✅ **Classificação de leituras**: normoglicemia, hipoglicemia e hiperglicemia (inclusive em níveis extremos)
- 🗂️ **Filtros personalizáveis**:
  - Intervalo de datas
  - Intervalo de horas
  - Faixa de glicemia
- 📥 **Exportação dos dados filtrados** em Excel

## 🖼️ Exemplo do painel
- Entrada de dados:
<img src="https://raw.githubusercontent.com/guilherme-rhein/Sibionics_Glucose_Dashboard/refs/heads/main/img/Dashboard_inicial.png" alt="Dashboard Screenshot" width="800"/>

- Resultado:
<img src="https://raw.githubusercontent.com/guilherme-rhein/Sibionics_Glucose_Dashboard/refs/heads/main/img/Dashboard.png" alt="Dashboard Screenshot" width="800"/>

## 📦 Como utilizar localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   
   
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt

  
3. Execute o aplicativo:
   ```bash
   streamlit run app.py
