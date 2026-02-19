import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparador Luz Grupo Finanzas", page_icon="⚡", layout="wide")

st.title("⚡ Comparador de Tarifas Eléctricas")
st.markdown("Introduce los datos de tu factura respetando los periodos P1, P2 y P3.")

# --- INPUTS (Nomenclatura P1, P2, P3 tal cual el Excel) ---
with st.sidebar:
    st.header("📋 Datos de Factura")
    dias = st.number_input("Días Facturados", value=30)
    
    st.subheader("Potencia (kW)")
    p1_kw = st.number_input("Punta - P1", value=3.5, step=0.1)
    p2_kw = st.number_input("Valle - P2", value=3.5, step=0.1)
    
    st.subheader("Energía (kWh)")
    c1_kwh = st.number_input("Energía Punta - P1", value=50.0)
    c2_kwh = st.number_input("Energía Llana - P2", value=50.0)
    c3_kwh = st.number_input("Energía Valle - P3", value=100.0)

# --- BASE DE DATOS EXACTA ---
tarifas = [
    {"Nombre": "OCTOPUS SUN CLUB", "p1": 0.097000, "p2": 0.027000, "e1": 0.120000, "e2": 0.120000, "e3": 0.120000},
    {"Nombre": "ESLUZ SOLAR FIJA 2.0", "p1": 0.080247, "p2": 0.007407, "e1": 0.182000, "e2": 0.134000, "e3": 0.085000},
    {"Nombre": "NUFRI Flex", "p1": 0.094533, "p2": 0.046371, "e1": 0.165812, "e2": 0.090774, "e3": 0.058239},
    {"Nombre": "IMAGINA Tarifa base (Sin horas)", "p1": 0.087000, "p2": 0.044000, "e1": 0.105000, "e2": 0.105000, "e3": 0.105000},
    {"Nombre": "IMAGINA (Noches y findes)", "p1": 0.101840, "p2": 0.022498, "e1": 0.177691, "e2": 0.103870, "e3": 0.069473},
    {"Nombre": "Doméstica-Visalia Luz Fijo", "p1": 0.060274, "p2": 0.060274, "e1": 0.101995, "e2": 0.101995, "e3": 0.101995},
    {"Nombre": "REPSOL Ahorro Plus", "p1": 0.068219, "p2": 0.068219, "e1": 0.129900, "e2": 0.129900, "e3": 0.129900},
    {"Nombre": "Enérgya VM Formula Fija", "p1": 0.082192, "p2": 0.002739, "e1": 0.166000, "e2": 0.130000, "e3": 0.103000},
    {"Nombre": "Iberdrola Plan Online", "p1": 0.091074, "p2": 0.013483, "e1": 0.191661, "e2": 0.133374, "e3": 0.099645},
    {"Nombre": "Naturgy Noche", "p1": 0.123030, "p2": 0.037337, "e1": 0.180200, "e2": 0.107200, "e3": 0.071800},
    {"Nombre": "Endesa One Luz", "p1": 0.090214, "p2": 0.090214, "e1": 0.147600, "e2": 0.079200, "e3": 0.055800},
    {"Nombre": "Total Energies A tu aire", "p1": 0.072603, "p2": 0.072575, "e1": 0.173572, "e2": 0.103930, "e3": 0.076176},
    {"Nombre": "CHC Plan Vehículo Eléctrico", "p1": 0.088356, "p2": 0.088356, "e1": 0.219000, "e2": 0.219000, "e3": 0.059000},
    {"Nombre": "PVPC (Semiregulado)", "p1": 0.084431, "p2": 0.001987, "e1": 0.173200, "e2": 0.104200, "e3": 0.086200},
]

# --- LÓGICA DE CÁLCULO (Clon del Excel) ---
# Valores diarios extraídos de tus celdas de ejemplo (30 días)
VALOR_BS_DIARIO = 0.57363674 / 30 
VALOR_ALQ_DIARIO = 0.81 / 30
IEE_FACTOR = 0.0511269
IVA_FACTOR = 0.21

resultados = []

for t in tarifas:
    # 1. Término Potencia
    coste_pot = (p1_kw * t["p1"] * dias) + (p2_kw * t["p2"] * dias)
    # 2. Término Energía
    coste_ene = (c1_kwh * t["e1"]) + (c2_kwh * t["e2"]) + (c3_kwh * t["e3"])
    # 3. Otros fijos
    bono_social = VALOR_BS_DIARIO * dias
    alquiler = VALOR_ALQ_DIARIO * dias
    
    # 4. Impuesto Eléctrico (Base = Potencia + Energía + Bono Social)
    base_iee = coste_pot + coste_ene + bono_social
    iee = base_iee * IEE_FACTOR
    
    # 5. IVA (Base = Todo lo anterior + Alquiler)
    total_bruto = base_iee + alquiler + iee
    iva = total_bruto * IVA_FACTOR
    
    total_neto = total_bruto + iva
    
    resultados.append({
        "Compañía": t["Nombre"],
        "Total Factura (€)": round(total_neto, 2),
        "P1 (€)": round(p1_kw * t["p1"] * dias, 2),
        "P2 (€)": round(p2_kw * t["p2"] * dias, 2),
        "Energía (€)": round(coste_ene, 2)
    })

# --- TABLA Y RESULTADO ---
df = pd.DataFrame(resultados).sort_values("Total Factura (€)")

st.subheader("📊 Tabla Comparativa")
st.table(df)

mejor = df.iloc[0]
st.success(f"🏆 La mejor opción es **{mejor['Nombre']}** con un total de **{mejor['Total Factura (€)']}€**")
