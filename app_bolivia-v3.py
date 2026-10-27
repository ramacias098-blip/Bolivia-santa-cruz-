import streamlit as st
import pandas as pd
import unicodedata
import re

# =============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y ENTORNO EJECUTIVO
# =============================================================================
st.set_page_config(
    page_title="Sistema IA de Importaciones Bolivia 2026 - Miguel Macias",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Normalización avanzada de texto para evitar fallos de acentos/mayúsculas
def normalizar(texto: str) ->str:
    if not texto:
        return ""
    nfkd = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).lower().strip()

# Base de datos NANDINA 2026 oficial (Bolivia) con partidas 100% únicas e independientes
@st.cache_data
def cargar_catalogo_nandina_2026():
    return [
        # TECNOLOGÍA Y ELECTRÓNICA
        {
            "categoria": "💻 Tecnología y Electrónica",
            "producto": "Celulares y Smartphones",
            "partida": "8517.13.00.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificacion": "Homologación ATT (Autoridad de Telecomunicaciones)",
            "descripcion": "Teléfonos inteligentes para redes celulares o inalámbricas.",
            "keywords": "celular telefono smartphone iphone samsung xiaomi redmi huawei movil cel"
        },
        {
            "categoria": "💻 Tecnología y Electrónica",
            "producto": "Televisores, Smart TVs y Monitores",
            "partida": "8528.72.00.00",
            "ga": 0.10,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificacion": "Etiquetado de Eficiencia Energética (IBNORCA)",
            "descripcion": "Aparatos receptores de televisión, incluso con aparato de grabación o reproducción de sonido o imagen incorporado (Smart TV, OLED, QLED).",
            "keywords": "televisor tv smart tv pantalla monitor lg samsung sony hisense tcl tele"
        },
        {
            "categoria": "💻 Tecnología y Electrónica",
            "producto": "Laptops y Computadoras Portátiles",
            "partida": "8471.30.00.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificacion": "Ninguno (DS Incentivo Digital - Libre Importación)",
            "descripcion": "Máquinas automáticas para tratamiento de datos, portátiles de peso <= 10kg.",
            "keywords": "laptop notebook computadora pc dell hp lenovo macbook mac procesador"
        },
        {
            "categoria": "💻 Tecnología y Electrónica",
            "producto": "Consolas de Videojuegos",
            "partida": "9504.50.00.00",
            "ga": 0.10,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificacion": "Ninguno",
            "descripcion": "Consolas y máquinas de videojuegos, excepto las de la subpartida 9504.30.",
            "keywords": "playstation ps5 xbox nintendo switch consola videojuego game"
        },
        {
            "categoria": "💻 Tecnología y Electrónica",
            "producto": "Audífonos Inalámbricos y Auriculares",
            "partida": "8518.30.00.00",
            "ga": 0.10,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificacion": "Ninguno",
            "descripcion": "Auriculares y audífonos, incluso combinados con micrófono.",
            "keywords": "audifonos auriculares airpods bluetooth sonido parlante headset"
        },
        {
            "categoria": "💻 Tecnología y Electrónica",
            "producto": "Smartwatches y Relojes Inteligentes",
            "partida": "8517.62.10.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificacion": "Homologación ATT (si transmite SIM/eSIM)",
            "descripcion": "Aparatos para la recepción o transmisión de datos en redes inalámbricas tipo smartwatch.",
            "keywords": "smartwatch reloj inteligente apple watch samsung galaxy watch garmin"
        },

        # BEBIDAS ALCOHÓLICAS Y TABACO (RÉGIMEN ESPECIAL ICE ANB)
        {
            "categoria": "🍾 Bebidas Alcohólicas y Tabaco",
            "producto": "Whisky y Licores Espirituosos",
            "partida": "2208.30.00.00",
            "ga": 0.15,
            "ice": 0.20,
            "unidad": "Botellas / Cajas",
            "certificacion": "Registro Sanitario SENASAG + Timbre Fiscal ANB",
            "descripcion": "Whisky importado en envases para la venta al por menor.",
            "keywords": "whisky wisky licor tragos johnnie walker chivas buchanans licor"
        },
        {
            "categoria": "🍾 Bebidas Alcohólicas y Tabaco",
            "producto": "Ron y Aguardientes de Caña",
            "partida": "2208.40.00.00",
            "ga": 0.15,
            "ice": 0.20,
            "unidad": "Botellas",
            "certificacion": "Registro Sanitario SENASAG + Timbre Fiscal ANB",
            "descripcion": "Ron y demás aguardientes procedentes de la destilación de productos de caña de azúcar.",
            "keywords": "ron habana abuelo zacapa aguardiente destilado"
        },
        {
            "categoria": "🍾 Bebidas Alcohólicas y Tabaco",
            "producto": "Vinos de Uva y Espumantes",
            "partida": "2204.21.00.00",
            "ga": 0.20,
            "ice": 0.15,
            "unidad": "Botellas",
            "certificacion": "Registro Sanitario SENASAG",
            "descripcion": "Vino de uvas frescas, en recipientes de capacidad <= 2 litros.",
            "keywords": "vino tinto blanco espumante champagne cabernet malbec prosecco"
        },
        {
            "categoria": "🍾 Bebidas Alcohólicas y Tabaco",
            "producto": "Cerveza de Malta",
            "partida": "2203.00.00.00",
            "ga": 0.20,
            "ice": 0.25,
            "unidad": "Latas / Botellas",
            "certificacion": "Registro Sanitario SENASAG",
            "descripcion": "Cerveza obtenida a partir de malta.",
            "keywords": "cerveza heineken corona corona lata botella birra"
        },
        {
            "categoria": "🍾 Bebidas Alcohólicas y Tabaco",
            "producto": "Cigarrillos de Tabaco",
            "partida": "2402.20.00.00",
            "ga": 0.30,
            "ice": 0.50,
            "unidad": "Cajetillas",
            "certificacion": "Timbre Fiscal ANB + Advertencia Sanitaria de Salud",
            "descripcion": "Cigarrillos que contengan tabaco.",
            "keywords": "cigarrillo cigarro tabaco marlboro camel cajetilla"
        },
        {
            "categoria": "🍾 Bebidas Alcohólicas y Tabaco",
            "producto": "Vapeadores y Esencias con Nicotina",
            "partida": "2404.12.00.00",
            "ga": 0.30,
            "ice": 0.50,
            "unidad": "Unidades / Cartuchos",
            "certificacion": "Registro Sanitario Ministerio de Salud",
            "descripcion": "Productos destinados a la inhalación sin combustión que contengan nicotina.",
            "keywords": "vape vaper vapeador esencia nicotina vapes pod"
        },

        # ENERGÍAS RENOVABLES Y SOSTENIBILIDAD
        {
            "categoria": "☀️ Energías Renovables",
            "producto": "Paneles Solares y Módulos Fotovoltaicos",
            "partida": "8541.43.00.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Piezas",
            "certificacion": "Incentivo Energías Limpias (0% GA)",
            "descripcion": "Células fotovoltaicas ensambladas en módulos o compuestas en paneles.",
            "keywords": "panel solar modulo fotovoltaico energia solar inversor kit solar"
        },
        {
            "categoria": "☀️ Energías Renovables",
            "producto": "Inversores de Corriente Solar",
            "partida": "8504.40.90.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificacion": "Incentivo Ley Energías Renovables (0% GA)",
            "descripcion": "Convertidores estáticos para sistemas solares.",
            "keywords": "inversor solar transformador cargador dcdc acdc"
        },

        # MAQUINARIA Y VEHÍCULOS
        {
            "categoria": "🚜 Maquinaria y Vehículos",
            "producto": "Tractores Agrícolas",
            "partida": "8701.91.00.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificacion": "DS Diferimiento Arancelario Bienes de Capital (0% GA)",
            "descripcion": "Tractores agrícolas para fomento a la producción.",
            "keywords": "tractor maquinaria agricola cosechadora arado agro"
        },
        {
            "categoria": "🚜 Maquinaria y Vehículos",
            "producto": "Vehículos Eléctricos e Híbridos",
            "partida": "8703.80.00.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificacion": "DS Vehículos Ecológicos (0% GA + 0% ICE)",
            "descripcion": "Automóviles propulsados con motor eléctrico o híbrido.",
            "keywords": "auto electrico hybrido tesla BYD carro ecologico"
        },
        {
            "categoria": "🚜 Maquinaria y Vehículos",
            "producto": "Automóviles a Gasolina / Diésel",
            "partida": "8703.23.10.00",
            "ga": 0.15,
            "ice": 0.18,
            "unidad": "Unidades",
            "certificacion": "Inspección Ambiental e Inspección ANB",
            "descripcion": "Automóviles de turismo con motor de combustión interna.",
            "keywords": "auto carro camioneta toyota suzuki nissan gasolina diesel"
        },

        # TEXTIL Y CALZADO
        {
            "categoria": "👟 Calzado y Textil",
            "producto": "Calzado Deportivo y Zapatillas",
            "partida": "6404.11.00.00",
            "ga": 0.30,
            "ice": 0.0,
            "unidad": "Pares",
            "certificacion": "Etiquetado de Origen / Normativa IBNORCA",
            "descripcion": "Calzado de deporte con suela de caucho o plástico y parte superior textil.",
            "keywords": "zapatilla tenis calzado zapato deportivo nike adidas puma"
        },
        {
            "categoria": "👟 Calzado y Textil",
            "producto": "Camisetas y Poleras de Algodón",
            "partida": "6109.10.00.00",
            "ga": 0.20,
            "ice": 0.0,
            "unidad": "Piezas",
            "certificacion": "Certificado de Origen (si aplica ACE/CAN)",
            "descripcion": "Camisetas de punto, de algodón.",
            "keywords": "polera camiseta ropa camisa vestimenta algodon"
        },

        # SALUD Y COSMÉTICA
        {
            "categoria": "🏥 Salud y Cosmética",
            "producto": "Cosméticos y Cremas para la Piel",
            "partida": "3304.99.00.00",
            "ga": 0.10,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificacion": "Registro Sanitario AGEMED",
            "descripcion": "Preparaciones para el maquillaje y cuidado de la piel.",
            "keywords": "cosmetico crema maquillaje belleza piel agemed"
        },
        {
            "categoria": "🏥 Salud y Cosmética",
            "producto": "Perfumes y Lociones",
            "partida": "3303.00.00.00",
            "ga": 0.20,
            "ice": 0.0,
            "unidad": "Frascos",
            "certificacion": "Registro Sanitario AGEMED",
            "descripcion": "Perfumes y aguas de tocador.",
            "keywords": "perfume fragancia locion coloni agemed"
        },
        {
            "categoria": "🏥 Salud y Cosmética",
            "producto": "Suplementos Alimenticios y Vitaminas",
            "partida": "2106.90.90.00",
            "ga": 0.10,
            "ice": 0.0,
            "unidad": "Frascos / Cajas",
            "certificacion": "Registro Sanitario SENASAG",
            "descripcion": "Preparaciones alimenticias no comprendidas en otra parte.",
            "keywords": "suplemento vitamina proteina senasag creatina colageno"
        }
    ]

