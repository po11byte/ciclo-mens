import streamlit as st
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import requests

st.set_page_config(page_title="App del Ciclo Menstrual", layout="centered")

OPENWEATHER_API_KEY = "1aefb8a907db6f0953a604ab4d387020"
NEWS_API_KEY = "de254c1053d7f9b4e714f00a366ff53c"

def obtener_clima(ciudad="San Salvador"):
    if OPENWEATHER_API_KEY == "tu_key_openweather_aqui":
        return None
        
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={OPENWEATHER_API_KEY}&units=metric&lang=es"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "temperatura": round(data["main"]["temp"]),
                "humedad": data["main"]["humidity"],
                "descripcion": data["weather"][0]["description"],
                "ciudad": data["name"],
                "presion": data["main"]["pressure"]
            }
    except:
        pass
    return None

def obtener_noticias_salud():
    if NEWS_API_KEY == "tu_key_newsapi_aqui":
        return []
        
    url = f"https://newsapi.org/v2/everything?q=salud+mujer+menstrual+ciclo&language=es&sortBy=publishedAt&pageSize=3&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("articles", [])
    except:
        pass
    return []

def obtener_consejos_nutricion(fase):
    alimentos_por_fase = {
        "Menstrual": "Alimentos ricos en hierro: espinacas, lentejas, carne roja. Vitamina C: naranjas, fresas, pimientos. Hidratacion: mucha agua e infusiones",
        "Folicular": "Alimentos con zinc: nueces, semillas, legumbres. Fibra: vegetales verdes, granos integrales. Proteinas magras: pescado, pollo, tofu", 
        "Ovulación": "Grasas saludables: aguacate, aceite de oliva, frutos secos. Omega-3: salmon, atun, semillas de chia. Antioxidantes: bayas, tomates, zanahorias",
        "Lútea": "Magnesio: platano, chocolate oscuro, almendras. Carbohidratos complejos: avena, quinoa, camote. Calcio: lacteos, brocoli, sardinas"
    }
    return alimentos_por_fase.get(fase, "Dieta balanceada con variedad de nutrientes")

st.title("Ciclo Menstrual Inteligente")
st.write("App con APIs integradas para informacion en tiempo real")

with st.sidebar:
    st.header("APIs Conectadas")
    
    clima_status = "Conectada" if OPENWEATHER_API_KEY != "tu_key_openweather_aqui" else "Pendiente"
    news_status = "Conectada" if NEWS_API_KEY != "tu_key_newsapi_aqui" else "Pendiente"
    
    st.write(f"Clima: {clima_status}")
    st.write(f"Noticias: {news_status}")
    
    st.markdown("---")
    st.write("Configuracion:")
    ciudad = st.text_input("Ciudad para el clima:", "San Salvador")
    
    st.markdown("---")
    st.write("Obtén tus API Keys:")
    st.write("1. OpenWeatherMap.org")
    st.write("2. NewsAPI.org")

col1, col2 = st.columns(2)
with col1:
    fecha_ultima = st.date_input("Fecha del ultimo periodo", datetime.date.today())
    duracion_periodo = st.number_input("Duracion del sangrado (dias)", min_value=2, max_value=10, value=5, step=1)
    
with col2:
    duracion_ciclo = st.number_input("Duracion promedio del ciclo (dias)", min_value=20, max_value=40, value=28, step=1)
    ciclo_irregular = st.checkbox("Mi ciclo es irregular")

