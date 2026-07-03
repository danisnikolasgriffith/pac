import streamlit as st

st.title("Dashboard Analisi PAC")

# 1. Sidebar per gli INPUT (Variabili indipendenti)
st.sidebar.header("Parametri PAC")
Ii = st.sidebar.number_input("Contributo Iniziale (€)", value=1800, step=100)
Ir = st.sidebar.number_input("Contributo Mensile (€)", value=150, step=10)
Ci = st.sidebar.slider("Costo una-tantum (%)", 0.0, 5.0, 0.0) / 100
Cr = st.sidebar.slider("Costi ricorrenti annui (%)", 0.0, 5.0, 2.0) / 100
P = st.sidebar.slider("Performance annua attesa (%)", -20.0, 40.0, 5.0) / 100
anni = st.sidebar.slider("Orizzonte temporale (anni)", 1, 20, 5)

# 2. Logica di Calcolo
# Capitale investito totale
capitale_versato = Ii + (Ir * 12 * anni)

# Calcolo Valore Finale Netto (Semplificato)
# Applico il rendimento netto dei costi ricorrenti al montante
rendimento_netto = P - Cr
Vnf = (Ii * (1 - Ci) * (1 + rendimento_netto)**anni) + \
      (Ir * 12 * ((1 + rendimento_netto)**anni - 1) / rendimento_netto if rendimento_netto != 0 else Ir * 12 * anni)

delta = Vnf - capitale_versato

# 3. Output
st.subheader("Risultati")
col1, col2, col3 = st.columns(3)
col1.metric("Capitale Versato", f"{capitale_versato:,.2f} €")
col2.metric("Valore Finale Netto", f"{Vnf:,.2f} €")
col3.metric("Profitto/Perdita", f"{delta:,.2f} €", delta_color="normal")

# Visualizzazione Semaforo
if delta > 0:
    st.success("Il piano è in POSITIVO")
elif delta == 0:
    st.warning("Il piano è NEUTRO")
else:
    st.error("Il piano è in NEGATIVO")
