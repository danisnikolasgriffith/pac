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
Cr = st.sidebar.slider("Costi ricorrenti annui (%)", 0.0, 3.0, 1.5, step=0.1) / 100
P = st.sidebar.slider("Performance annua attesa (%)", -20.0, 20.0, 0.0, step=0.5) / 100
st.sidebar.divider()
I = st.sidebar.slider("Inflazione annua (%)", 0.0, 5.0, 2.0, step=0.5) / 100
T = st.sidebar.selectbox("Aliquota Fiscale (%)", [12.5, 26.0]) / 100
st.sidebar.divider()
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
delta = Vnf - capitale_versato # profitto/perdita

# Calcolo tasse su delta
delta_tassabile = max(0, delta)
tasse = delta_tassabile * T
Vnf_netto_fiscale = Vnf - tasse
delta_netto_fiscale = Vnf_netto_fiscale - capitale_versato

# Calcolo valore reale (potere d'acquisto)
Vnf_netto_inflazione = Vnf_netto_fiscale / ((1 + I)**anni)
delta_netto_inflazione = Vnf_netto_inflazione - capitale_versato

# 3. Risultati e Visualizzazione
st.subheader("Risultati")

# Banner Semaforo
if delta > 0:
    st.success("Il piano è in POSITIVO")
elif abs(delta) < 0.01:
    st.warning("Il piano è NEUTRO")
else:
    st.error("Il piano è in NEGATIVO")

def display_row_right_aligned(label, value_abs, value_pct=None):
    col_label, col_abs, col_pct = st.columns([2, 1, 1])
    with col_label:
        st.markdown(f"**{label}**")
    with col_abs:
        # Allineamento a destra usando il padding
        st.markdown(f"<div style='text-align: right'>{value_abs:,.2f} €</div>", unsafe_allow_html=True)
    with col_pct:
        if value_pct is not None:
            # Allineamento a destra per le percentuali
            st.markdown(f"<div style='text-align: right'>({value_pct:+.2f}%)</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='text-align: right'>-</div>", unsafe_allow_html=True)

# Visualizzazione in elenco dettagliato
st.write("### Dettaglio Finanziario")
display_row_right_aligned("Capitale Versato", capitale_versato)
display_row_right_aligned("Valore Finale Lordo Costi", Vfl, ((Vfl/capitale_versato)-1)*100)
display_row_right_aligned("Costi Totali", costi_totali, (costi_totali/capitale_versato)*100)
display_row_right_aligned("Valore Finale Netto Costi", Vnf, ((Vnf/capitale_versato)-1)*100)
display_row_right_aligned("Profitto/Perdita", delta, (delta/capitale_versato)*100)
st.divider()
display_row_right_aligned("Valore Finale    Netto Tasse", Vnf_netto_fiscale, ((Vnf_netto_fiscale/capitale_versato)-1)*100)
display_row_right_aligned("Profitto/Perdita Netto Tasse", delta_netto_fiscale, (delta_netto_fiscale/capitale_versato)*100)
st.divider()
display_row_right_aligned("Valore Finale    Netto Inflazione", Vnf_netto_inflazione, ((Vnf_netto_inflazione/capitale_versato)-1)*100)
display_row_right_aligned("Profitto/Perdita Netto Inflazione", delta_netto_inflazione, (delta_netto_inflazione/capitale_versato)*100) 

# Visualizzazione Grafica
st.subheader("Composizione Valore Finale")
df = pd.DataFrame({
    "Componente": ["Capitale Versato", "Costi", "Profitto Netto"],
    "Valore": [capitale_versato, costi_totali, max(0, delta)]
})
fig = px.bar(df, x="Componente", y="Valore", color="Componente", text_auto='.2s')
st.plotly_chart(fig, use_container_width=True)
