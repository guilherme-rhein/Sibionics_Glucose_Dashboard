import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import timeit



def main():
    st.set_page_config(page_title = 'Dashboard de Glicemia', layout="wide")
    st.title("📊 Dashboard de Glicemia")
    st.markdown("---")

    # Data Func
    @st.cache_data 
    def load_data(file_data):
        return pd.read_excel(file_data)

    st.sidebar.write("## Adicione o arquivo:")
    data_file_1 = st.sidebar.file_uploader("Histórico de Glicemia", type=['xlsx'])
    if (data_file_1 is not None):
        start = timeit.default_timer()
        df_raw = load_data(data_file_1)
        df = df_raw.copy()
	df.drop(columns=["deviceModel"], inplace=True, errors='ignore')

	    
        #df.columns = ["DataHora", "Glicemia"]
	id_colunas = {"Hora": "DataHora",
		      "Leitura de sensor(mg/dL)": "Glicemia"
		     }
	df.rename(columns=id_colunas, inplace=True)
	    
	    
        #df["DataHora"] = pd.to_datetime(df["DataHora"].str.replace(" GMT-3", ""), format="%d-%m-%Y %H:%M")
        #df = df.sort_values("DataHora")
        #df = df.dropna()
        df["DataHora"] = pd.to_datetime(df["DataHora"].str.replace(" GMT-3", ""), format="%d-%m-%Y %H:%M", errors='coerce')
        df = df.sort_values("DataHora")
        df = df.dropna(subset=["DataHora", "Glicemia"])


        # Filters
        st.sidebar.header("Filtros")
        data_min = df["DataHora"].min().date()
        data_max = df["DataHora"].max().date()
        data_inicio, data_fim = st.sidebar.date_input("Intervalo de datas:", [data_min, data_max], min_value=data_min, max_value=data_max)

        # Hour filter
        st.sidebar.markdown("### Intervalo de horas")
        hora_inicio = st.sidebar.time_input("Hora inicial", value=pd.to_datetime("00:00").time())
        hora_fim = st.sidebar.time_input("Hora final", value=pd.to_datetime("23:59").time())


        # Glucose Filter 
        st.sidebar.markdown("### Intervalo de Glicemia")
        glicemia_min = float(df["Glicemia"].min())
        glicemia_max = float(df["Glicemia"].max())
        glicemia_range = st.sidebar.slider("Selecione o intervalo de glicemia (mg/dL):",
                                        min_value=glicemia_min,
                                        max_value=glicemia_max,
                                        value=(glicemia_min, glicemia_max),
                                        step=1.0)



        # App
        mask = (
            (df["DataHora"].dt.date >= data_inicio) &
            (df["DataHora"].dt.date <= data_fim) &
            (df["DataHora"].dt.time >= hora_inicio) &
            (df["DataHora"].dt.time <= hora_fim) &
            (df["Glicemia"] >= glicemia_range[0]) &
            (df["Glicemia"] <= glicemia_range[1])
        )
        df_filtrado = df[mask]

        # Métrics
        st.subheader("Resumo Geral")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Leituras", len(df_filtrado))
        col2.metric("Média", f"{df_filtrado['Glicemia'].mean():.1f} mg/dL")
        col3.metric("Mínimo", f"{df_filtrado['Glicemia'].min()} mg/dL")
        col4.metric("Máximo", f"{df_filtrado['Glicemia'].max()} mg/dL")

        # Class
        hipo = df_filtrado[df_filtrado["Glicemia"] < 70]
        hiper = df_filtrado[df_filtrado["Glicemia"] > 180]
        normo = df_filtrado[(df_filtrado["Glicemia"] >= 70) & (df_filtrado["Glicemia"] <= 180)]
        hipoext = df_filtrado[df_filtrado["Glicemia"] < 60]
        hiperext = df_filtrado[df_filtrado["Glicemia"] > 250]

        st.subheader("Classificação das Leituras")
        st.write(f"🔵 Normoglicemia (70-180 mg/dL): {len(normo)} registros - {len(normo)/len(df_filtrado)*100:.2f}%")
        st.write(f"🔻 Hipoglicemia (<70 mg/dL): {len(hipo)} registros - {len(hipo)/len(df_filtrado)*100:.2f}%")
        st.write(f"🔺 Hiperglicemia (>180 mg/dL): {len(hiper)} registros - {len(hiper)/len(df_filtrado)*100:.2f}%")

        st.write(f"🔻 Hipoglicemia Extrema (<60 mg/dL): {len(hipoext)} registros - {len(hipoext)/len(df_filtrado)*100:.2f}%")
        st.write(f"🔺 Hiperglicemia Extrema (>250 mg/dL): {len(hiperext)} registros - {len(hiperext)/len(df_filtrado)*100:.2f}%")

        # Graph 01
        st.subheader("Evolução da Glicemia ao Longo do Tempo")
        st.line_chart(df_filtrado.set_index("DataHora")["Glicemia"])

        # Graph base
        df_filtrado["Hora"] = df_filtrado["DataHora"].dt.hour
        media_por_hora = df_filtrado.groupby("Hora")["Glicemia"].mean().reset_index()

        # Graph 02
        st.subheader("Distribuição da Glicemia por Hora")
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.boxplot(data=df_filtrado, x="Hora", y="Glicemia", ax=ax)
        ax.set_title("Boxplot da Glicemia por Hora do Dia")
        st.pyplot(fig)  


        # Graph 03
        fig, ax = plt.subplots(figsize=(25, 2))
        sns.heatmap(media_por_hora[["Glicemia"]].T, cmap="coolwarm", annot=True, fmt=".1f", cbar=True, ax=ax)
        ax.set_title("Média de Glicemia por Hora do Dia")
        ax.set_yticklabels(["Glicemia Média"], rotation=0)
        ax.set_xticklabels(media_por_hora["Hora"], rotation=0)
        st.pyplot(fig)     


        # Tab
        st.subheader("Eventos de Hipoglicemia e Hiperglicemia")
        st.markdown("#### Hipoglicemias")
        st.dataframe(hipo)

        st.markdown("#### Hiperglicemias")
        st.dataframe(hiper)

        # Export
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Exportar dados")

        @st.cache_data
        def convert_df_to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Glicemia Filtrada')
            output.seek(0)
            return output

        excel_data = convert_df_to_excel(df_filtrado)
        st.sidebar.download_button("📥 Baixar dados filtrados", data=excel_data, file_name="glicemia_filtrada.xlsx")



if __name__ == '__main__':

	main()


