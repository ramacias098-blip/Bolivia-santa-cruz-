import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import unicodedata

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN GENERAL Y ESTILOS UI PREMIUM 2026
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Portal de Importaciones & Landed Cost Bolivia - Miguel Macias",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función para limpiar texto en búsquedas (normalización)
def normalizar_texto(texto: str) ->str:
    if not texto:
        return ""
    nfkd = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).lower().strip()

# Base de Datos de Partidas NANDINA Bolivia 2026 (Extendida, Fidedigna y Corregida)
@st.cache_data
def obtener_base_datos_nandina_2026():
    return [
        # TECNOLOGÍA Y COMUNICACIONES
        {
            "categoria": "📱 Tecnología & Electrónica",
            "producto": "Celulares, Smartphones e iPhones",
            "partida": "8517.13.00.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Homologación ATT Bolivia (Autoridad de Telecomunicaciones)",
            "descripcion": "Teléfonos inteligentes para redes celulares o inalámbricas. Arancel 0% DS Incentivo Tecnológico.",
            "keywords": "celular iphone samsung xiaomi smartphone telefono movil redmi huawei motorola oppo"
        },
        {
            "categoria": "📺 Electrodomésticos y Pantallas",
            "producto": "Televisores, Smart TVs y Monitores LED/OLED",
            "partida": "8528.72.00.00",
            "ga": 0.10,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Certificado Eficiencia Energética / IBNORCA",
            "descripcion": "Aparatos receptores de televisión, incluso con aparato receptor de radiodifusión o de grabación/reproducción de sonido/video incorporado.",
            "keywords": "televisor tele tv smart tv pantalla monitor led oled qled lg samsung sony tcl hisense"
        },
        {
            "categoria": "💻 Computación",
            "producto": "Laptops, Notebooks y MacBooks",
            "partida": "8471.30.00.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Libre Importación (Arancel 0%)",
            "descripcion": "Máquinas automáticas para tratamiento de datos, portátiles de peso <= 10kg.",
            "keywords": "laptop notebook computadora macbook pc dell hp lenovo mac procesador portatil"
        },

        # BEBIDAS ALCOHÓLICAS Y CIGARRILLOS (REGIMEN ESPECIAL ICE ANB)
        {
            "categoria": "🍾 Bebidas Alcohólicas & Cigarrillos",
            "producto": "Whisky, Ron, Tequila, Vodka y Gines",
            "partida": "2208.30.00.00",
            "ga": 0.15,
            "ice": 0.20,
            "unidad": "Botellas / Litros",
            "certificados": "Registro Sanitario SENASAG + Timbre de Control Fiscal (ANB)",
            "descripcion": "Aguardientes, licores y demás bebidas espirituosas. Sujeto a Gravamen Arancelario y Alícuota ICE.",
            "keywords": "whisky ron tequila vodka gin licor aguardiente johnnie walker chivas etiqueta buchanans trago alcohol"
        },
        {
            "categoria": "🍾 Bebidas Alcohólicas & Cigarrillos",
            "producto": "Vinos de Uva Fina y Espumantes",
            "partida": "2204.21.00.00",
            "ga": 0.20,
            "ice": 0.15,
            "unidad": "Botellas",
            "certificados": "Registro Sanitario SENASAG + Timbre Fiscal",
            "descripcion": "Vino de uvas frescas, incluido el vino enriquecido con alcohol. Recargo arancelario de protección nacional.",
            "keywords": "vino espumante champagne tinto blanco cabernet malbec sangria"
        },
        {
            "categoria": "🍾 Bebidas Alcohólicas & Cigarrillos",
            "producto": "Cerveza de Malta",
            "partida": "2203.00.00.00",
            "ga": 0.20,
            "ice": 0.25,
            "unidad": "Latas / Botellas / Litros",
            "certificados": "Registro Sanitario SENASAG + Timbre Fiscal",
            "descripcion": "Cerveza obtenida a partir de malta. Sometida a GA (20%) e ICE específico/ad-valorem.",
            "keywords": "cerveza heineken corona pacena huari lata botellin choff"
        },
        {
            "categoria": "🍾 Bebidas Alcohólicas & Cigarrillos",
            "producto": "Singani Boliviano y Licores Especiales",
            "partida": "2208.90.10.00",
            "ga": 0.20,
            "ice": 0.15,
            "unidad": "Botellas",
            "certificados": "Registro Sanitario SENASAG + Denominación de Origen",
            "descripcion": "Aguardiente de uva (Singani) y licores saborizados.",
            "keywords": "singani los parrales rujero licor fernet baileys amaretto"
        },
        {
            "categoria": "🍾 Bebidas Alcohólicas & Cigarrillos",
            "producto": "Cigarrillos, Tabaco y Vapeadores",
            "partida": "2402.20.00.00",
            "ga": 0.30,
            "ice": 0.50,
            "unidad": "Cajetillas / Unidades",
            "certificados": "Registro Sanitario Ministerio de Salud + Timbre Fiscal ANB",
            "descripcion": "Cigarrillos que contengan tabaco o sucedáneos. Alícuota ICE elevada del 50%.",
            "keywords": "cigarrillo tabaco marlboro camel vape pod vapeador esencia vaper"
        },

        # VEHÍCULOS Y ENERGÍAS
        {
            "categoria": "🚗 Vehículos & Maquinaria",
            "producto": "Vehículos Eléctricos e Híbridos",
            "partida": "8703.80.00.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Inspección Técnica Ambiental (DS Vehículos Ecológicos 0% GA)",
            "descripcion": "Automóviles propulsados por motor eléctrico o tecnología híbrida.",
            "keywords": "auto electrico hybrido tesla BYD carro ecologico bateria"
        },
        {
            "categoria": "🚗 Vehículos & Maquinaria",
            "producto": "Automóviles a Gasolina / Diésel",
            "partida": "8703.23.10.00",
            "ga": 0.15,
            "ice": 0.18,
            "unidad": "Unidades",
            "certificados": "Inspección Ambiental + Autorización Senasag",
            "descripcion": "Automóviles de turismo convencionales de cilindrada > 1500cm3 y <= 3000cm3.",
            "keywords": "auto carro coche camioneta toyota suzuki nissan gasolina diesel"
        },
        {
            "categoria": "🚗 Vehículos & Maquinaria",
            "producto": "Motos, Motocicletas y Cuatrimotos",
            "partida": "8711.20.00.00",
            "ga": 0.15,
            "ice": 0.10,
            "unidad": "Unidades",
            "certificados": "Inspección Ambiental / ATT si aplica control remoto",
            "descripcion": "Motocicletas con motor de émbolo alternativo de cilindrada > 50cm3 pero <= 250cm3.",
            "keywords": "moto motocicleta cuadratrack cuatrimoto scooter honda yamaha pegasus"
        },
        {
            "categoria": "☀️ Energías Renovables",
            "producto": "Paneles Solares y Kits Fotovoltaicos",
            "partida": "8541.43.00.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Piezas",
            "certificados": "Incentivo Ley Energías Limpias (0% GA)",
            "descripcion": "Módulos y paneles fotovoltaicos para generación eléctrica solar.",
            "keywords": "panel solar modulo fotovoltaico energia solar inversor kit solar"
        },
        {
            "categoria": "🏗️ Industria & Maquinaria",
            "producto": "Tractores y Maquinaria Agrícola",
            "partida": "8701.91.00.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "DS Diferimiento Arancelario Bienes de Capital (0% GA)",
            "descripcion": "Tractores e implementos agrícolas de fomento a la producción.",
            "keywords": "tractor cosechadora sembradora arado maquinaria agricola agro"
        },
        {
            "categoria": "👟 Moda & Calzado",
            "producto": "Zapatillas Deportivas y Calzado",
            "partida": "6404.11.00.00",
            "ga": 0.30,
            "ice": 0.0,
            "unidad": "Pares",
            "certificados": "Etiquetado de Origen / IBNORCA",
            "descripcion": "Calzado de deporte con suela de caucho/plástico y parte superior textil.",
            "keywords": "zapatilla tenis calzado zapato deportivo nike adidas puma jordan"
        }
    ]

