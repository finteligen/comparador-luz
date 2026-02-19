import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparador Eléctrico VIP", page_icon="⚡")
st.title("⚡ Comparador de Tarifas (Grupo Finanzas)")

with st.sidebar:
    st.header("Tus Datos")
    dias = st.number_input("Días factura", value=30)
    p1 = st.number_input("Potencia Punta (kW)", value=3.5)
    p2 = st.number_input("Potencia Valle (kW)", value=3.5)
    c1 = st.number_input("Consumo Punta (kWh)", value=50.0)
    c2 = st.number_input("Consumo Llano (kWh)", value=50.0)
    c3 = st.number_input("Consumo Valle (kWh)", value=100.0)

# Precios extraídos de tu Excel
tarifas = [
    {"Nombre": "OCTOPUS SUN CLUB", "pp": 0.097, "pv": 0.027, "e1": 0.12, "e2": 0.12, "e3": 0.12},
    {"Nombre": "ESLUZ SOLAR FIJA 2.0", "pp": 0.080, "pv": 0.007, "e1": 0.182, "e2": 0.134, "e3": 0.085},
    {"Nombre": "NUFRI Flex", "pp": 0.094, "pv": 0.046, "e1": 0.165, "e2": 0.090, "e3": 0.058},
    {"Nombre": "NATURGY Noche", "pp": 0.123, "pv": 0.037, "e1": 0.180, "e2": 0.107, "e3": 0.071},
    {"Nombre": "PVPC (Referencia)", "pp": 0.084, "pv": 0.001, "e1": 0.173, "e2": 0.104, "e3": 0.086}
]

resultados = []
for t in tarifas:
    coste_p = (p1 * t["pp"] * dias) + (p2 * t["pv"] * dias)
    coste_e = (c1 * t["e1"]) + (c2 * t["e2"]) + (c3 * t["e3"])
    otros = (0.019 + 0.027) * dias
    subtotal = coste_p + coste_e + otros
    total = (subtotal + (subtotal * 0.0511)) * 1.21
    resultados.append({"Compañía": t["Nombre"], "Total (€)": round(total, 2)})

df = pd.DataFrame(resultados).sort_values("Total (€)")
st.table(df)
st.success(f"¡La mejor opción es {df.iloc[0]['Compañía']}!")