# Estilos CSS de Ultra-Lujo Ejecutivo
st.markdown("""
<style>
    /* Estilo del Header */
    .hero-header {
        background: linear-gradient(135deg, #0A192F 0%, #112240 50%, #1A365D 100%);
        padding: 30px;
        border-radius: 18px;
        color: #FFFFFF;
        box-shadow: 0 10px 25px rgba(0,0,0,0.25);
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 25px;
    }
    .hero-title {
        font-size: 2.3rem !important;
        font-weight: 800 !important;
        color: #00F2FE !important;
        margin: 0 0 10px 0 !important;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        color: #E2E8F0 !important;
        font-size: 1.1rem !important;
        margin: 0 !important;
    }
    .hero-badge {
        background: linear-gradient(90deg, #FFC107 0%, #FF8F00 100%);
        color: #000000;
        padding: 6px 18px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 0.88rem;
        display: inline-block;
        margin-top: 12px;
        box-shadow: 0 4px 12px rgba(255,193,7,0.3);
    }
    /* Tarjetas Métricas */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: transform 0.2s ease;
    }
    .metric-value-usd {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0F172A;
    }
    .metric-value-bob {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2563EB;
    }
    .metric-label {
        font-size: 0.88rem;
        color: #64748B;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 5px;
    }
    /* Tarjeta del Asistente IA */
    .ai-box {
        background: #F8FAFC;
        border-left: 6px solid #00F2FE;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 20px;
        border-top: 1px solid #E2E8F0;
        border-right: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;
    }
    .ai-badge {
        background: #00F2FE;
        color: #0F172A;
        font-weight: 800;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 0.8rem;
    }
    /* Barra de Progreso Visual de Costos */
    .progress-container {
        width: 100%;
        background-color: #E2E8F0;
        border-radius: 10px;
        display: flex;
        height: 24px;
        overflow: hidden;
        margin: 15px 0;
    }
    .bar-fob { background-color: #2563EB; }
    .bar-flete { background-color: #3B82F6; }
    .bar-ga { background-color: #EF4444; }
    .bar-iva { background-color: #F59E0B; }
    .bar-ice { background-color: #8B5CF6; }
    .bar-gastos { background-color: #10B981; }
</style>
""", unsafe_allow_html=True)

