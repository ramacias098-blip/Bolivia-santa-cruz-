
import streamlit as st
import pandas as pd

# Configuración de la página web
st.set_page_config(
    page_title="Sistema de Importaciones y Landed Cost Bolivia - Miguel Macias",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para apariencia profesional y logos de importación
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
    }
    .main-header p {
        color: #e0e6ed;
        font-size: 1.05rem;
        margin-top: 6px;
        margin-bottom: 0;
    }
    .badge-miguel {
        background-color: #ffc107;
        color: #000000;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
        display: inline-block;
        margin-top: 8px;
    }
    .card-box {
        background-color: #f8f9fa;
        border-left: 5px solid #2a5298;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Encabezado Principal con Logos e Iconos de Importación
st.markdown("""
<div class="main-header">
    <h1>🚢 📦 🛃 Portal de Importaciones y Landed Cost Bolivia</h1>
    <p>Plataforma Integral de Clasificación Arancelaria NANDINA, Costos Logísticos e Impuestos Aduaneros (ANB)</p>
    <div class="badge-miguel">👤 Desarrollado por: Miguel Macias</div>
</div>
""", unsafe_allow_html=True)

# Base de Datos Extendida de Partidas Arancelarias NANDINA para Bolivia
BASE_DATOS_NANDINA = [
    {
        "producto": "Laptops y Computadoras Portátiles",
        "partida": "8471.30.00.00",
        "ga": 0.0,
        "ice": 0.0,
        "unidad": "Unidades",
        "certificados": "Ninguno (Libre importación)",
        "descripcion": "Máquinas automáticas para tratamiento o procesamiento de datos, portátiles de peso <= 10kg."
    },
    {
        "producto": "Celulares y Smartphones",
        "partida": "8517.13.00.00",
        "ga": 0.0,
        "ice": 0.0,
        "unidad": "Unidades",
        "certificados": "Homologación ATT (Bolivia)",
        "descripcion": "Teléfonos inteligentes para redes celulares o inalámbricas."
    },
    {
        "producto": "Sillas de Oficina y Muebles Giratorios",
        "partida": "9401.30.00.00",
        "ga": 0.15,
        "ice": 0.0,
        "unidad": "Unidades",
        "certificados": "Ninguno",
        "descripcion": "Asientos giratorios ajustables en altura para oficina o hogar."
    },
    {
        "producto": "Calzado Deportivo y Zapatillas",
        "partida": "6404.11.00.00",
        "ga": 0.30,
        "ice": 0.0,
        "unidad": "Pares",
        "certificados": "Etiquetado de Origen / IBNORCA",
        "descripcion": "Calzado de deporte con suela de caucho o plástico y parte superior de materia textil."
    },
    {
        "producto": "Prendas de Vestir / Camisetas de Algodón",
        "partida": "6109.10.00.00",
        "ga": 0.20,
        "ice": 0.0,
        "unidad": "Piezas",
        "certificados": "Certificado de Origen (si aplica APRI/ACE)",
        "descripcion": "Camisetas de punto, de algodón para hombre, mujer o niños."
    },
    {
        "producto": "Vehículos de Pasajeros (Automóviles)",
        "partida": "8703.23.10.00",
        "ga": 0.15,
        "ice": 0.18,
        "unidad": "Unidades",
        "certificados": "Inspección Técnica Ambiental / Senasag (si aplica)",
        "descripcion": "Automóviles de turismo con motor de émbolo alternativo de cilindrada > 1500cm3 pero <= 3000cm3."
    },
    {
        "producto": "Repuestos de Automóvil / Pastillas y Discos de Freno",
        "partida": "8708.30.00.00",
        "ga": 0.10,
        "ice": 0.0,
        "unidad": "Piezas / Sets",
        "certificados": "Ninguno",
        "descripcion": "Frenos y servofrenos; sus partes para vehículos automóviles."
    },
    {
        "producto": "Paneles Solares y Células Fotovoltaicas",
        "partida": "8541.43.00.00",
        "ga": 0.0,
        "ice": 0.0,
        "unidad": "Piezas",
        "certificados": "Incentivo Energías Renovables",
        "descripcion": "Células fotovoltaicas ensambladas en módulos o compuestas en paneles."
    },
    {
        "producto": "Suplementos Alimenticios y Vitaminas",
        "partida": "2106.90.90.00",
        "ga": 0.10,
        "ice": 0.0,
        "unidad": "Frascos / Cajas",
        "certificados": "Registro Sanitario SENASAG / UNIMED",
        "descripcion": "Preparaciones alimenticias no expresadas ni comprendidas en otra parte."
    },
    {
        "producto": "Cosméticos y Cremas para la Piel",
        "partida": "3304.99.00.00",
        "ga": 0.10,
        "ice": 0.0,
        "unidad": "Unidades",
        "certificados": "Registro Sanitario AGEMED",
        "descripcion": "Preparaciones de belleza, maquillaje y cuidado de la piel."
    }
]

# Panel Lateral de Configuración
st.sidebar.title("🛠️ Panel de Control")
st.sidebar.markdown("**Autor:** Miguel Macias")
st.sidebar.markdown("---")

tipo_cambio = st.sidebar.number_input("💵 Tipo de Cambio (BOB / USD):", min_value=1.0, value=6.96, step=0.01)
modalidad_transporte = st.sidebar.selectbox("🚢 Vía de Transporte:", ["Marítimo FCL (Contenedor)", "Marítimo LCL (Carga Consolidada)", "Aéreo Express", "Terrestre Internacional"])

st.sidebar.markdown("---")
st.sidebar.info("📌 **Recuerda:** En Bolivia, la base imponible del IVA de Importación incluye el CIF + GA + ICE, generando la alícuota efectiva del **14.94%**.")

# Pestañas Principales
tab1, tab2, tab3, tab4 = st.tabs([
    "🔎 1. Clasificación Arancelaria (NANDINA)",
    "🚚 2. Costos Logísticos e Impuestos",
    "📊 3. Resumen y Cotización Landed Cost",
    "💰 4. Simulador de Margen de Ganancia y Venta"
])

with tab1:
    st.subheader("Buscador Inteligente de Partida Arancelaria")
    st.markdown("Escriba el nombre o categoría del producto para obtener la subpartida arancelaria correspondiente en la Aduana Nacional de Bolivia.")
    
    col_search1, col_search2 = st.columns([2, 1])
    with col_search1:
        busqueda_prod = st.text_input("🔍 Escriba el producto a consultar:", value="Laptops y Computadoras Portátiles")
    
    # Filtrar coincidencia
    match = next((item for item in BASE_DATOS_NANDINA if busqueda_prod.lower() in item["producto"].lower()), None)
    
    if match:
        partida_cod = match["partida"]
        ga_porcentaje = match["ga"] * 100
        ice_porcentaje = match["ice"] * 100
        certif = match["certificados"]
        desc_det = match["descripcion"]
    else:
        partida_cod = "8471.90.00.00"
        ga_porcentaje = 10.0
        ice_porcentaje = 0.0
        certif = "Verificación Estándar ANB"
        desc_det = "Partida genérica para productos no catalogados específicamente."

    with col_search2:
        st.markdown(f"### Partida NANDINA\n`{partida_cod}`")
    
    st.markdown(f"""
    <div class="card-box">
        <h4>📋 Ficha Arancelaria Sugerida</h4>
        <ul>
            <li><b>Código NANDINA:</b> <code>{partida_cod}</code></li>
            <li><b>Descripción Oficial:</b> {desc_det}</li>
            <li><b>Gravamen Arancelario (GA):</b> <span style="color:#2a5298; font-weight:bold;">{ga_porcentaje:.1f}%</span></li>
            <li><b>Impuesto al Consumo Específico (ICE):</b> {ice_porcentaje:.1f}%</li>
            <li><b>Certificaciones Requeridas en Bolivia:</b> {certif}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col_adj1, col_adj2 = st.columns(2)
    with col_adj1:
        ga_custom = st.number_input("Ajustar Gravamen Arancelario GA (%):", min_value=0.0, max_value=40.0, value=float(ga_porcentaje), step=0.5) / 100.0
    with col_adj2:
        ice_custom = st.number_input("Ajustar Impuesto ICE (% si aplica):", min_value=0.0, max_value=80.0, value=float(ice_porcentaje), step=1.0) / 100.0

with tab2:
    st.subheader("Parámetros de Compra, Logística e Impuestos Aduaneros")
    
    col_log1, col_log2 = st.columns(2)
    
    with col_log1:
        st.markdown("#### 📦 Datos de la Mercancía")
        cant_unidades = st.number_input("Cantidad de Unidades a Importar:", min_value=1, value=100)
        precio_fob_u = st.number_input("Precio FOB Unitario ($USD):", min_value=0.01, value=45.00)
        fob_total_val = cant_unidades * precio_fob_u
        st.caption(f"**Valor FOB Total Mercancía:** `${fob_total_val:,.2f} USD`")
        
        st.markdown("#### 🚢 Fletes y Seguros de Transporte")
        flete_marit_aereo = st.number_input("Flete Internacional Tramo 1 (Origen a Puerto/Aeropuerto) ($USD):", min_value=0.0, value=350.0)
        flete_terrestre_bo = st.number_input("Flete Terrestre Tramo 2 (Puerto Arica/Iquique a Bolivia) ($USD):", min_value=0.0, value=180.0)
        seguro_carga = st.number_input("Seguro Internacional de Transporte ($USD):", min_value=0.0, value=40.0)
    
    with col_log2:
        st.markdown("#### 🛃 Gastos Nacionales y Despacho Aduanero en Bolivia")
        gastos_aspb_dab = st.number_input("Puerto y Almacenes (ASPB / DAB) ($USD):", min_value=0.0, value=90.0)
        honorarios_agente = st.number_input("Agente Despachante de Aduana (ADA) ($USD):", min_value=0.0, value=130.0)
        tramites_cert = st.number_input("Certificaciones, Senasag, Fideicomisos ($USD):", min_value=0.0, value=60.0)
        transporte_local = st.number_input("Flete Local (Aduana Interna a Almacén Final) ($USD):", min_value=0.0, value=50.0)
        
        st.markdown("#### 🏛️ Configuración de Impuestos (ANB)")
        aplica_iva_efectivo = st.checkbox("Aplicar Alícuota Efectiva IVA Importación (14.94%)", value=True)
        alicuota_iva = 0.1494 if aplica_iva_efectivo else 0.13

# CÁLCULOS MATEMÁTICOS DE COSTO LANDED
cif_frontera = fob_total_val + flete_marit_aereo + flete_terrestre_bo + seguro_carga
monto_ga_calc = cif_frontera * ga_custom
monto_ice_calc = cif_frontera * ice_custom

base_imponible_iva = cif_frontera + monto_ga_calc + monto_ice_calc
monto_iva_calc = base_imponible_iva * alicuota_iva

total_gastos_operativos = gastos_aspb_dab + honorarios_agente + tramites_cert + transporte_local
total_impuestos = monto_ga_calc + monto_ice_calc + monto_iva_calc

costo_landed_total_usd = cif_frontera + total_impuestos + total_gastos_operativos
costo_landed_unit_usd = costo_landed_total_usd / cant_unidades

costo_landed_total_bob = costo_landed_total_usd * tipo_cambio
costo_landed_unit_bob = costo_landed_unit_usd * tipo_cambio
factor_multiplicador = costo_landed_unit_usd / precio_fob_u

with tab3:
    st.subheader("📊 Resumen del Costo Landed y Factor de Importación")
    
    # Métricas Principales
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Costo Unitario Final (USD)", f"${costo_landed_unit_usd:,.2f}", f"+{((factor_multiplicador - 1)*100):.1f}% vs FOB")
    k2.metric("Costo Unitario Final (BOB)", f"Bs. {costo_landed_unit_bob:,.2f}")
    k3.metric("Costo Total Operación (USD)", f"${costo_landed_total_usd:,.2f}")
    k4.metric("Factor de Importación", f"{factor_multiplicador:.3f}x")
    
    st.markdown("---")
    
    st.subheader("📋 Desglose Detallado de la Póliza de Importación")
    
    tabla_datos = [
        {"Concepto Operativo": "1. Valor FOB Mercancía", "Monto USD": fob_total_val, "Monto BOB": fob_total_val * tipo_cambio, "% de Participación": (fob_total_val / costo_landed_total_usd)*100},
        {"Concepto Operativo": "2. Fletes y Seguro (Internacional + Terrestre)", "Monto USD": flete_marit_aereo + flete_terrestre_bo + seguro_carga, "Monto BOB": (flete_marit_aereo + flete_terrestre_bo + seguro_carga) * tipo_cambio, "% de Participación": ((flete_marit_aereo + flete_terrestre_bo + seguro_carga) / costo_landed_total_usd)*100},
        {"Concepto Operativo": "3. VALOR CIF FRONTERA / ADUANA", "Monto USD": cif_frontera, "Monto BOB": cif_frontera * tipo_cambio, "% de Participación": (cif_frontera / costo_landed_total_usd)*100},
        {"Concepto Operativo": f"4. Gravamen Arancelario - GA ({ga_custom*100:.1f}%)", "Monto USD": monto_ga_calc, "Monto BOB": monto_ga_calc * tipo_cambio, "% de Participación": (monto_ga_calc / costo_landed_total_usd)*100},
        {"Concepto Operativo": f"5. Impuesto ICE ({ice_custom*100:.1f}%)", "Monto USD": monto_ice_calc, "Monto BOB": monto_ice_calc * tipo_cambio, "% de Participación": (monto_ice_calc / costo_landed_total_usd)*100},
        {"Concepto Operativo": f"6. IVA Importación ({alicuota_iva*100:.2f}%)", "Monto USD": monto_iva_calc, "Monto BOB": monto_iva_calc * tipo_cambio, "% de Participación": (monto_iva_calc / costo_landed_total_usd)*100},
        {"Concepto Operativo": "7. Gastos Puerto, Almacenes y Despachante", "Monto USD": total_gastos_operativos, "Monto BOB": total_gastos_operativos * tipo_cambio, "% de Participación": (total_gastos_operativos / costo_landed_total_usd)*100},
        {"Concepto Operativo": "TOTAL COSTO LANDED PUESTO EN ALMACÉN", "Monto USD": costo_landed_total_usd, "Monto BOB": costo_landed_total_bob, "% de Participación": 100.0}
    ]
    
    df_resumen = pd.DataFrame(tabla_datos)
    st.dataframe(df_resumen.style.format({"Monto USD": "${:,.2f}", "Monto BOB": "Bs. {:,.2f}", "% de Participación": "{:.1f}%"}), use_container_width=True)
    
    st.info("💡 **Análisis de Utilidad:** Si tu precio FOB original fue de **$" + f"{precio_fob_u:,.2f} USD** por unidad, tu costo total puesto en Bolivia es de **${costo_landed_unit_usd:,.2f} USD** (o **Bs. {costo_landed_unit_bob:,.2f} BOB**). Debes establecer tu precio de venta considerando este costo landed.")

    # Opción para descargar la cotización en CSV
    csv_data = df_resumen.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Cotización de Importación (CSV / Excel)",
        data=csv_data,
        file_name="cotizacion_importacion_bolivia_miguel_macias.csv",
        mime="text/csv"
    )

with tab4:
    st.subheader("💰 Simulador de Margen de Ganancia y Precios de Venta en Bolivia")
    st.markdown("Establezca su precio de venta al público en Bolivia para proyectar la rentabilidad neta considerando impuestos comerciales (IVA e IT).")
    
    col_sal1, col_sal2 = st.columns(2)
    
    with col_sal1:
        st.markdown("#### 🏷️ Precio de Venta Proyectado")
        pvp_unit_bob = st.number_input("Precio de Venta al Público por Unidad (BOB):", min_value=0.0, value=float(round(costo_landed_unit_bob * 1.4, 2)), step=10.0)
        pvp_unit_usd = pvp_unit_bob / tipo_cambio
        
        gastos_comerciales_u_bob = st.number_input("Gastos Comerciales/Publicidad por Unidad (BOB):", min_value=0.0, value=15.0, step=5.0)
        gastos_comerciales_u_usd = gastos_comerciales_u_bob / tipo_cambio
        
    with col_sal2:
        st.markdown("#### 🧾 Régimen Tributario Comercial (SIN Bolivia)")
        venta_con_factura = st.checkbox("Emitir Factura Comercial al Vender (IVA 13% + IT 3%)", value=True)
        
        if venta_con_factura:
            debito_iva_u_bob = pvp_unit_bob * 0.13
            it_u_bob = pvp_unit_bob * 0.03
            credito_iva_import_u_bob = (monto_iva_calc * tipo_cambio) / cant_unidades
            st.caption(f"**Crédito Fiscal IVA recuperable por importación:** `Bs. {credito_iva_import_u_bob:,.2f} / unidad`")
        else:
            debito_iva_u_bob = 0.0
            it_u_bob = 0.0
            credito_iva_import_u_bob = 0.0

    # CÁLCULOS DE RENTABILIDAD
    ingreso_total_bob = pvp_unit_bob * cant_unidades
    ingreso_total_usd = ingreso_total_bob / tipo_cambio
    
    costo_landed_mas_gastos_u_bob = costo_landed_unit_bob + gastos_comerciales_u_bob + debito_iva_u_bob + it_u_bob
    costo_landed_mas_gastos_u_usd = costo_landed_mas_gastos_u_bob / tipo_cambio
    
    utilidad_neta_u_bob = pvp_unit_bob - costo_landed_mas_gastos_u_bob + credito_iva_import_u_bob
    utilidad_neta_u_usd = utilidad_neta_u_bob / tipo_cambio
    
    utilidad_neta_total_bob = utilidad_neta_u_bob * cant_unidades
    utilidad_neta_total_usd = utilidad_neta_total_bob / tipo_cambio
    
    roi_porcentaje = (utilidad_neta_u_bob / costo_landed_unit_bob) * 100 if costo_landed_unit_bob > 0 else 0.0
    margen_sobre_venta = (utilidad_neta_u_bob / pvp_unit_bob) * 100 if pvp_unit_bob > 0 else 0.0

    st.markdown("---")
    st.subheader("📈 Proyección Financiera de Ventas y Utilidad Neta")
    
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Ingreso Total Ventas (BOB)", f"Bs. {ingreso_total_bob:,.2f}", f"${ingreso_total_usd:,.2f} USD")
    r2.metric("Utilidad Neta por Unidad", f"Bs. {utilidad_neta_u_bob:,.2f}", f"${utilidad_neta_u_usd:,.2f} USD")
    r3.metric("Utilidad Neta Total Lote", f"Bs. {utilidad_neta_total_bob:,.2f}", f"${utilidad_neta_total_usd:,.2f} USD")
    r4.metric("Rentabilidad Neta (ROI)", f"{roi_porcentaje:.1f}%", f"{margen_sobre_venta:.1f}% sobre Venta")
    
    if utilidad_neta_u_bob > 0:
        st.success(f"🎉 **Operación Rentable:** Tu ganancia neta estimada por cada unidad vendida es de **Bs. {utilidad_neta_u_bob:,.2f}** (o **${utilidad_neta_u_usd:,.2f} USD**), generando un retorno sobre inversión (ROI) del **{roi_porcentaje:.1f}%**.")
    else:
        st.error(f"⚠️ **Atención:** El precio de venta seleccionado está por debajo de los costos totales e impuestos. Se requiere un precio mínimo de venta de **Bs. {costo_landed_mas_gastos_u_bob:,.2f}** para no perder dinero.")

# Pie de Página Oficial
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; font-size: 0.9rem;">
    🚢 <b>Plataforma de Cálculo de Importaciones y Costos Landed Bolivia</b><br>
    Desarrollado por <b>Miguel Macias</b> | Basado en Normativa Aduana Nacional de Bolivia (ANB) y Nomenclatura NANDINA
</div>
""", unsafe_allow_html=True)

