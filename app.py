import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparador Luz Grupo Finanzas", page_icon="⚡", layout="centered")

# Estilo para el título principal
st.markdown("<h1 style='text-align: center;'>⚡ Comparador de Tarifas Eléctricas</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Análisis exclusivo para el Grupo Finanzas</p>", unsafe_allow_html=True)

# --- BARRA LATERAL (DATOS) ---
with st.sidebar:
    st.header("📋 Tus Datos")
    dias = st.number_input("Días de la factura", value=30)
    
    st.subheader("Potencia (kW)")
    p1_kw = st.number_input("Punta - P1", value=3.5, step=0.1)
    p2_kw = st.number_input("Valle - P2", value=3.5, step=0.1)
    
    st.subheader("Consumo (kWh)")
    c1_kwh = st.number_input("Energía Punta (P1)", value=50.0)
    c2_kwh = st.number_input("Energía Llana (P2)", value=50.0)
    c3_kwh = st.number_input("Energía Valle (P3)", value=100.0)

# --- BASE DE DATOS (Las 14 tarifas del Excel) ---
tarifas = [
    {"Nombre": "OCTOPUS SUN CLUB", "p1": 0.097, "p2": 0.027, "e1": 0.12, "e2": 0.12, "e3": 0.12},
    {"Nombre": "ESLUZ SOLAR FIJA 2.0", "p1": 0.080247, "p2": 0.007407, "e1": 0.182, "e2": 0.134, "e3": 0.085},
    {"Nombre": "NUFRI Flex", "p1": 0.094533, "p2": 0.046371, "e1": 0.165812, "e2": 0.090774, "e3": 0.058239},
    {"Nombre": "IMAGINA Tarifa base (Sin horas)", "p1": 0.087, "p2": 0.044, "e1": 0.105, "e2": 0.105, "e3": 0.105},
    {"Nombre": "IMAGINA (Noches y findes)", "p1": 0.10184, "p2": 0.022498, "e1": 0.177691, "e2": 0.10387, "e3": 0.069473},
    {"Nombre": "Doméstica-Visalia Luz Fijo", "p1": 0.060274, "p2": 0.060274, "e1": 0.101995, "e2": 0.101995, "e3": 0.101995},
    {"Nombre": "REPSOL Ahorro Plus", "p1": 0.068219, "p2": 0.068219, "e1": 0.1299, "e2": 0.1299, "e3": 0.1299},
    {"Nombre": "Enérgya VM Formula Fija", "p1": 0.082192, "p2": 0.002739, "e1": 0.166, "e2": 0.130, "e3": 0.103},
    {"Nombre": "Iberdrola Plan Online", "p1": 0.091074, "p2": 0.013483, "e1": 0.191661, "e2": 0.133374, "e3": 0.099645},
    {"Nombre": "Naturgy Noche", "p1": 0.12303, "p2": 0.037337, "e1": 0.1802, "e2": 0.1072, "e3": 0.0718},
    {"Nombre": "Endesa One Luz", "p1": 0.090214, "p2": 0.090214, "e1": 0.1476, "e2": 0.0792, "e3": 0.0558},
    {"Nombre": "Total Energies A tu aire", "p1": 0.072603, "p2": 0.072575, "e1": 0.173572, "e2": 0.10393, "e3": 0.076176},
    {"Nombre": "CHC energía PLAN VEHICULO", "p1": 0.088356, "p2": 0.088356, "e1": 0.219, "e2": 0.219, "e3": 0.059},
    {"Nombre": "PVPC-REGULADO", "p1": 0.084431, "p2": 0.001987, "e1": 0.1732, "e2": 0.1042, "e3": 0.0862},
]

# --- LÓGICA DE CÁLCULO ---
VALOR_BS_DIARIO = 0.57363674 / 30 
VALOR_ALQ_DIARIO = 0.81 / 30
IEE_FACTOR = 0.0511269
IVA_FACTOR = 0.21

resultados = []
for t in tarifas:
    coste_pot = (p1_kw * t["p1"] * dias) + (p2_kw * t["p2"] * dias)
    coste_ene = (c1_kwh * t["e1"]) + (c2_kwh * t["e2"]) + (c3_kwh * t["e3"])
    bono_social = VALOR_BS_DIARIO * dias
    alquiler = VALOR_ALQ_DIARIO * dias
    base_iee = coste_pot + coste_ene + bono_social
    iee = base_iee * IEE_FACTOR
    total_bruto = base_iee + iee + alquiler
    total_neto = total_bruto * (1 + IVA_FACTOR)
    
    resultados.append({
        "Compañía": t["Nombre"],
        "Total Factura (€)": round(total_neto, 2),
        "Ahorro Estimado (€)": 0 # Se calcula abajo
    })

# --- PROCESAMIENTO DE TOP 3 ---
df = pd.DataFrame(resultados).sort_values("Total Factura (€)").reset_index(drop=True)

# Calculamos el ahorro respecto a la peor opción de la lista (para dar perspectiva)
peor_precio = df["Total Factura (€)"].max()
df["Ahorro Estimado (€)"] = round(peor_precio - df["Total Factura (€)"], 2)

# Solo nos quedamos con las 3 primeras
df_top3 = df.head(3).copy()
df_top3.index = df_top3.index + 1 # Ranking 1, 2, 3

# --- INTERFAZ DE RESULTADOS ---
mejor = df_top3.iloc[0]

# Rótulo grande para el ganador
st.markdown(f"""
    <div style="background-color:#00c853; padding:25px; border-radius:15px; text-align:center; color:white; margin-bottom:25px;">
        <h2 style="margin:0;">🏆 LA OPCIÓN MÁS BARATA</h2>
        <h1 style="margin:10px 0; font-size:45px;">{mejor['Compañía']}</h1>
        <h2 style="margin:0;">{mejor['Total Factura (€)']} € / mes</h2>
        <p style="margin:5px 0 0 0; opacity:0.9;">¡Ahorras {mejor['Ahorro Estimado (€)']}€ respecto a la tarifa más cara!</p>
    </div>
    """, unsafe_allow_html=True)

st.subheader("🥈🥉 Resto del Podio")
st.table(df_top3)

st.info("💡 Nota: Los cálculos se realizan de forma privada en tu navegador. Tus datos no se guardan en ningún servidor.")