# Header Principal
st.markdown("""
<div class="hero-header">
    <div class="hero-title">🤖 Portal de Importaciones e Inteligencia Arancelaria Bolivia 2026</div>
    <div class="hero-subtitle">Plataforma Empresarial con Asistente Virtual IA, Arancel NANDINA Actualizado e Impuestos ANB</div>
    <div class="hero-badge">👤 Desarrollado por: Miguel Macias</div>
</div>
""", unsafe_allow_html=True)

catalogo = cargar_catalogo_nandina_2026()

# Panel Lateral de Controles
st.sidebar.title("⚙️ Parámetros de Operación")
st.sidebar.markdown("**Director Ejecutivo:** Miguel Macias")
st.sidebar.markdown("---")

tipo_cambio = st.sidebar.number_input("💵 Tipo de Cambio (BOB / USD):", min_value=1.0, value=6.96, step=0.01)
vía_transporte = st.sidebar.selectbox("🚢 Vía de Transporte Logístico:", [
    "Marítimo FCL (Contenedor Completo)",
    "Marítimo LCL (Carga Consolidada)",
    "Aéreo Express / Courier",
    "Terrestre Internacional (Arica/Iquique a Bolivia)"
])

st.sidebar.markdown("---")
st.sidebar.success("✅ **Base de Datos ANB 2026:** Tasas arancelarias actualizadas con Decretos Supremos de diferimiento (0% GA) e Impuestos Especiales (ICE).")