if st.button("Calcular Ciclo + APIs", type="primary", use_container_width=True):
    if fecha_ultima:
        proximo_periodo = fecha_ultima + datetime.timedelta(days=duracion_ciclo)
        ovulacion = fecha_ultima + datetime.timedelta(days=duracion_ciclo - 14)
        inicio_fertil = ovulacion - datetime.timedelta(days=4)
        fin_fertil = ovulacion + datetime.timedelta(days=1)
        
        hoy = datetime.date.today()
        if fecha_ultima <= hoy < fecha_ultima + datetime.timedelta(days=duracion_periodo):
            fase_actual = "Menstrual"
        elif fecha_ultima + datetime.timedelta(days=duracion_periodo) <= hoy < ovulacion:
            fase_actual = "Folicular" 
        elif hoy == ovulacion:
            fase_actual = "Ovulacion"
        elif ovulacion < hoy <= proximo_periodo:
            fase_actual = "Lutea"
        else:
            fase_actual = "Entre ciclos"
        
        st.success("Resultados de tu ciclo")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Proximo periodo", proximo_periodo.strftime("%d/%m/%Y"))
            st.metric("Fase actual", fase_actual)
        with col2:
            st.metric("Ovulacion", ovulacion.strftime("%d/%m/%Y"))
            st.metric("Dias hasta proximo", (proximo_periodo - hoy).days)
        with col3:
            st.metric("Ventana fertil", f"{inicio_fertil.strftime('%d/%m')} al {fin_fertil.strftime('%d/%m')}")
        
        st.markdown("---")
        st.header("Informacion en Tiempo Real")
        
        with st.expander("Clima y Sintomas", expanded=True):
            clima_data = obtener_clima(ciudad)
            if clima_data:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Temperatura", f"{clima_data['temperatura']}C")
                with col2:
                    st.metric("Humedad", f"{clima_data['humedad']}%")
                with col3:
                    st.metric("Condicion", clima_data['descripcion'].title())
                
                if clima_data['humedad'] > 80:
                    st.info("Alta humedad: Puede aumentar la retencion de liquidos")
                if clima_data['temperatura'] > 30:
                    st.info("Temperatura alta: Mantente hidratada y evita exposicion prolongada al sol")
                if clima_data['temperatura'] < 18:
                    st.info("Temperatura baja: El frio puede intensificar los colicos, mantente abrigada")
            else:
                st.warning("Configura tu API Key de OpenWeatherMap para ver informacion del clima")
                st.write("Ve a: https://openweathermap.org/api")
        
        with st.expander("Nutricion para tu Fase", expanded=True):
            consejos_nutricion = obtener_consejos_nutricion(fase_actual)
            st.write(consejos_nutricion)
            
            st.info("Tip: Estos alimentos pueden ayudar a balancear tus hormonas y reducir sintomas")
        
        with st.expander("Noticias de Salud Femenina", expanded=True):
            noticias = obtener_noticias_salud()
            if noticias:
                for i, noticia in enumerate(noticias, 1):
                    st.write(f"{i}. {noticia['title']}")
                    if noticia['description']:
                        st.write(f"   {noticia['description']}")
                    st.write(f"   Leer mas: {noticia['url']}")
                    if i < len(noticias):
                        st.markdown("---")
            else:
                st.warning("Configura tu API Key de NewsAPI para ver noticias actualizadas")
                st.write("Ve a: https://newsapi.org")
        
        st.markdown("---")
        st.subheader("Grafica de tu Ciclo")
        
        dias = pd.date_range(fecha_ultima, proximo_periodo)
        fases = []
        for d in dias:
            if fecha_ultima <= d < fecha_ultima + datetime.timedelta(days=duracion_periodo):
                fases.append("Menstrual")
            elif fecha_ultima + datetime.timedelta(days=duracion_periodo) <= d < ovulacion:
                fases.append("Folicular")
            elif d == ovulacion:
                fases.append("Ovulacion")
            else:
                fases.append("Lutea")

        df = pd.DataFrame({"Fecha": dias, "Fase": fases})
        colores = {"Menstrual": "#ff6b6b", "Folicular": "#feca57", "Ovulacion": "#48dbfb", "Lutea": "#1dd1a1"}
        df["Color"] = df["Fase"].map(colores)

        fig, ax = plt.subplots(figsize=(10, 2))
        ax.bar(df["Fecha"], [1]*len(df), color=df["Color"], width=1.0)
        ax.set_yticks([])
        ax.set_xticks([fecha_ultima, ovulacion, proximo_periodo])
        ax.set_xticklabels(["Inicio", "Ovulacion", "Proximo"])
        ax.set_title("Timeline de tu Ciclo Menstrual")
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        
    else:
        st.warning("Selecciona una fecha valida")

st.markdown("---")
st.header("Como Obtener tus API Keys")

col1, col2 = st.columns(2)

with col1:
    st.subheader("OpenWeatherMap")
    st.write("1. Ve a openweathermap.org")
    st.write("2. Registrate (gratis)")
    st.write("3. Ve a API Keys")
    st.write("4. Copia tu key")

with col2:
    st.subheader("NewsAPI") 
    st.write("1. Ve a newsapi.org")
    st.write("2. Registrate con Google")
    st.write("3. Verifica tu email")
    st.write("4. Copia tu key")

st.markdown("---")
st.write("App del Ciclo Menstrual con APIs | Desarrollado con Streamlit")