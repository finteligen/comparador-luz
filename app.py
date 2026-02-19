import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Comparador Luz - Finteligen", page_icon="⚡", layout="centered")

# 2. Marca de agua y fecha en el lateral (Superior Izquierda)
with st.sidebar:
    st.markdown(f"""
        <div style='background-color: #f9f9f9; padding: 10px; border-radius: 10px; border: 1px solid #eeeeee;'>
            <p style='margin: 0; font-size: 0.8rem; color: #888;'>Desarrollado por:</p>
            <a href='https://www.finteligen.com' target='_blank' style='text-decoration: none; color: #00c853; font-weight: bold;'>www.finteligen.com</a>
            <p style='margin-top: 10px; margin-bottom: 0; font-size: 0.75rem; color: #aaa;'>Actualizado a:</p>
            <p style='margin: 0; font-size: 0.85rem; font-weight: bold;'>19 de febrero de 2026</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.header("📋 Introduce tus datos")
    dias = st.number_input("Días de factura", value=30)
    p1_kw = st.number_input("Potencia Punta - P1 (kW)", value=3.5, step=0.1)
    p2_kw = st.number_input("Potencia Valle - P2 (kW)", value=3.5, step=0.1)
    
    st.subheader("Consumos (kWh)")
    c1 = st.number_input("Energía Punta (P1)", value=50.0)
    c2 = st.number_input("Energía Llana (P2)", value=50.0)
    c3 = st.number_input("Energía Valle (P3)", value=100.0)

# 3. Título Principal
st.markdown("<h1 style='text-align: center;'>⚡ Comparador de Tarifas Eléctricas</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Selección de las 3 mejores opciones del mercado</p>", unsafe_allow_html=True)

# 4. Base de Datos (13 Tarifas - Esluz Eliminada)
tarifas = [
    {"Nombre": "OCTOPUS SUN CLUB", "p1": 0.097, "p2": 0.027, "e1": 0.12, "e2": 0.12, "e3": 0.12},
    {"Nombre": "NUFRI Flex", "p1": 0.094533, "p2": 0.046371, "e1": 0.165812, "e2": 0.090774, "e3": 0.058239},
    {"Nombre": "IMAGINA Tarifa base (Sin horas)", "p1": 0.087, "p2": 0.044, "e1": 0.105, "e2": 0.105, "e3": 0.105},
    {"Nombre": "IMAGINA (Noches y findes)", "p1": 0.10184, "p2": 0.022498, "e1": 0.177691, "e2": 0.10387, "e3": 0.069473},
    {"Nombre": "Doméstica-Visalia Luz Fijo", "p1": 0.060274, "p2": 0.060274, "e1": 0.101995, "e2": 0.101995, "e3": 0.101995},
    {"Nombre": "REPSOL Ahorro Plus", "p1": 0.068219, "p2": 0.068219, "e1": 0.1299, "e2": 0.1299, "e3": 0.1299},
    {"Nombre": "Enérgya VM Formula Fija", "p1": 0.08219178, "p2": 0.00273863, "e1": 0.166, "e2": 0.130, "e3": 0.103},
    {"Nombre": "Iberdrola Plan Online", "p1": 0.091074, "p2": 0.013483, "e1": 0.191661, "e2": 0.133374, "e3": 0.099645},
    {"Nombre": "Naturgy Noche", "p1": 0.12303, "p2": 0.037337, "e1": 0.1802, "e2": 0.1072, "e3": 0.0718},
    {"Nombre": "Endesa One Luz", "p1": 0.09021370, "p2": 0.09021370, "e1": 0.1476, "e2": 0.0792, "e3": 0.0558},
    {"Nombre": "Total Energies A tu aire", "p1": 0.072603, "p2": 0.072575, "e1": 0.173572, "e2": 0.10393, "e3": 0.076176},
    {"Nombre": "CHC energía PLAN VEHICULO", "p1": 0.088356, "p2": 0.088356, "e1": 0.219, "e2": 0.219, "e3": 0.059},
    {"Nombre": "PVPC-REGULADO", "p1": 0.08443127, "p2": 0.00198746, "e1": 0.1732, "e2": 0.1042, "e3": 0.0862},
]

# 5. Lógica Matemática (Fiel al Excel)
BS_DIARIO = 0.57363674 / 30 
ALQ_DIARIO = 0.81 / 30
IEE_FACTOR = 0.0511269
IVA_FACTOR = 0.21

resultados = []
for t in tarifas:
    c_pot = (p1_kw * t["p1"] * dias) + (p2_kw * t["p2"] * dias)
    c_ene = (c1 * t["e1"]) + (c2 * t["e2"]) + (c3 * t["e3"])
    bono_social = BS_DIARIO * dias
    alquiler = ALQ_DIARIO * dias
    
    # 1º Suma para Impuesto Eléctrico
    base_iee = c_pot + c_ene + bono_social
    iee = base_iee * IEE_FACTOR
    
    # 2º Suma para IVA
    total_bruto = base_iee + iee + alquiler
    total_neto = total_bruto * (1 + IVA_FACTOR)
    
    resultados.append({
        "Compañía": t["Nombre"],
        "Total Factura (€)": round(total_neto, 2)
    })

# 6. Ordenación y Filtrado (TOP 3)
df_final = pd.DataFrame(resultados).sort_values("Total Factura (€)").reset_index(drop=True)
df_top3 = df_final.head(3).copy()
df_top3.index = df_top3.index + 1  # Ranking 1, 2, 3

# 7. Interfaz de Resultados
mejor = df_top3.iloc[0]

st.markdown(f"""
    <div style="background-color:#00c853; padding:25px; border-radius:15px; text-align:center; color:white; margin:20px 0; border: 2px solid #ffffff; box-shadow: 0px 4px 12px rgba(0,0,0,0.1);">
        <h3 style="margin:0; font-weight: 300; letter-spacing: 1px;">🥇 MEJOR OPCIÓN ENCONTRADA</h3>
        <h1 style="margin:10px 0; font-size:42px; font-weight: bold;">{mejor['Compañía']}</h1>
        <h2 style="margin:0; font-size:32px;">{mejor['Total Factura (€)']} € <span style="font-size: 1rem;">(Estimación mensual)</span></h2>
    </div>
    """, unsafe_allow_html=True)

st.subheader("🥈🥉 Podio de Ahorro")
st.table(df_top3)

st.info("Los precios son estimativos basados en las tarifas vigentes a fecha de actualización.")
