import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Analisi PAC", layout="wide")
st.title("Dashboard Analisi PAC")

# 1. Sidebar per gli INPUT
st.sidebar.header("Parametri PAC")
Ii = st.sidebar.slider("Contributo Iniziale (€)", 0, 20000, 1800, step=1000)
Ir = st.sidebar.slider("Contributo Mensile (€)", 50, 500, 150, step=50)
Ci = st.sidebar.slider("Costo una-tantum (%)", 0.0, 5.0, 0.0) / 100
Cr = st.sidebar.slider("Costi ricorrenti annui (%)", 0.0, 5.0, 2.0) / 100
P = st.sidebar.slider("Performance annua attesa (%)", -20.0, 20.0, 0.0, step=0.5) / 100
anni = st.sidebar.slider("Orizzonte temporale (anni)", 1, 20, 5)

# 2. Logica di Calcolo
capitale_versato = Ii + (Ir * 12 * anni)

if P == 0:
    Vfl = Ii + (Ir * 12 * anni)
else:
    Vfl = (Ii * (1 + P)**anni) + (Ir * 12 * (((1 + P)**anni - 1) / P))

costi_una_tantum = Ii * Ci
costi_totali = costi_una_tantum + (Vfl - (Vfl / ((1 + Cr)**anni)))
Vnf = Vfl - costi_totali
delta = Vnf - capitale_versato

# 3. Risultati e Visualizzazione
st.subheader("Risultati")

# Banner Semaforo
if delta > 0:
    st.success("Il piano è in POSITIVO")
elif abs(delta) < 0.01:
    st.warning("Il piano è NEUTRO")
else:
    st.error("Il piano è in NEGATIVO")

# Visualizzazione in elenco dettagliato
st.write("### Dettaglio Finanziario")
st.markdown(f"- **Capitale Versato:** {capitale_versato:,.2f} €")
st.markdown(f"- **Valore Finale Lordo:** {Vfl:,.2f} € ({((Vfl/capitale_versato)-1)*100:+.2f}%)")
st.markdown(f"- **Costi Totali:** {costi_totali:,.2f} € ({(costi_totali/capitale_versato)*100:.2f}%)")
st.markdown(f"- **Valore Finale Netto:** {Vnf:,.2f} € ({((Vnf/capitale_versato)-1)*100:+.2f}%)")
st.markdown(f"- **Profitto/Perdita:** {delta:,.2f} € ({((delta/capitale_versato)*100):+.2f}%)")

# Visualizzazione Grafica
st.subheader("Composizione Valore Finale")
df = pd.DataFrame({
    "Componente": ["Capitale Versato", "Costi", "Profitto Netto"],
    "Valore": [capitale_versato, costi_totali, max(0, delta)]
})
fig = px.bar(df, x="Componente", y="Valore", color="Componente", text_auto='.2s')
st.plotly_chart(fig, use_container_width=True)
