import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparador Luz Grupo Finanzas", page_icon="⚡", layout="wide")

st.title("⚡ Comparador de Tarifas Eléctricas")
st.markdown("Los cálculos incluyen Potencia, Energía, Impuesto Eléctrico (5.11%), Bono Social e IVA (21%).")

# --- BARRA LATERAL (INPUTS) ---
with st.sidebar:
    st.header("📋 Datos de Factura")
    dias = st.number_input("Días Facturados", value=30)
    
    st.subheader("Potencia Contratada (kW)")
    p1_kw = st.number_input("Punta - P1", value=3.5, step=0.1)
    p2_kw = st.number_input("Valle - P2", value=3.5, step=0.1)
    
    st.subheader("Consumo (kWh)")
    c1_kwh = st.number_input("Energía Punta - P1", value=50.0)
    c2_kwh = st.number_input("Energía Llana - P2", value=50.0)
    c3_kwh = st.number_input("Energía Valle - P3", value=100.0)

# --- BASE DE DATOS (Sincronizada con tu Excel) ---
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

# --- LÓGICA DE CÁLCULO (Clon del Excel) ---
BS_DIARIO = 0.57363674 / 30 
ALQ_DIARIO = 0.81 / 30
IEE_FACTOR = 0.0511269
IVA_FACTOR = 0.21

resultados = []

for t in tarifas:
    # Potencia y Energía
    coste_pot = (p1_kw * t["p1"] * dias) + (p2_kw * t["p2"] * dias)
    coste_ene = (c1_kwh * t["e1"]) + (c2_kwh * t["e2"]) + (c3_kwh * t["e3"])
    
    # Otros fijos
    bono_social = BS_DIARIO * dias
    alquiler = ALQ_DIARIO * dias
    
    # Impuesto Eléctrico (IEE) se aplica sobre Potencia + Energía + Bono Social
    base_iee = coste_pot + coste_ene + bono_social
    iee = base_iee * IEE_FACTOR
    
    # IVA se aplica sobre (Base IEE + IEE + Alquiler)
    total_bruto = base_iee + iee + alquiler
    iva = total_bruto * IVA_FACTOR
    
    total_neto = total_bruto + iva
    
    resultados.append({
        "Compañía": t["Nombre"],
        "Total Factura (€)": round(total_neto, 2),
        "Potencia (€)": round(coste_pot, 2),
        "Energía (€)": round(coste_ene, 2)
    })

# --- TABLA Y ORDENACIÓN ---
# 1. Crear el DataFrame
df = pd.DataFrame(resultados)

# 2. Ordenar por precio (de menor a mayor)
df = df.sort_values("Total Factura (€)")

# 3. Resetear el índice para que sea 1, 2, 3... correlativo
df = df.reset_index(drop=True)
df.index = df.index + 1

# --- MOSTRAR EN APP ---
st.subheader("📊 Tabla Comparativa (Ordenada por ahorro)")
st.table(df)

# Mensaje final con la mejor opción
mejor = df.iloc[0]
st.success(f"🏆 La mejor opción para tu consumo es **{mejor['Compañía']}** con un total de **{mejor['Total Factura (€)']}€**")