# CSS Personalizado Ultra Moderno
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .hero-banner {
        background: linear-gradient(135deg, #0b132b 0%, #1c2541 50%, #3a506b 100%);
        padding: 32px;
        border-radius: 20px;
        color: #ffffff;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.12);
        margin-bottom: 28px;
    }
    
    .hero-title {
        font-size: 2.4rem !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #ffffff, #48cae4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 10px 0 !important;
    }
    
    .hero-subtitle {
        color: #cbd5e1 !important;
        font-size: 1.1rem !important;
        margin-bottom: 15px !important;
    }
    
    .badge-miguel {
        background: linear-gradient(90deg, #ffb703, #fb8500);
        color: #000000;
        padding: 6px 18px;
        border-radius: 30px;
        font-weight: 800;
        font-size: 0.9rem;
        display: inline-block;
        box-shadow: 0 4px 12px rgba(251, 133, 0, 0.3);
    }
    
    .metric-card-custom {
        background: #ffffff;
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        text-align: center;
        transition: transform 0.2s ease;
    }
    .metric-card-custom:hover {
        transform: translateY(-3px);
    }
    
    .card-ia {
        background: #f8fafc;
        border-left: 6px solid #0284c7;
        padding: 22px;
        border-radius: 14px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# ENCABEZADO PRINCIPAL HERO
# -----------------------------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🚢 Portal de Importaciones & Landed Cost Bolivia 2026</div>
    <div class="hero-subtitle">Plataforma Avanzada con Asistente Virtual IA, Clasificación NANDINA e Impuestos ANB (IVA 14.94% + ICE)</div>
    <div class="badge-miguel">👤 Desarrollado por: Miguel Macias - Consultoría & Comercio Exterior</div>
</div>
""", unsafe_allow_html=True)

base_nandina = obtener_base_datos_nandina_2026()

# BARRA LATERAL CONFIGURACIÓN
st.sidebar.title("🛠️ Panel de Control Global")
st.sidebar.markdown("**Consultor:** Miguel Macias")
st.sidebar.markdown("---")

tipo_cambio = st.sidebar.number_input("💵 Tipo de Cambio Oficial (BOB / USD):", min_value=1.0, value=6.96, step=0.01)
vía_transporte = st.sidebar.selectbox("🚢 Modalidad Logística:", [
    "Marítimo FCL (Contenedor Completo)",
    "Marítimo LCL (Carga Consolidada)",
    "Aéreo Express / Courier",
    "Terrestre Internacional"
])

st.sidebar.markdown("---")
st.sidebar.success("💡 **Actualización Normativa 2026:** Incluye alícuotas del Impuesto al Consumo Específico (ICE) para bebidas alcohólicas y cigarrillos, además del arancel 0% GA para tecnología y bienes ecológicos.")

# PESTAÑAS DE NAVEGACIÓN
tab_ia, tab_clasif, tab_costos, tab_resumen, tab_ventas = st.tabs([
    "🤖 1. Asistente Virtual IA",
    "🔎 2. Clasificación NANDINA & Arancel",
    "🚚 3. Parámetros de Costos & Impuestos",
    "📊 4. Dashboard Landed Cost",
    "💰 5. Margen de Ganancia & Ventas"
])

# -----------------------------------------------------------------------------
# PESTAÑA 1: ASISTENTE VIRTUAL IA DE IMPORTACIONES
# -----------------------------------------------------------------------------
with tab_ia:
    st.subheader("🤖 Asistente Virtual IA para Importadores en Bolivia")
    st.markdown("Consulte cualquier producto o duda normativa. La IA analizará la partida NANDINA, calculará los impuestos estimados (GA, IVA, ICE) y le indicará los requisitos en la Aduana Nacional de Bolivia (ANB).")
    
    col_ia1, col_ia2 = st.columns([2, 1])
    with col_ia1:
        consulta_ia = st.text_input("💬 Pregúntele a la IA (ej. ¿Cuánto paga importar 100 Smart TVs?, ¿Qué impuestos paga el Whisky?, ¿Arancel de un iPhone?):", value="¿Cuánto de impuesto paga importar 50 Smart TVs y Celulares?")
    
    with col_ia2:
        st.markdown("<br>", unsafe_allow_html=True)
        btn_consultar = st.button("🚀 Consultar con IA", use_container_width=True)

    if consulta_ia or btn_consultar:
        query_norm_ia = normalizar_texto(consulta_ia)
        
        # Búsqueda inteligente de contexto
        matches_ia = [item for item in base_nandina if any(k in query_norm_ia for k in normalizar_texto(item["keywords"]).split()) or normalizar_texto(item["producto"]) in query_norm_ia]
        
        st.markdown("""
        <div class="card-ia">
            <h3>🧠 Respuesta del Asistente IA de Comercio Exterior</h3>
        """, unsafe_allow_html=True)
        
        if "tv" in query_norm_ia or "tele" in query_norm_ia or "televisor" in query_norm_ia:
            st.markdown("""
            * **Producto Detectado:** Televisores y Smart TVs
            * **Partida NANDINA Oficial:** `8528.72.00.00`
            * **Gravamen Arancelario (GA):** **10.0%**
            * **Impuesto al Consumo Específico (ICE):** 0.0%
            * **IVA Importación Efectivo:** **14.94%** sobre base CIF + GA.
            * **Requisitos Aduana Bolivia:** Etiquetado de eficiencia energética / Registro IBNORCA.
            * **💡 Recomendación del Experto (Miguel Macias):** *A diferencia de los celulares (que tienen 0% GA), las pantallas y televisores tributan el 10% de GA. Verifique el flete marítimo consolidado para proteger su margen.*
            """)
        elif "whisky" in query_norm_ia or "licor" in query_norm_ia or "ron" in query_norm_ia or "alcohol" in query_norm_ia or "bebida" in query_norm_ia or "vino" in query_norm_ia or "cerveza" in query_norm_ia:
            st.markdown("""
            * **Producto Detectado:** Bebidas Alcohólicas / Licores
            * **Partida NANDINA Oficial:** `2208.30.00.00` (Whisky) / `2204.21.00.00` (Vinos) / `2203.00.00.00` (Cerveza)
            * **Gravamen Arancelario (GA):** **15.0% - 20.0%**
            * **Impuesto al Consumo Específico (ICE):** **15.0% - 25.0%** (Según grado alcohólico y categoría).
            * **IVA Importación Efectivo:** **14.94%** sobre base CIF + GA + ICE.
            * **Requisitos Aduana Bolivia:** Registro Sanitario SENASAG + Timbre Físico de Control Fiscal Controlado por ANB.
            * **💡 Recomendación del Experto (Miguel Macias):** *Las bebidas alcohólicas están gravadas con el ICE. Asegúrese de tramitar el Registro SENASAG previo al embarque en origen para evitar la retención en aduana interna.*
            """)
        elif "celular" in query_norm_ia or "iphone" in query_norm_ia or "telefono" in query_norm_ia:
            st.markdown("""
            * **Producto Detectado:** Celulares / Smartphones
            * **Partida NANDINA Oficial:** `8517.13.00.00`
            * **Gravamen Arancelario (GA):** **0.0%** (Incentivo Tecnológico en Bolivia)
            * **Impuesto al Consumo Específico (ICE):** 0.0%
            * **IVA Importación Efectivo:** **14.94%** sobre base CIF.
            * **Requisitos Aduana Bolivia:** Homologación de Modelo ante la ATT (Autoridad de Telecomunicaciones).
            * **💡 Recomendación del Experto (Miguel Macias):** *Aproveche el arancel 0% de GA. Solo pagará el IVA de importación (recuperable como crédito fiscal al vender).*
            """)
        else:
            st.markdown(f"""
            * **Análisis de Consulta:** '{consulta_ia}'
            * **Partida NANDINA General Sugerida:** `8471.90.00.00`
            * **GA Estándar Estimado:** **10.0%**
            * **IVA Importación Efectivo:** **14.94%**
            * **Requisitos Aduana Bolivia:** Verificación de Valor y Factura Comercial.
            * **💡 Consejo:** Puede personalizar la tasa exacta de GA en la pestaña **2. Clasificación NANDINA**.
            """)
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PESTAÑA 2: CLASIFICACIÓN ARANCELARIA NANDINA ACCURATE
# -----------------------------------------------------------------------------
with tab_clasif:
    st.subheader("🔎 Clasificador Arancelario NANDINA Bolivia (Catálogo 2026)")
    st.markdown("Seleccione o busque el producto. Cada categoría cuenta con su partida arancelaria de 10 dígitos independiente y diferenciada.")
    
    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        busqueda_prod = st.text_input("🔍 Buscar por producto o partida (ej. televisor, celular, whisky, zapatilla, tractor, cigarrillo):", value="Televisores, Smart TVs y Monitores LED/OLED")
    
    with col_c2:
        cats_unicas = ["Todas"] + sorted(list(set(x["categoria"] for x in base_nandina)))
        cat_filtro = st.selectbox("Filtrar por Categoría:", cats_unicas)
    
    query_norm_clasif = normalizar_texto(busqueda_prod)
    
    # Búsqueda exacta y diferenciada
    coincidencias_exactas = []
    for item in base_nandina:
        if cat_filtro != "Todas" and item["categoria"] != cat_filtro:
            continue
        if query_norm_clasif in normalizar_texto(item["producto"]) or query_norm_clasif in normalizar_texto(item["keywords"]) or query_norm_clasif in normalizar_texto(item["partida"]):
            coincidencias_exactas.append(item)
            
    if coincidencias_exactas:
        item_sel = coincidencias_exactas[0]
    else:
        item_sel = {
            "categoria": "⚙️ Mercancía General",
            "producto": busqueda_prod,
            "partida": "8471.90.00.00",
            "ga": 0.10,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Verificación General Aduanera ANB",
            "descripcion": "Partida asignada para mercancías generales. Puede ajustar la tasa abajo."
        }

    st.markdown("---")
    st.success(f"📌 **Partida Seleccionada:** `{item_sel['partida']}` — **{item_sel['producto']}** ({item_sel['categoria']})")
    
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.markdown(f"""
        **Ficha Técnica Arancelaria:**
        * **Código NANDINA:** `{item_sel['partida']}`
        * **Descripción:** {item_sel['descripcion']}
        * **Permisos / Registros:** {item_sel['certificados']}
        """)
    
    with col_info2:
        ga_sugerido_pct = item_sel['ga'] * 100
        ice_sugerido_pct = item_sel['ice'] * 100
        
        ga_custom = st.number_input("Ajustar Gravamen Arancelario GA (%):", min_value=0.0, max_value=50.0, value=float(ga_sugerido_pct), step=0.5) / 100.0
        ice_custom = st.number_input("Ajustar Impuesto al Consumo Específico ICE (% si aplica):", min_value=0.0, max_value=80.0, value=float(ice_sugerido_pct), step=1.0) / 100.0

# -----------------------------------------------------------------------------
# PESTAÑA 3: PARÁMETROS DE COSTOS&IMPUESTOS
# -----------------------------------------------------------------------------
with tab_costos:
    st.subheader("🚚 Ingreso de Valores de Compra, Fletes e Impuestos")
    
    col_in1, col_in2 = st.columns(2)
    
    with col_in1:
        st.markdown("#### 📦 Valor de Compra en Origen")
        cant_unidades = st.number_input("Cantidad Total de Unidades:", min_value=1, value=100)
        precio_fob_u = st.number_input("Precio FOB Unitario ($USD):", min_value=0.01, value=120.00)
        fob_total_val = cant_unidades * precio_fob_u
        st.info(f"💵 **Valor FOB Total:** `${fob_total_val:,.2f} USD`")
        
        st.markdown("#### 🚢 Fletes y Seguros Internacionales")
        flete_marit_aereo = st.number_input("Flete Internacional Tramo 1 ($USD):", min_value=0.0, value=450.0)
        flete_terrestre_bo = st.number_input("Flete Terrestre Tramo 2 a Bolivia ($USD):", min_value=0.0, value=220.0)
        seguro_carga = st.number_input("Seguro Internacional ($USD):", min_value=0.0, value=50.0)

    with col_in2:
        st.markdown("#### 🛃 Despacho Aduanero y Puerto en Bolivia")
        gastos_aspb_dab = st.number_input("Puerto / Almacenes (ASPB / DAB) ($USD):", min_value=0.0, value=110.0)
        honorarios_agente = st.number_input("Agente Despachante ADA ($USD):", min_value=0.0, value=150.0)
        tramites_cert = st.number_input("Certificados (Senasag, ATT, Timbres) ($USD):", min_value=0.0, value=80.0)
        transporte_local = st.number_input("Flete Local a Almacén Final ($USD):", min_value=0.0, value=60.0)
        
        st.markdown("#### 🏛️ Alícuota IVA Importación")
        aplica_iva_efectivo = st.checkbox("Aplicar Alícuota Efectiva IVA Importación (14.94%)", value=True)
        alicuota_iva = 0.1494 if aplica_iva_efectivo else 0.13

# CÁLCULOS FINANCIEROS MATEMÁTICOS DE LANDED COST
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

# -----------------------------------------------------------------------------
# PESTAÑA 4: DASHBOARD LANDED COST Y GRÁFICOS INTERACTIVOS
# -----------------------------------------------------------------------------
with tab_resumen:
    st.subheader("📊 Dashboard Interactivo de Distribución de Costos")
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Costo Unitario Final (USD)", f"${costo_landed_unit_usd:,.2f}", f"+{((factor_multiplicador - 1)*100):.1f}% vs FOB")
    k2.metric("Costo Unitario Final (BOB)", f"Bs. {costo_landed_unit_bob:,.2f}")
    k3.metric("Costo Total Operación (USD)", f"${costo_landed_total_usd:,.2f}")
    k4.metric("Factor Multiplicador", f"{factor_multiplicador:.3f}x")
    
    st.markdown("---")
    
    # Gráfico Visual Moderno de Torta / Dona (Plotly)
    col_chart1, col_chart2 = st.columns([1, 1])
    
    with col_chart1:
        st.markdown("#### 🥧 Distribución del Costo Landed Total")
        df_pie = pd.DataFrame({
            "Componente": ["FOB Mercancía", "Fletes & Seguro", "Gravamen (GA)", "Impuesto ICE", "IVA Importación", "Gastos Aduaneros"],
            "Monto_USD": [fob_total_val, flete_marit_aereo + flete_terrestre_bo + seguro_carga, monto_ga_calc, monto_ice_calc, monto_iva_calc, total_gastos_operativos]
        })
        fig = px.pie(df_pie, values="Monto_USD", names="Componente", hole=0.45, color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_traces(textinfo="percent+label")
        fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
    with col_chart2:
        st.markdown("#### 📋 Póliza de Importación Desglosada")
        tabla_datos = [
            {"Concepto Operativo": "1. Valor FOB Mercancía", "Monto USD": fob_total_val, "Monto BOB": fob_total_val * tipo_cambio, "% Participación": (fob_total_val / costo_landed_total_usd)*100},
            {"Concepto Operativo": "2. Fletes y Seguro Internacional", "Monto USD": flete_marit_aereo + flete_terrestre_bo + seguro_carga, "Monto BOB": (flete_marit_aereo + flete_terrestre_bo + seguro_carga) * tipo_cambio, "% Participación": ((flete_marit_aereo + flete_terrestre_bo + seguro_carga) / costo_landed_total_usd)*100},
            {"Concepto Operativo": "3. VALOR CIF ADUANA FRONTERA", "Monto USD": cif_frontera, "Monto BOB": cif_frontera * tipo_cambio, "% Participación": (cif_frontera / costo_landed_total_usd)*100},
            {"Concepto Operativo": f"4. Gravamen GA ({ga_custom*100:.1f}%)", "Monto USD": monto_ga_calc, "Monto BOB": monto_ga_calc * tipo_cambio, "% Participación": (monto_ga_calc / costo_landed_total_usd)*100},
            {"Concepto Operativo": f"5. Impuesto ICE ({ice_custom*100:.1f}%)", "Monto USD": monto_ice_calc, "Monto BOB": monto_ice_calc * tipo_cambio, "% Participación": (monto_ice_calc / costo_landed_total_usd)*100},
            {"Concepto Operativo": f"6. IVA Importación ({alicuota_iva*100:.2f}%)", "Monto USD": monto_iva_calc, "Monto BOB": monto_iva_calc * tipo_cambio, "% Participación": (monto_iva_calc / costo_landed_total_usd)*100},
            {"Concepto Operativo": "7. Gastos Puerto, Despachante & Local", "Monto USD": total_gastos_operativos, "Monto BOB": total_gastos_operativos * tipo_cambio, "% Participación": (total_gastos_operativos / costo_landed_total_usd)*100},
            {"Concepto Operativo": "TOTAL COSTO LANDED PUESTO ALMACÉN", "Monto USD": costo_landed_total_usd, "Monto BOB": costo_landed_total_bob, "% Participación": 100.0}
        ]
        df_resumen = pd.DataFrame(tabla_datos)
        st.dataframe(df_resumen.style.format({"Monto USD": "${:,.2f}", "Monto BOB": "Bs. {:,.2f}", "% Participación": "{:.1f}%"}), use_container_width=True)

# -----------------------------------------------------------------------------
# PESTAÑA 5: MARGEN DE GANANCIA&SIMULADOR DE VENTAS
# -----------------------------------------------------------------------------
with tab_ventas:
    st.subheader("💰 Proyección de Ventas y Utilidad Neta Comercial")
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        pvp_unit_bob = st.number_input("Precio de Venta al Público por Unidad (BOB):", min_value=0.0, value=float(round(costo_landed_unit_bob * 1.35, 2)))
        gastos_comerciales_bob = st.number_input("Gastos Comerciales/Marketing por Unidad (BOB):", min_value=0.0, value=20.0)
        
    with col_v2:
        venta_con_factura = st.checkbox("Emitir Factura Comercial en Venta (IVA 13% + IT 3%)", value=True)
        if venta_con_factura:
            debito_iva_u_bob = pvp_unit_bob * 0.13
            it_u_bob = pvp_unit_bob * 0.03
            credito_iva_import_u_bob = (monto_iva_calc * tipo_cambio) / cant_unidades
        else:
            debito_iva_u_bob = 0.0
            it_u_bob = 0.0
            credito_iva_import_u_bob = 0.0

    ingreso_total_bob = pvp_unit_bob * cant_unidades
    costo_landed_mas_gastos_u_bob = costo_landed_unit_bob + gastos_comerciales_bob + debito_iva_u_bob + it_u_bob
    utilidad_neta_u_bob = pvp_unit_bob - costo_landed_mas_gastos_u_bob + credito_iva_import_u_bob
    utilidad_neta_u_usd = utilidad_neta_u_bob / tipo_cambio
    utilidad_neta_total_bob = utilidad_neta_u_bob * cant_unidades
    roi_porcentaje = (utilidad_neta_u_bob / costo_landed_unit_bob) * 100 if costo_landed_unit_bob > 0 else 0.0

    st.markdown("---")
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Ingreso Total Ventas (BOB)", f"Bs. {ingreso_total_bob:,.2f}")
    r2.metric("Ganancia Neta por Unidad", f"Bs. {utilidad_neta_u_bob:,.2f}", f"${utilidad_neta_u_usd:,.2f} USD")
    r3.metric("Ganancia Total del Lote", f"Bs. {utilidad_neta_total_bob:,.2f}")
    r4.metric("Rentabilidad Neta (ROI)", f"{roi_porcentaje:.1f}%")

    if utilidad_neta_u_bob > 0:
        st.success(f"🎉 **Operación Rentable:** Ganancia neta estimada por unidad: **Bs. {utilidad_neta_u_bob:,.2f}** (ROI: **{roi_porcentaje:.1f}%**).")
    else:
        st.error(f"⚠️ **Atención:** El precio de venta seleccionado no cubre los costos. Requiere precio mínimo de **Bs. {costo_landed_mas_gastos_u_bob:,.2f}**.")

# Pie de Página
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem;">
    🚢 <b>Plataforma de Importaciones y Costos Landed Bolivia 2026</b><br>
    Desarrollado por <b>Miguel Macias</b> | Basado en Normativa Aduana Nacional de Bolivia (ANB) y Arancel NANDINA
</div>
""", unsafe_allow_html=True)