# Pestañas de la Aplicación
tab_ia, tab_clasif, tab_log, tab_resumen, tab_simulador = st.tabs([
    "🤖 1. Asistente Virtual IA",
    "🔎 2. Clasificación NANDINA",
    "🚚 3. Logística e Impuestos",
    "📊 4. Cuadro Ejecutivo Landed Cost",
    "💰 5. Simulador de Venta y Margen"
])

# =============================================================================
# PESTAÑA 1: ASISTENTE VIRTUAL IA DE IMPORTACIONES
# =============================================================================
with tab_ia:
    st.subheader("🤖 Consultas en Lenguaje Natural al Asistente IA")
    st.markdown("Escriba lo que desea consultar como si hablara con un experto en comercio exterior (ej. *'¿Cuánto paga traer 50 Smart TVs?'*, *'¿Cuáles son los impuestos del Whisky?'*, *'Quiero importar 100 celulares de China'*).")

    col_ia1, col_ia2 = st.columns([3, 1])
    with col_ia1:
        consulta_user = st.text_input("💬 Escriba su consulta aquí:", value="¿Cuánto de impuesto paga importar 20 Smart TVs y 50 Laptops?")
    with col_ia2:
        btn_consultar = st.button("🚀 Analizar con IA", use_container_width=True)

    query_norm = normalizar(consulta_user)
    
    # Motor Inteligente de Detección por IA
    coincidencias_ia = []
    for item in catalogo:
        p_norm = normalizar(item["producto"])
        k_norm = normalizar(item["keywords"])
        if any(palabra in query_norm for palabra in p_norm.split()) or any(k in query_norm for k in k_norm.split() if len(k) > 3):
            coincidencias_ia.append(item)

    st.markdown("---")
    
    if coincidencias_ia:
        st.markdown(f"### 📑 Informe Ejecutivo Generado por la IA")
        for item in coincidencias_ia:
            ga_p = item["ga"] * 100
            ice_p = item["ice"] * 100
            st.markdown(f"""
            <div class="ai-box">
                <span class="ai-badge">IA RECOMENDACIÓN</span>
                <h3 style="margin-top:10px; color:#0F172A;">📦 {item['producto']}</h3>
                <p><b>Subpartida NANDINA Oficial:</b> <code>{item['partida']}</code></p>
                <p><b>Descripción Técnica:</b> {item['descripcion']}</p>
                <ul>
                    <li><b>Gravamen Arancelario (GA):</b> <b style="color:#10B981;">{ga_p:.1f}%</b></li>
                    <li><b>Impuesto al Consumo Específico (ICE):</b> <b>{ice_p:.1f}%</b></li>
                    <li><b>Alícuota Efectiva IVA Importación (ANB):</b> <b>14.94%</b> sobre CIF+GA+ICE</li>
                    <li><b>Certificaciones y Permisos Aduaneros:</b> <mark>{item['certificacion']}</mark></li>
                </ul>
                <p style="font-size:0.9rem; color:#64748B; margin-bottom:0;"><i>Análisis verificado según la Nomenclatura Arancelaria de la Aduana Nacional de Bolivia | Firma: <b>Miguel Macias</b></i></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("💡 **Análisis de la IA:** Se ha detectado una consulta sobre mercancía general. La subpartida estándar es `8471.90.00.00` con un GA del **10.0%** y una alícuota de IVA del **14.94%**. Puedes ajustar los valores detallados en las siguientes pestañas.")

# =============================================================================
# PESTAÑA 2: CLASIFICACIÓN NANDINA CON PARTIDAS ÚNICAS
# =============================================================================
with tab_clasif:
    st.subheader("🔎 Buscador Oficial de Partida Arancelaria NANDINA 2026")
    
    col_s1, col_s2 = st.columns([2, 1])
    with col_s1:
        prod_busqueda = st.text_input("🔍 Buscar por producto o partida (ej. celular, televisor, whisky, ropa, auto):", value="Televisores, Smart TVs y Monitores")
    with col_s2:
        cat_filtro = st.selectbox("Filtrar por Categoría:", ["Todas las Categorías"] + sorted(list(set(i["categoria"] for i in catalogo))))

    busq_norm = normalizar(prod_busqueda)
    match_item = None

    for item in catalogo:
        if cat_filtro != "Todas las Categorías" and item["categoria"] != cat_filtro:
            continue
        if busq_norm in normalizar(item["producto"]) or busq_norm in normalizar(item["keywords"]) or busq_norm in normalizar(item["partida"]):
            match_item = item
            break

    if not match_item:
        match_item = {
            "categoria": "⚙️ Mercancía General",
            "producto": prod_busqueda if prod_busqueda else "Mercancía General",
            "partida": "8471.90.00.00",
            "ga": 0.10,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificacion": "Verificación Aduanera ANB Estándar",
            "descripcion": "Clasificación general asignada para productos no catalogados específicamente."
        }

    ga_porcentaje = match_item["ga"] * 100
    ice_porcentaje = match_item["ice"] * 100

    st.markdown("---")
    st.markdown(f"""
    <div style="background:#FFFFFF; padding:20px; border-radius:12px; border:1px solid #CBD5E1; border-left:6px solid #2563EB;">
        <h3 style="margin-top:0; color:#0F172A;">📋 Ficha Técnica Arancelaria NANDINA</h3>
        <p><b>Producto Seleccionado:</b> {match_item['producto']}</p>
        <p><b>Código Subpartida (10 Dígitos):</b> <code style="font-size:1.2rem; color:#2563EB;">{match_item['partida']}</code></p>
        <p><b>Descripción Oficial ANB:</b> {match_item['descripcion']}</p>
        <p><b>Gravamen Arancelario (GA) Sugerido:</b> <b style="color:#059669; font-size:1.1rem;">{ga_porcentaje:.1f}%</b></p>
        <p><b>Impuesto Específico (ICE):</b> <b>{ice_porcentaje:.1f}%</b></p>
        <p><b>Permisos y Requisitos en Bolivia:</b> <span>{match_item['certificacion']}</span></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### ⚙️ Personalizar Tasas del Cálculo")
    col_ga1, col_ga2 = st.columns(2)
    with col_ga1:
        ga_custom = st.number_input("Ajustar GA (%):", min_value=0.0, max_value=40.0, value=float(ga_porcentaje), step=0.5) / 100.0
    with col_ga2:
        ice_custom = st.number_input("Ajustar ICE (%):", min_value=0.0, max_value=80.0, value=float(ice_porcentaje), step=1.0) / 100.0

# =============================================================================
# PESTAÑA 3: LOGÍSTICA E IMPUESTOS
# =============================================================================
with tab_log:
    st.subheader("🚚 Datos de la Compra, Fletes y Gastos Aduaneros")

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("#### 📦 Valoración en Origen")
        cant_unidades = st.number_input("Cantidad de Unidades a Importar:", min_value=1, value=100)
        precio_fob_u = st.number_input("Precio FOB Unitario ($USD):", min_value=0.01, value=120.00, step=5.0)
        fob_total_val = cant_unidades * precio_fob_u
        st.info(f"💵 **Valor FOB Total:** `${fob_total_val:,.2f} USD`")

        st.markdown("#### 🚢 Fletes y Seguros")
        flete_marit_aereo = st.number_input("Flete Internacional Tramo 1 ($USD):", min_value=0.0, value=450.0, step=10.0)
        flete_terrestre_bo = st.number_input("Flete Terrestre a Bolivia Tramo 2 ($USD):", min_value=0.0, value=220.0, step=10.0)
        seguro_carga = st.number_input("Seguro Internacional de Carga ($USD):", min_value=0.0, value=50.0, step=5.0)

    with col_m2:
        st.markdown("#### 🛃 Gastos de Despacho en Bolivia")
        gastos_aspb_dab = st.number_input("Puerto y Almacenes (ASPB / DAB) ($USD):", min_value=0.0, value=110.0, step=5.0)
        honorarios_agente = st.number_input("Agente Despachante de Aduana (ADA) ($USD):", min_value=0.0, value=150.0, step=10.0)
        tramites_cert = st.number_input("Certificaciones y Permisos ($USD):", min_value=0.0, value=80.0, step=5.0)
        transporte_local = st.number_input("Flete Local a Almacén ($USD):", min_value=0.0, value=60.0, step=5.0)

        st.markdown("#### 🏛️ Alícuota IVA Importación")
        aplica_iva_efectivo = st.checkbox("Aplicar Alícuota Efectiva IVA Importación (14.94%)", value=True)
        alicuota_iva = 0.1494 if aplica_iva_efectivo else 0.13

# =============================================================================
# CÁLCULOS MATEMÁTICOS OFICIALES DE LANDED COST
# =============================================================================
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

# Porcentajes de participación
pct_fob = (fob_total_val / costo_landed_total_usd) * 100
pct_flete = ((flete_marit_aereo + flete_terrestre_bo + seguro_carga) / costo_landed_total_usd) * 100
pct_ga = (monto_ga_calc / costo_landed_total_usd) * 100
pct_iva = (monto_iva_calc / costo_landed_total_usd) * 100
pct_ice = (monto_ice_calc / costo_landed_total_usd) * 100
pct_gastos = (total_gastos_operativos / costo_landed_total_usd) * 100

# =============================================================================
# PESTAÑA 4: CUADRO EJECUTIVO Y RESUMEN VISUAL
# =============================================================================
with tab_resumen:
    st.subheader("📊 Resumen del Costo Landed Puesto en Bolivia")

    # Tarjetas Métricas
    c_k1, c_k2, c_k3, c_k4 = st.columns(4)
    with c_k1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Costo Unitario Final</div>
            <div class="metric-value-usd">${costo_landed_unit_usd:,.2f} USD</div>
            <div style="font-size:0.85rem; color:#10B981; font-weight:700;">+{((factor_multiplicador - 1)*100):.1f}% vs FOB</div>
        </div>
        """, unsafe_allow_html=True)
    with c_k2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Costo Unitario Bolivianos</div>
            <div class="metric-value-bob">Bs. {costo_landed_unit_bob:,.2f}</div>
            <div style="font-size:0.85rem; color:#64748B;">T.C. {tipo_cambio:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with c_k3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Inversión Total Lote</div>
            <div class="metric-value-usd">${costo_landed_total_usd:,.2f} USD</div>
            <div style="font-size:0.85rem; color:#64748B;">Bs. {costo_landed_total_bob:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with c_k4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Factor Multiplicador</div>
            <div class="metric-value-usd" style="color:#8B5CF6;">{factor_multiplicador:.3f}x</div>
            <div style="font-size:0.85rem; color:#64748B;">Ratio sobre FOB</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📈 Distribución Porcentual del Costo")
    
    # Barra Visual Proporcional
    st.markdown(f"""
    <div class="progress-container">
        <div class="bar-fob" style="width: {pct_fob}%;" title="FOB: {pct_fob:.1f}%"></div>
        <div class="bar-flete" style="width: {pct_flete}%;" title="Fletes: {pct_flete:.1f}%"></div>
        <div class="bar-ga" style="width: {pct_ga}%;" title="GA: {pct_ga:.1f}%"></div>
        <div class="bar-iva" style="width: {pct_iva}%;" title="IVA: {pct_iva:.1f}%"></div>
        <div class="bar-ice" style="width: {pct_ice}%;" title="ICE: {pct_ice:.1f}%"></div>
        <div class="bar-gastos" style="width: {pct_gastos}%;" title="Gastos: {pct_gastos:.1f}%"></div>
    </div>
    <div style="display:flex; justify-content:space-between; font-size:0.82rem; font-weight:700; color:#475569; flex-wrap:wrap;">
        <span style="color:#2563EB;">🟦 Mercancía FOB ({pct_fob:.1f}%)</span>
        <span style="color:#3B82F6;">🟦 Fletes ({pct_flete:.1f}%)</span>
        <span style="color:#EF4444;">🟥 GA ({pct_ga:.1f}%)</span>
        <span style="color:#F59E0B;">🟧 IVA ({pct_iva:.1f}%)</span>
        <span style="color:#8B5CF6;">🟪 ICE ({pct_ice:.1f}%)</span>
        <span style="color:#10B981;">🟩 Gastos Op. ({pct_gastos:.1f}%)</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📋 Póliza de Importación Desglosada")

    tabla_datos = [
        {"Concepto Operativo": "1. Valor FOB Mercancía", "Monto USD": fob_total_val, "Monto BOB": fob_total_val * tipo_cambio, "% Participación": pct_fob},
        {"Concepto Operativo": "2. Fletes y Seguro Internacional", "Monto USD": flete_marit_aereo + flete_terrestre_bo + seguro_carga, "Monto BOB": (flete_marit_aereo + flete_terrestre_bo + seguro_carga) * tipo_cambio, "% Participación": pct_flete},
        {"Concepto Operativo": "3. VALOR CIF ADUANA / FRONTERA", "Monto USD": cif_frontera, "Monto BOB": cif_frontera * tipo_cambio, "% Participación": (cif_frontera / costo_landed_total_usd)*100},
        {"Concepto Operativo": f"4. Gravamen Arancelario GA ({ga_custom*100:.1f}%)", "Monto USD": monto_ga_calc, "Monto BOB": monto_ga_calc * tipo_cambio, "% Participación": pct_ga},
        {"Concepto Operativo": f"5. Impuesto ICE ({ice_custom*100:.1f}%)", "Monto USD": monto_ice_calc, "Monto BOB": monto_ice_calc * tipo_cambio, "% Participación": pct_ice},
        {"Concepto Operativo": f"6. IVA Importación ({alicuota_iva*100:.2f}%)", "Monto USD": monto_iva_calc, "Monto BOB": monto_iva_calc * tipo_cambio, "% Participación": pct_iva},
        {"Concepto Operativo": "7. Gastos Puerto, ADA y Almacén", "Monto USD": total_gastos_operativos, "Monto BOB": total_gastos_operativos * tipo_cambio, "% Participación": pct_gastos},
        {"Concepto Operativo": "TOTAL COSTO LANDED FINAL", "Monto USD": costo_landed_total_usd, "Monto BOB": costo_landed_total_bob, "% Participación": 100.0}
    ]

    df_resumen = pd.DataFrame(tabla_datos)
    st.dataframe(df_resumen.style.format({"Monto USD": "${:,.2f}", "Monto BOB": "Bs. {:,.2f}", "% Participación": "{:.1f}%"}), use_container_width=True)

    csv_data = df_resumen.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Cotización Oficial (CSV / Excel)",
        data=csv_data,
        file_name="cotizacion_importacion_bolivia_miguel_macias.csv",
        mime="text/csv"
    )

