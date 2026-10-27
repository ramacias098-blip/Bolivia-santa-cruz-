import streamlit as st
import pandas as pd
import unicodedata

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y RENDIMIENTO (SIN LIBRERÍAS EXTERNAS)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Calculadora de Importaciones Bolivia 2026 - Miguel Macias",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

def normalizar_texto(texto: str) ->str:
    if not texto:
        return ""
    nfkd = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).lower().strip()

@st.cache_data
def obtener_base_datos_nandina_2026():
    return [
        # TECNOLOGÍA
        {
            "categoria": "💻 Tecnología y Electrónica",
            "producto": "Celulares y Teléfonos Inteligentes (Smartphones)",
            "partida": "8517.13.00.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Homologación ATT (Autoridad de Telecomunicaciones)",
            "descripcion": "Teléfonos inteligentes para redes celulares o inalámbricas (Incentivo Digital GA 0%).",
            "keywords": "celular telefono smartphone iphone samsung xiaomi redmi huawei movil"
        },
        {
            "categoria": "💻 Tecnología y Electrónica",
            "producto": "Televisores, Smart TV y Monitores",
            "partida": "8528.72.00.00",
            "ga": 0.10,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Etiquetado de Eficiencia Energética IBNORCA",
            "descripcion": "Aparatos receptores de televisión en color, Smart TVs, monitores y pantallas LED/OLED.",
            "keywords": "televisor tele tv smarttv monitor pantalla lg samsung sony roku hisense"
        },
        {
            "categoria": "💻 Tecnología y Electrónica",
            "producto": "Laptops y Computadoras Portátiles",
            "partida": "8471.30.00.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Ninguno (Libre Importación)",
            "descripcion": "Máquinas automáticas para tratamiento de datos, portátiles de peso <= 10kg.",
            "keywords": "laptop notebook computadora pc dell hp lenovo macbook mac procesador"
        },
        # BEBIDAS Y TABACO (CON ICE)
        {
            "categoria": "🍷 Bebidas Alcohólicas y Tabaco",
            "producto": "Whisky, Ron, Gin, Tequila y Licores",
            "partida": "2208.30.00.00",
            "ga": 0.15,
            "ice": 0.20,
            "unidad": "Botellas / Litros",
            "certificados": "Registro Sanitario SENASAG + Timbre Control Fiscal ANB",
            "descripcion": "Aguardientes, licores y demás bebidas espirituosas alcohólicas.",
            "keywords": "whisky ron gin tequila licor bebida alcoholica etiqueta negra red label johnnie walker"
        },
        {
            "categoria": "🍷 Bebidas Alcohólicas y Tabaco",
            "producto": "Vinos de Uva y Espumantes",
            "partida": "2204.21.00.00",
            "ga": 0.20,
            "ice": 0.15,
            "unidad": "Botellas",
            "certificados": "Registro Sanitario SENASAG",
            "descripcion": "Vinos de uvas frescas, incluidos los vinos enriquecidos con alcohol.",
            "keywords": "vino tinto blanco espumante champagne chardonnay cabernet"
        },
        {
            "categoria": "🍷 Bebidas Alcohólicas y Tabaco",
            "producto": "Cerveza de Malta",
            "partida": "2203.00.00.00",
            "ga": 0.20,
            "ice": 0.25,
            "unidad": "Latas / Botellas",
            "certificados": "Registro Sanitario SENASAG",
            "descripcion": "Cerveza obtenida a partir de malta de cebada.",
            "keywords": "cerveza lata botella malta corona heineken paceña"
        },
        {
            "categoria": "🍷 Bebidas Alcohólicas y Tabaco",
            "producto": "Cigarrillos, Tabaco y Vapeadores",
            "partida": "2402.20.00.00",
            "ga": 0.30,
            "ice": 0.50,
            "unidad": "Cajetillas / Unidades",
            "certificados": "Timbre Fiscal de Control + Autorización Ministerio de Salud",
            "descripcion": "Cigarrillos que contengan tabaco o sucedáneos, vapeadores y esencias.",
            "keywords": "cigarro cigarrillo tabaco vape vapeador vaper pod marlboro"
        },
        # VEHÍCULOS
        {
            "categoria": "🚗 Vehículos y Repuestos",
            "producto": "Vehículos Eléctricos e Híbridos",
            "partida": "8703.80.00.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Inspección Ambiental / DS Vehículos Ecológicos (0% GA)",
            "descripcion": "Automóviles propulsados únicamente con motor eléctrico o híbridos.",
            "keywords": "auto electrico hybrido tesla BYD carro ecologico bateria"
        },
        {
            "categoria": "🚗 Vehículos y Repuestos",
            "producto": "Automóviles a Gasolina / Diésel",
            "partida": "8703.23.10.00",
            "ga": 0.15,
            "ice": 0.18,
            "unidad": "Unidades",
            "certificados": "Inspección Técnica Ambiental y Senasag (si aplica)",
            "descripcion": "Automóviles de turismo con motor de cilindrada > 1500cm3 y <= 3000cm3.",
            "keywords": "auto carro coche camioneta toyota suzuki nissan gasolina diesel"
        },
        {
            "categoria": "🚗 Vehículos y Repuestos",
            "producto": "Repuestos de Auto (Frenos, Discos, Pastillas)",
            "partida": "8708.30.00.00",
            "ga": 0.10,
            "ice": 0.0,
            "unidad": "Piezas / Sets",
            "certificados": "Ninguno",
            "descripcion": "Frenos y servofrenos y sus partes para vehículos automotores.",
            "keywords": "repuesto freno pastilla disco amortiguador suspension autoparte"
        },
        # OTROS
        {
            "categoria": "☀️ Energías Renovables",
            "producto": "Paneles Solares y Kit Fotovoltaico",
            "partida": "8541.43.00.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Piezas",
            "certificados": "Incentivo Energías Limpias (Arancel 0%)",
            "descripcion": "Células fotovoltaicas ensambladas en módulos o compuestas en paneles.",
            "keywords": "panel solar modulo fotovoltaico energia solar inversor kit solar"
        },
        {
            "categoria": "👟 Calzado y Textil",
            "producto": "Calzado Deportivo y Zapatillas",
            "partida": "6404.11.00.00",
            "ga": 0.30,
            "ice": 0.0,
            "unidad": "Pares",
            "certificados": "Etiquetado de Origen / Normativa IBNORCA",
            "descripcion": "Calzado de deporte con suela de caucho o plástico y parte textil.",
            "keywords": "zapatilla tenis calzado zapato deportivo nike adidas puma"
        }
    ]

