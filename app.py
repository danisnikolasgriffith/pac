import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Analisi PAC", layout="wide")
st.title("Dashboard Analisi PAC")

# 1. Sidebar per gli INPUT
st.sidebar.header("Parametri PAC")
Ii = st.sidebar.slider("Contributo Iniziale (€)", 0, 20000, 1800, step=1000)
Ir = st.sidebar.slider("Contributo Mensile (€)", 50, 500, 150, step=100)
Ci = st.sidebar.slider("Costo una-tantum (%)", 0.0, 5.0, 0.0) / 100
Cr = st.sidebar.slider("Costi ricorrenti annui (%)", 0.0, 5.0, 2.0) / 100
P = st.sidebar.slider("Performance annua attesa (%)", -20.0, 40.0, 5.0) / 100
anni = st.sidebar.slider("Orizzonte temporale (anni)", 1, 20, 5)

# 2. Logica di Calcolo
capitale_versato = Ii + (Ir * 12 * anni)
rendimento_netto = P - Cr

# Valore Finale Lordo (Performance lorda applicata al capitale)
Vfl = (Ii * (1 + P)**anni) + (Ir * 12 * ((1 + P)**anni - 1) / P if P != 0 else Ir * 12 * anni)

# Costi (Una-tantum + Impatto costi ricorrenti)
costi_una_tantum = Ii * Ci
costi_totali = costi_una_tantum + (Vfl * (Cr / (P if P != 0 else 1)) * (1 - (1+P)**-anni)) # Semplificazione impatto Cr

# Valore Finale Netto
Vnf = Vfl - costi_totali
delta = Vnf - capitale_versato

# 3. Risultati e Visualizzazione
st.subheader("Risultati")

# Semaforo
if delta > 0:
    st.success("Il piano è in POSITIVO")
elif delta == 0:
    st.warning("Il piano è NEUTRO")
else:
    st.error("Il piano è in NEGATIVO")

# Metriche dettagliate
col1, col2 = st.columns(2)

with col1:
    st.metric("Capitale Versato", f"{capitale_versato:,.2f} €")
    st.metric("Valore Finale Lordo", f"{Vfl:,.2f} € ({((Vfl/capitale_versato)-1)*100:+.2f}%)")
    st.metric("Costi Totali", f"{costi_totali:,.2f} € ({(costi_totali/capitale_versato)*100:.2f}%)")

with col2:
    st.metric("Valore Finale Netto", f"{Vnf:,.2f} € ({((Vnf/capitale_versato)-1)*100:+.2f}%)")
    st.metric("Profitto/Perdita", f"{delta:,.2f} €", delta_color="normal")

# Visualizzazione Grafica
st.subheader("Composizione Valore Finale")
df = pd.DataFrame({
    "Componente": ["Capitale Versato", "Costi", "Profitto Netto"],
    "Valore": [capitale_versato, costi_totali, max(0, delta)]
})
fig = px.bar(df, x="Componente", y="Valore", color="Componente", text_auto='.2s')
st.plotly_chart(fig, use_container_width=True)
