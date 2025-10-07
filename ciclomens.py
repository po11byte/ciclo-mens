import streamlit as st
import datetime
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="App del Ciclo Menstrual", layout="centered")

st.title("Ciclo Menstrual")
st.write("Calcula tu ciclo, fases y dias fertiles.")

fecha_ultima = st.date_input("Fecha del ultimo periodo")
duracion_ciclo = st.number_input("Duracion promedio del ciclo (dias)", min_value=20, max_value=40, value=28, step=1)
duracion_periodo = st.number_input("Duracion del sangrado (dias)", min_value=2, max_value=10, value=5, step=1)

if st.button("Calcular Ciclo", type="primary"):
    if fecha_ultima:
        proximo_periodo = fecha_ultima + datetime.timedelta(days=duracion_ciclo)
        ovulacion = fecha_ultima + datetime.timedelta(days=duracion_ciclo - 14)
        inicio_fertil = ovulacion - datetime.timedelta(days=4)
        fin_fertil = ovulacion + datetime.timedelta(days=1)

        st.success("Resultados del ciclo")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Proximo periodo", proximo_periodo.strftime("%d/%m/%Y"))
            st.metric("Ovulacion", ovulacion.strftime("%d/%m/%Y"))
        with col2:
            st.metric("Inicio fertil", inicio_fertil.strftime("%d/%m/%Y"))
            st.metric("Fin fertil", fin_fertil.strftime("%d/%m/%Y"))
        st.markdown("---")
        st.subheader("Fases del ciclo")
        st.write("1. Menstrual: {} al {}".format(fecha_ultima.strftime("%d/%m/%Y"), (fecha_ultima + datetime.timedelta(days=duracion_periodo)).strftime("%d/%m/%Y")))
        st.write("2. Folicular: {} al {}".format((fecha_ultima + datetime.timedelta(days=duracion_periodo)).strftime("%d/%m/%Y"), ovulacion.strftime("%d/%m/%Y")))
        st.write("3. Ovulacion: {}".format(ovulacion.strftime("%d/%m/%Y")))
        st.write("4. Lutea: {} al {}".format((ovulacion + datetime.timedelta(days=1)).strftime("%d/%m/%Y"), proximo_periodo.strftime("%d/%m/%Y")))

        st.markdown("---")
        st.subheader("Grafica del ciclo")

        dias = pd.date_range(fecha_ultima, proximo_periodo)
        fases = []
        for d in dias:
            d_date = d.date()
            if fecha_ultima <= d_date < fecha_ultima + datetime.timedelta(days=duracion_periodo):
                fases.append("Menstrual")
            elif fecha_ultima + datetime.timedelta(days=duracion_periodo) <= d_date < ovulacion:
                fases.append("Folicular")
            elif d_date == ovulacion:
                fases.append("Ovulacion")
            else:
                fases.append("Lutea")

        df = pd.DataFrame({"Fecha": dias, "Fase": fases})
        colores = {"Menstrual": "#ff6b6b", "Folicular": "#feca57", "Ovulacion": "#48dbfb", "Lutea": "#1dd1a1"}
        df["Color"] = df["Fase"].map(colores)

        fig, ax = plt.subplots(figsize=(8, 1.5))
        ax.bar(df["Fecha"], [1]*len(df), color=df["Color"], width=1.0)
        ax.set_yticks([])
        ax.set_xticks([fecha_ultima, ovulacion, proximo_periodo])
        ax.set_xticklabels(["Inicio", "Ovulacion", "Proximo Periodo"])
        ax.set_title("Linea del ciclo menstrual")
        st.pyplot(fig)
        st.markdown("---")
        st.subheader("Recomendaciones")
        st.write("- Registra tus ciclos regularmente para mayor precision.")
        st.write("- Dias fertiles: {} al {}".format(inicio_fertil.strftime("%d/%m/%Y"), fin_fertil.strftime("%d/%m/%Y")))
        st.write("- Ovulacion estimada el {}.".format(ovulacion.strftime("%d/%m/%Y")))
        st.write("- El proximo periodo podria comenzar el {}.".format(proximo_periodo.strftime("%d/%m/%Y")))
    else:
        st.warning("Selecciona una fecha valida.")

st.markdown("---")
st.write("Desarrollado con Streamlit")