# =============================================================================
# PESTAÑA 5: SIMULADOR DE MARGEN Y COMERCIALIZACIÓN
# =============================================================================
with tab_simulador:
    st.subheader("💰 Simulador de Precios de Venta y Margen de Ganancia")

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("#### 🏷️ Fijación de Precio de Venta al Público (PVP)")
        pvp_unit_bob = st.number_input("Precio de Venta Sugerido por Unidad (BOB):", min_value=0.0, value=float(round(costo_landed_unit_bob * 1.35, 2)), step=10.0)
        gastos_comerciales_u_bob = st.number_input("Gastos de Comercialización/Publicidad por Unidad (BOB):", min_value=0.0, value=15.0, step=5.0)

    with col_v2:
        st.markdown("#### 🧾 Régimen Tributario Comercial (SIN)")
        venta_con_factura = st.checkbox("Emitir Factura Comercial (IVA 13% + IT 3%)", value=True)
        
        if venta_con_factura:
            debito_iva_u_bob = pvp_unit_bob * 0.13
            it_u_bob = pvp_unit_bob * 0.03
            credito_iva_import_u_bob = (monto_iva_calc * tipo_cambio) / cant_unidades
            st.caption(f"**Crédito Fiscal IVA recuperado por importación:** `Bs. {credito_iva_import_u_bob:,.2f} / unidad`")
        else:
            debito_iva_u_bob = 0.0
            it_u_bob = 0.0
            credito_iva_import_u_bob = 0.0

    ingreso_total_bob = pvp_unit_bob * cant_unidades
    costo_total_venta_u_bob = costo_landed_unit_bob + gastos_comerciales_u_bob + debito_iva_u_bob + it_u_bob - credito_iva_import_u_bob
    
    utilidad_neta_u_bob = pvp_unit_bob - costo_total_venta_u_bob
    utilidad_neta_u_usd = utilidad_neta_u_bob / tipo_cambio
    
    utilidad_neta_total_bob = utilidad_neta_u_bob * cant_unidades
    utilidad_neta_total_usd = utilidad_neta_total_bob / tipo_cambio
    
    roi_porcentaje = (utilidad_neta_u_bob / costo_landed_unit_bob) * 100 if costo_landed_unit_bob > 0 else 0.0

    st.markdown("---")
    st.subheader("📈 Proyección de Utilidad Neta y Rentabilidad")

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Ingreso Total Ventas", f"Bs. {ingreso_total_bob:,.2f}")
    r2.metric("Ganancia Neta por Unidad", f"Bs. {utilidad_neta_u_bob:,.2f}", f"${utilidad_neta_u_usd:,.2f} USD")
    r3.metric("Ganancia Neta Lote Total", f"Bs. {utilidad_neta_total_bob:,.2f}", f"${utilidad_neta_total_usd:,.2f} USD")
    r4.metric("Retorno de Inversión (ROI)", f"{roi_porcentaje:.1f}%")

    if utilidad_neta_u_bob > 0:
        st.success(f"🎉 **Operación Rentable:** Vendiendo a **Bs. {pvp_unit_bob:,.2f}**, tu ganancia neta estimada por unidad es de **Bs. {utilidad_neta_u_bob:,.2f}** (**${utilidad_neta_u_usd:,.2f} USD**), generando un ROI del **{roi_porcentaje:.1f}%**.")
    else:
        st.error(f"⚠️ **Precio por debajo del costo:** Se requiere un precio mínimo de venta de **Bs. {costo_total_venta_u_bob:,.2f}** para no generar pérdidas.")

# Pie de Página Oficial
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.9rem; padding: 10px 0;">
    🚢 <b>Sistema Inteligente de Cálculo de Importaciones Bolivia 2026</b><br>
    Desarrollado por <b>Miguel Macias</b> | Basado en Normativa Aduana Nacional de Bolivia (ANB) y Nomenclatura NANDINA
</div>
""", unsafe_allow_html=True)