# Estilos CSS Modernos
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
        padding: 26px;
        border-radius: 16px;
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    }
    .main-header h1 { color: #ffffff !important; font-size: 2.2rem !important; font-weight: 800 !important; margin: 0 0 6px 0 !important; }
    .main-header p { color: #e0e6ed !important; font-size: 1.05rem !important; margin: 0 !important; }
    .badge-miguel { background-color: #ffc107; color: #111111; padding: 5px 16px; border-radius: 25px; font-weight: 700; font-size: 0.88rem; display: inline-block; margin-top: 10px; }
    .card-info { background-color: #ffffff; border: 1px solid #e1e8ed; border-left: 6px solid #2C5364; padding: 16px; border-radius: 10px; margin-bottom: 16px; }
    .card-ai { background-color: #f8fafc; border: 1px solid #cbd5e1; border-left: 6px solid #0284c7; padding: 16px; border-radius: 10px; margin-bottom: 16px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🚢 📦 🛃 Portal de Importaciones y Landed Cost Bolivia 2026</h1>
    <p>Plataforma Inteligente de Clasificación Arancelaria NANDINA e Impuestos Aduaneros (ANB)</p>
    <div class="badge-miguel">👤 Desarrollado por: Miguel Macias</div>
</div>
""", unsafe_allow_html=True)

base_nandina = obtener_base_datos_nandina_2026()

st.sidebar.title("🛠️ Configuración General")
st.sidebar.markdown("**Autor:** Miguel Macias")
st.sidebar.markdown("---")
tipo_cambio = st.sidebar.number_input("💵 Tipo de Cambio Oficial (BOB / USD):", min_value=1.0, value=6.96, step=0.01)

tab1, tab2, tab3, tab4 = st.tabs([
    "🤖 1. Asistente Arancelario Inteligente",
    "🚚 2. Costos Logísticos e Impuestos",
    "📊 3. Resumen y Gráficos Landed Cost",
    "💰 4. Simulador de Margen y Precio Venta"
])

# PESTAÑA 1: ASISTENTE IA Y CLASIFICADOR
with tab1:
    st.subheader("🤖 Asistente de Clasificación Arancelaria NANDINA 2026")
    st.markdown("Escriba su consulta en lenguaje natural o busque el producto a clasificar en la Aduana Nacional de Bolivia.")

    col_q1, col_q2 = st.columns([2, 1])
    with col_q1:
        busqueda_input = st.text_input("🔍 Consulta o Producto (ej. celular, televisor, whisky, vino, laptop, autos):", value="Celulares y Teléfonos Inteligentes")
    with col_q2:
        cat_filtro = st.selectbox("Filtrar por Categoría:", ["Todas"] + sorted(list(set(x["categoria"] for x in base_nandina))))

    query_norm = normalizar_texto(busqueda_input)
    coincidencias = []
    for item in base_nandina:
        if cat_filtro != "Todas" and item["categoria"] != cat_filtro:
            continue
        p_norm = normalizar_texto(item["producto"])
        k_norm = normalizar_texto(item["keywords"])
        part_norm = normalizar_texto(item["partida"])
        if query_norm in p_norm or query_norm in k_norm or query_norm in part_norm:
            coincidencias.append(item)
        else:
            palabras = query_norm.split()
            if any(p in p_norm or p in k_norm for p in palabras if len(p) > 2):
                coincidencias.append(item)

    if coincidencias:
        prod_sel = coincidencias[0]
        coincid_ok = True
    else:
        prod_sel = {
            "categoria": "⚙️ Partida General Configurable",
            "producto": busqueda_input if busqueda_input else "Mercancía General",
            "partida": "8471.90.00.00",
            "ga": 0.10,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Verificación Aduanera ANB Estándar",
            "descripcion": "Partida general asignada. Puede personalizar la tasa de GA/ICE abajo."
        }
        coincid_ok = False

    ga_orig = prod_sel["ga"] * 100
    ice_orig = prod_sel["ice"] * 100

    # Respuesta del Asistente Virtual IA
    st.markdown(f"""
    <div class="card-ai">
        <h4>🤖 Respuesta del Asistente Comercial Miguel Macias:</h4>
        <p>Para la importación de <b>{prod_sel['producto']}</b> en Bolivia, la Aduana Nacional asigna la subpartida <code>{prod_sel['partida']}</code>.</p>
        <ul>
            <li><b>Gravamen Arancelario (GA):</b> <b>{ga_orig:.1f}%</b></li>
            <li><b>Impuesto al Consumo Específico (ICE):</b> <b>{ice_orig:.1f}%</b></li>
            <li><b>IVA Importación Efectivo:</b> <b>14.94%</b></li>
            <li><b>Certificaciones y Permisos:</b> {prod_sel['certificados']}</li>
        </ul>
        <p><small><i>{prod_sel['descripcion']}</i></small></p>
    </div>
    """, unsafe_allow_html=True)

    c_adj1, c_adj2 = st.columns(2)
    with c_adj1:
        ga_aplicado = st.number_input("Ajustar GA (%):", min_value=0.0, max_value=40.0, value=float(ga_orig), step=0.5) / 100.0
    with c_adj2:
        ice_aplicado = st.number_input("Ajustar ICE (% si aplica):", min_value=0.0, max_value=80.0, value=float(ice_orig), step=1.0) / 100.0

# PESTAÑA 2: LOGÍSTICA E IMPUESTOS
with tab2:
    st.subheader("Parámetros de Compra, Logística e Impuestos")
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.markdown("#### 📦 Origen y Fletes")
        cant_unidades = st.number_input("Cantidad de Unidades:", min_value=1, value=100)
        precio_fob_u = st.number_input("Precio FOB Unitario ($USD):", min_value=0.01, value=45.0)
        flete_int = st.number_input("Flete Internacional ($USD):", min_value=0.0, value=350.0)
        flete_terr = st.number_input("Flete Terrestre a Bolivia ($USD):", min_value=0.0, value=180.0)
        seguro_int = st.number_input("Seguro Internacional ($USD):", min_value=0.0, value=40.0)
    with col_l2:
        st.markdown("#### 🛃 Gastos Aduana e Impuestos")
        gastos_puerto = st.number_input("Puerto y Almacenes ($USD):", min_value=0.0, value=90.0)
        agente_ada = st.number_input("Despachante de Aduana ADA ($USD):", min_value=0.0, value=130.0)
        certificaciones = st.number_input("Trámites y Certificados ($USD):", min_value=0.0, value=60.0)
        flete_local = st.number_input("Flete Local Almacén ($USD):", min_value=0.0, value=50.0)

# CÁLCULOS
fob_total = cant_unidades * precio_fob_u
cif_total = fob_total + flete_int + flete_terr + seguro_int

monto_ga = cif_total * ga_aplicado
monto_ice = cif_total * ice_aplicado
base_iva = cif_total + monto_ga + monto_ice
monto_iva = base_iva * 0.1494

gastos_op_total = gastos_puerto + agente_ada + certificaciones + flete_local
impuestos_total = monto_ga + monto_ice + monto_iva

costo_landed_total_usd = cif_total + impuestos_total + gastos_op_total
costo_landed_unit_usd = costo_landed_total_usd / cant_unidades

costo_landed_total_bob = costo_landed_total_usd * tipo_cambio
costo_landed_unit_bob = costo_landed_unit_usd * tipo_cambio
factor_multiplicador = costo_landed_unit_usd / precio_fob_u

# PESTAÑA 3: RESUMEN Y GRÁFICOS COMPATIBLES
with tab3:
    st.subheader("📊 Resumen Ejecutivo y Estructura de Costos")
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Costo Unitario Final (USD)", f"${costo_landed_unit_usd:,.2f}", f"+{((factor_multiplicador - 1)*100):.1f}% vs FOB")
    k2.metric("Costo Unitario Final (BOB)", f"Bs. {costo_landed_unit_bob:,.2f}")
    k3.metric("Costo Total Operación (USD)", f"${costo_landed_total_usd:,.2f}")
    k4.metric("Factor Multiplicador", f"{factor_multiplicador:.3f}x")

    st.markdown("---")
    st.subheader("📈 Distribución Porcentual del Costo Landed")

    # Gráfico de barras nativo de Streamlit (sin depender de plotly)
    df_chart = pd.DataFrame({
        "Componente": ["FOB Mercancía", "Fletes y Seguro", "Impuesto GA", "Impuesto ICE", "Impuesto IVA (14.94%)", "Gastos Operativos"],
        "Monto ($USD)": [fob_total, (flete_int + flete_terr + seguro_int), monto_ga, monto_ice, monto_iva, gastos_op_total]
    }).set_index("Componente")

    st.bar_chart(df_chart)

    st.markdown("---")
    st.subheader("📋 Tabla Oficial de Desglose de Póliza")

    tabla_datos = [
        {"Concepto": "1. Valor FOB Mercancía", "Monto USD": fob_total, "Monto BOB": fob_total * tipo_cambio, "% Total": (fob_total/costo_landed_total_usd)*100},
        {"Concepto": "2. Fletes y Seguro Internacional", "Monto USD": flete_int + flete_terr + seguro_int, "Monto BOB": (flete_int + flete_terr + seguro_int) * tipo_cambio, "% Total": ((flete_int + flete_terr + seguro_int)/costo_landed_total_usd)*100},
        {"Concepto": "3. VALOR CIF ADUANA FRONTERA", "Monto USD": cif_total, "Monto BOB": cif_total * tipo_cambio, "% Total": (cif_total/costo_landed_total_usd)*100},
        {"Concepto": f"4. Gravamen Arancelario GA ({ga_aplicado*100:.1f}%)", "Monto USD": monto_ga, "Monto BOB": monto_ga * tipo_cambio, "% Total": (monto_ga/costo_landed_total_usd)*100},
        {"Concepto": f"5. Impuesto ICE ({ice_aplicado*100:.1f}%)", "Monto USD": monto_ice, "Monto BOB": monto_ice * tipo_cambio, "% Total": (monto_ice/costo_landed_total_usd)*100},
        {"Concepto": "6. IVA Importación Efectivo (14.94%)", "Monto USD": monto_iva, "Monto BOB": monto_iva * tipo_cambio, "% Total": (monto_iva/costo_landed_total_usd)*100},
        {"Concepto": "7. Gastos Despacho, Puerto y Almacenes", "Monto USD": gastos_op_total, "Monto BOB": gastos_op_total * tipo_cambio, "% Total": (gastos_op_total/costo_landed_total_usd)*100},
        {"Concepto": "TOTAL COSTO LANDED PUESTO EN ALMACÉN", "Monto USD": costo_landed_total_usd, "Monto BOB": costo_landed_total_bob, "% Total": 100.0}
    ]

    df_resumen = pd.DataFrame(tabla_datos)
    st.dataframe(df_resumen.style.format({"Monto USD": "${:,.2f}", "Monto BOB": "Bs. {:,.2f}", "% Total": "{:.1f}%"}), use_container_width=True)

# PESTAÑA 4: SIMULADOR DE MARGEN Y VENTA
with tab4:
    st.subheader("💰 Simulador de Precio de Venta y Margen de Ganancia")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        pvp_bob = st.number_input("Precio de Venta al Público (Bs. BOB):", min_value=0.0, value=float(round(costo_landed_unit_bob * 1.35, 2)))
        gastos_mkt_bob = st.number_input("Gastos Comercialización / Publicidad (Bs. BOB):", min_value=0.0, value=15.0)
    with col_s2:
        factura_comercial = st.checkbox("Emitir Factura Comercial al Vender (IVA 13% + IT 3%)", value=True)
        if factura_comercial:
            debito_iva_bob = pvp_bob * 0.13
            it_bob = pvp_bob * 0.03
            credito_iva_import = (monto_iva * tipo_cambio) / cant_unidades
            st.caption(f"**Crédito Fiscal IVA recuperado por importación:** `Bs. {credito_iva_import:,.2f} / unidad`")
        else:
            debito_iva_bob = 0.0
            it_bob = 0.0
            credito_iva_import = 0.0

    ingreso_total_bob = pvp_bob * cant_unidades
    costo_venta_unit_bob = costo_landed_unit_bob + gastos_mkt_bob + debito_iva_bob + it_bob - credito_iva_import
    
    utilidad_unit_bob = pvp_bob - costo_venta_unit_bob
    utilidad_unit_usd = utilidad_unit_bob / tipo_cambio
    utilidad_total_bob = utilidad_unit_bob * cant_unidades
    utilidad_total_usd = utilidad_total_bob / tipo_cambio

    roi = (utilidad_unit_bob / costo_landed_unit_bob) * 100 if costo_landed_unit_bob > 0 else 0.0

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Ingreso Ventas Total", f"Bs. {ingreso_total_bob:,.2f}")
    r2.metric("Ganancia Neta / Unidad", f"Bs. {utilidad_unit_bob:,.2f}", f"${utilidad_unit_usd:,.2f} USD")
    r3.metric("Ganancia Neta Lote Total", f"Bs. {utilidad_total_bob:,.2f}", f"${utilidad_total_usd:,.2f} USD")
    r4.metric("ROI (Retorno de Inversión)", f"{roi:.1f}%")

    if utilidad_unit_bob > 0:
        st.success(f"🎉 **Operación Rentable:** Ganancia neta estimada de **Bs. {utilidad_unit_bob:,.2f} BOB** (${utilidad_unit_usd:,.2f} USD) por unidad, con un ROI del **{roi:.1f}%**.")
    else:
        st.error(f"⚠️ **Atención:** El precio seleccionado genera pérdidas. Se requiere un precio mínimo de **Bs. {(costo_landed_unit_bob + gastos_mkt_bob):,.2f}**.")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748b;'>🚢<b>Portal de Importaciones y Landed Cost Bolivia 2026</b><br>Desarrollado por<b>Miguel Macias</b></div>", unsafe_allow_html=True)
