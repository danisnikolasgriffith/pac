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
    vf_lordo_costi = Ii + (Ir * 12 * anni)
else:
    vf_lordo_costi = (Ii * (1 + P)**anni) + (Ir * 12 * (((1 + P)**anni - 1) / P))
delta_lordo_costi = vf_lordo_costi - capitale_versato

costi_una_tantum = Ii * Ci
costi_totali = costi_una_tantum + (vf_lordo_costi - (vf_lordo_costi / ((1 + Cr)**anni)))
vf_netto_costi = vf_lordo_costi - costi_totali
delta_netto_costi = vf_netto_costi - capitale_versato

# Calcolo tasse su delta
delta_tassabile = max(0, delta_netto_costi)
tasse = delta_tassabile * T
vf_netto_fiscale = vf_netto_costi - tasse
delta_netto_fiscale = vf_netto_fiscale - capitale_versato

# Calcolo valore reale (potere d'acquisto)
vf_netto_inflazione = vf_netto_fiscale / ((1 + I)**anni)
delta_netto_inflazione = vf_netto_fiscale - capitale_versato

# 3. Risultati e Visualizzazione
st.subheader("Risultati")

# Banner Semaforo (Lordo Costi)
if delta_lordo_costi > 0:
    st.success("Il piano (lordo costi) è in POSITIVO")
elif abs(delta_lordo_costi) < 0.01:
    st.warning("Il piano (lordo costi) è NEUTRO")
else:
    st.error("Il piano (lordo costi) è in NEGATIVO")

# Banner Semaforo (Netto Costi)
if delta_netto_costi > 0:
    st.success("Il piano (netto costi) è in POSITIVO")
elif abs(delta_netto_costi) < 0.01:
    st.warning("Il piano (netto costi) è NEUTRO")
else:
    st.error("Il piano (netto costi) è in NEGATIVO")

# Banner Semaforo (Netto Tasse)
if delta_netto_fiscale > 0:
    st.success("Il piano (netto tasse) è in POSITIVO")
elif abs(delta_netto_fiscale) < 0.01:
    st.warning("Il piano (netto tasse) è NEUTRO")
else:
    st.error("Il piano (netto tasse) è in NEGATIVO")

# Banner Semaforo (Netto inflazione)
if delta_netto_inflazione > 0:
    st.success("Il piano (netto inflazione) è in POSITIVO")
elif abs(delta_netto_inflazione) < 0.01:
    st.warning("Il piano (netto inflazione) è NEUTRO")
else:
    st.error("Il piano (netto inflazione) è in NEGATIVO")

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
display_row_right_aligned("Valore Finale Lordo Costi", vf_lordo_costi, ((vf_lordo_costi/capitale_versato)-1)*100)
display_row_right_aligned("Costi Totali", costi_totali, (costi_totali/capitale_versato)*100)
display_row_right_aligned("Valore Finale Netto Costi", vf_netto_costi, ((vf_netto_costi/capitale_versato)-1)*100)
display_row_right_aligned("Profitto/Perdita", delta_netto_costi, (delta_netto_costi/capitale_versato)*100)
st.divider()
display_row_right_aligned("Valore Finale    Netto Tasse", vf_netto_fiscale, ((vf_netto_fiscale/capitale_versato)-1)*100)
display_row_right_aligned("Profitto/Perdita Netto Tasse", delta_netto_fiscale, (delta_netto_fiscale/capitale_versato)*100)
st.divider()
display_row_right_aligned("Valore Finale    Netto Inflazione", vf_netto_inflazione, ((vf_netto_inflazione/capitale_versato)-1)*100)
display_row_right_aligned("Profitto/Perdita Netto Inflazione", delta_netto_inflazione, (delta_netto_inflazione/capitale_versato)*100) 

# Visualizzazione Grafica
st.subheader("Composizione Valore Finale")
df = pd.DataFrame({
    "Componente": ["Valore Finale Lordo Costi", "Valore Finale Netto Costi", "Valore Finale Netto Tasse", "Valore Finale Netto Inflazione",],
    "Valore": [vf_lordo_costi, vf_netto_costi, vf_netto_fiscale, vf_netto_inflazione]
})
fig = px.bar(df, x="Componente", y="Valore", color="Componente", text_auto='.2s')
st.plotly_chart(fig, use_container_width=True)

# Visualizzazione Profitto/Perdita
st.subheader("Composizione Valore Finale")
df = pd.DataFrame({
    "Componente": ["Lordo Costi", "Netto Costi", "Netto Tasse", "Netto Inflazione",],
    "Valore": [delta_lordo_costi, delta_netto_costi, delta_netto_fiscale, delta_netto_inflazione]
})
fig = px.bar(df, x="Componente", y="Valore", color="Componente", text_auto='.2s')
st.plotly_chart(fig, use_container_width=True)
