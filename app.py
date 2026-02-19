import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Comparador Luz Grupo Finanzas", page_icon="⚡", layout="centered")

# --- MARCA DE AGUA Y LOGO (LATERAL SUPERIOR IZQUIERDA) ---
with st.sidebar:
    # Aquí es donde pondremos el logo cuando me lo pases. 
    # Por ahora dejo el espacio o puedes usar un emoji:
    st.markdown("### ⚡ Finteligen") 
    
    st.markdown("""
        <div style='opacity: 0.7; font-size: 0.8rem;'>
            Desarrollado por <a href='https://www.finteligen.com' target='_blank'>www.finteligen.com</a><br>
            <b>Actualizado:</b> 19 de febrero de 2026
        </div>
        """, unsafe_allow_html=True)
    st.divider()

# Título Principal
st.markdown("<h1 style='text-align: center;'>⚡ Comparador de Tarifas Eléctricas</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Análisis exclusivo para el Grupo Finanzas</p>", unsafe_allow_html=True)

# --- INPUTS ---
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

# --- BASE DE DATOS (Sin Esluz Solar) ---
tarifas = [
    {"Nombre": "OCTOPUS SUN CLUB", "p1": 0.097, "p2": 0.027, "e1": 0.12, "e2": 0.12, "e3": 0.12},
    {"Nombre": "NUFRI Flex", "p1": 0.094533, "p2": 0.046371, "e1": 0.165812, "e2": 0.090774, "e3": 0.058239},
    {"Nombre": "IMAGINA Tarifa base (Sin horas)", "p1": 0.087, "p2": 0.044, "e1": 0.105, "e2": 0.105, "e3": 0.105},
    {"Nombre": "IMAGINA (Noches y findes)", "p1": 0.10184, "p2": 0.022498, "e1": 0.177691, "e2": 0.10387, "e3": 0.069473},
    {"Nombre": "Doméstica-Visalia
