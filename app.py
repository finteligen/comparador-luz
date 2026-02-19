import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Comparador Luz Grupo Finanzas", page_icon="⚡", layout="centered")

# --- MARCA DE AGUA Y FECHA (LATERAL IZQUIERDA) ---
with st.sidebar:
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; border: 1px solid #d1d5db; margin-bottom: 20px;'>
            <p style='margin: 0; font-size: 0.85rem; color: #555;'>Desarrollado por:</p>
            <p style='margin: 0; font-weight: bold; color: #1f2937;'>www.finteligen.com</p>
            <hr style='margin: 10px 0;'>
            <p style='margin: 0; font-size: 0.8rem; color: #666;'>📅 Actualizado a:</p>
            <p style='margin: 0; font-weight: bold; color: #1f2937;'>19 de febrero de 2026</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("📋 Datos de Factura")
    dias = st.number_input("Días de la factura", value=30)
    
    st.subheader("Potencia (kW)")
    p1_kw = st.number_input("Punta - P1", value=3.5, step=0.1)
    p2_kw = st.number_input("Valle - P2", value=3.5, step=0.1)
    
    st.subheader("Consumo (kWh)")
    c1_kwh = st.number_input("Energía Punta (P1)", value=50.0)
    c2_kwh = st.number_input("Energía Llana (P2)", value=50.0)
    c3_kwh = st.number_input("Energía Valle (P3)", value=100.0)

# Título Principal
st.markdown("<h1 style='text-align: center; color: #1f2937;'>⚡ Comparador de Tarifas Eléctricas</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Podio de las 3 mejores opciones según tu consumo</p>", unsafe_allow_html=True)

# --- BASE DE DATOS (Sin Esluz Solar) ---
tarifas = [
    {"Nombre": "OCTOPUS SUN CLUB", "p1": 0.097, "p2": 0.027, "e1": 0.12, "e2": 0.12, "e3": 0.12},
    {"Nombre": "NUFRI Flex", "p1": 0.094533, "p2": 0.046371, "e1": 0.165812, "e2": 0.090774, "e3": 0.058239},
    {"Nombre": "IMAGINA Tarifa base (Sin horas)", "p1": 0.087, "p2": 0.044, "e1": 0.105, "e2": 0.105, "e3": 0.105},
    {"Nombre": "IMAGINA (Noches y findes)", "p1": 0.10184, "p2": 0.022498, "e1": 0.177691, "e2": 0.10387, "e3": 0.069473},
    {"Nombre": "Doméstica-Visalia Luz Fijo", "p1": 0.060274, "p2": 0.060274, "e1": 0.101995, "e2": 0.101995, "e3": 0.101995},
    {"Nombre": "REPSOL Ahorro Plus", "p1": 0.068219, "p2": 0.068219, "e1": 0.1299, "e2": 0.1299, "e3": 0.1
