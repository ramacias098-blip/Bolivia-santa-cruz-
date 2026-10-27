import streamlit as st
import pandas as pd
import unicodedata

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y RENDIMIENTO
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Calculadora de Importaciones Bolivia 2026 - Miguel Macias",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Optimización: Función de normalización de cadenas para búsquedas ultra-rápidas y sin fallos
def normalizar_texto(texto: str) ->str:
    if not texto:
        return ""
    # Quitar acentos y convertir a minúsculas
    nfkd = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).lower().strip()

# Optimización con Cache para multiusuarios (evita consumo excesivo de memoria)
@st.cache_data
def obtener_base_datos_nandina_2026():
    return [
        # TECNOLOGÍA Y COMPUTACIÓN
        {
            "categoria": "💻 Tecnología y Electrónica",
            "producto": "Laptops y Computadoras Portátiles",
            "partida": "8471.30.00.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Ninguno (Libre Importación - DS Incentivo Digital)",
            "descripcion": "Máquinas automáticas para tratamiento de datos, portátiles de peso <= 10kg.",
            "keywords": "laptop notebook computadora pc laptop dell hp lenovo macbook mac procesador"
        },
        {
            "categoria": "💻 Tecnología y Electrónica",
            "producto": "Celulares y Teléfonos Inteligentes (Smartphones)",
            "partida": "8517.13.00.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Homologación ATT (Autoridad de Telecomunicaciones)",
            "descripcion": "Teléfonos inteligentes para redes celulares o inalámbricas.",
            "keywords": "celular telefono smartphone iphone samsung xiaomi redmi huawei movil"
        },
        {
            "categoria": "💻 Tecnología y Electrónica",
            "producto": "Servidores y Equipos de Red (Routers, Switches)",
            "partida": "8517.62.90.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Homologación ATT (si transmite radiofrecuencia)",
            "descripcion": "Aparatos para la recepción, conversión y transmisión o regeneración de voz, imagen u otros datos.",
            "keywords": "servidor router switch red mikrotik cisco wifi modem fibra optica"
        },
        {
            "categoria": "💻 Tecnología y Electrónica",
            "producto": "Tablets e Ilustradoras Digitales",
            "partida": "8471.30.00.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Ninguno",
            "descripcion": "Dispositivos portátiles táctiles de procesamiento de datos.",
            "keywords": "tablet ipad samsung tab huion wacom pantalla tactil"
        },
        {
            "categoria": "💻 Tecnología y Electrónica",
            "producto": "Impresoras y Escáneres Multifuncionales",
            "partida": "8443.31.00.00",
            "ga": 0.05,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Ninguno",
            "descripcion": "Máquinas que efectúen dos o más funciones: impresión, copia o transmisión facsimilar.",
            "keywords": "impresora epson canon hp fotocopiadora escaner toner multifuncional"
        },

        # ENERGÍA Y SOSTENIBILIDAD
        {
            "categoria": "☀️ Energías Renovables",
            "producto": "Paneles Solares y Módulos Fotovoltaicos",
            "partida": "8541.43.00.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Piezas",
            "certificados": "Incentivo Energías Limpias (Arancel 0%)",
            "descripcion": "Células fotovoltaicas ensambladas en módulos o compuestas en paneles.",
            "keywords": "panel solar modulo fotovoltaico energia solar inversor paneles solares kit solar"
        },
        {
            "categoria": "☀️ Energías Renovables",
            "producto": "Inversores de Corriente Solar",
            "partida": "8504.40.90.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Incentivo Ley de Energías Renovables",
            "descripcion": "Convertidores estáticos de energía para sistemas solares.",
            "keywords": "inversor cargador regulador solar transformador dcdc acdc"
        },
        {
            "categoria": "☀️ Energías Renovables",
            "producto": "Baterías de Litio para Almacenamiento Solar",
            "partida": "8507.60.00.00",
            "ga": 0.05,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Verificación de Seguridad Eléctrica",
            "descripcion": "Acumuladores eléctricos de ión de litio.",
            "keywords": "bateria litio lifepo4 almacenamiento acumulador banco baterias"
        },

        # MAQUINARIA E INDUSTRIA (BIENES DE CAPITAL)
        {
            "categoria": "🏗️ Maquinaria e Industria",
            "producto": "Maquinaria Agrícola (Tractores, Cosechadoras)",
            "partida": "8701.91.00.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "DS Diferimiento Arancelario Bienes de Capital (0%)",
            "descripcion": "Tractores agrícolas e industriales para fomento de la producción nacional.",
            "keywords": "tractor cosechadora sembradora arado maquinaria agricola maiz soya agro"
        },
        {
            "categoria": "🏗️ Maquinaria e Industria",
            "producto": "Excavadoras y Maquinaria Pesada de Construcción",
            "partida": "8429.52.00.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "DS Incentivo Bienes de Capital",
            "descripcion": "Máquinas cuya superestructura pueda girar 360 grados, de oruga o ruedas.",
            "keywords": "excavadora retroexcavadora oruga pala cargadora maquinaria pesada cat caterpillar komatsu"
        },
        {
            "categoria": "🏗️ Maquinaria e Industria",
            "producto": "Generadores Eléctricos / Grupos Electrógenos",
            "partida": "8502.11.00.00",
            "ga": 0.05,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Ninguno",
            "descripcion": "Grupos electrógenos con motor de émbolo de encendido por compresión (diésel).",
            "keywords": "generador grupo electrogeno motor diesel luz corriente planta electrica cummins"
        },
        {
            "categoria": "🏗️ Maquinaria e Industria",
            "producto": "Bombas de Agua e Hidráulicas Industriales",
            "partida": "8413.70.00.00",
            "ga": 0.05,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Ninguno",
            "descripcion": "Bombas centrífugas para líquidos.",
            "keywords": "bomba agua hidraulica pozo riego turbina motorbomba"
        },

        # VEHÍCULOS Y REPUESTOS
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
            "producto": "Automóviles de Pasajeros (Gasolina/Diésel)",
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
        {
            "categoria": "🚗 Vehículos y Repuestos",
            "producto": "Neumáticos y Llantas para Vehículos",
            "partida": "4011.10.00.00",
            "ga": 0.15,
            "ice": 0.0,
            "unidad": "Piezas",
            "certificados": "Ninguno",
            "descripcion": "Neumáticos nuevos de caucho del tipo utilizado en automóviles de turismo.",
            "keywords": "neumatico llanta rueda caucho goma auto camioneta"
        },

        # SALUD Y MEDICINA
        {
            "categoria": "🏥 Salud y Medicina",
            "producto": "Equipos Médicos y de Diagnóstico",
            "partida": "9018.90.90.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Autorización Sanitaria AGEMED / Ministerio de Salud",
            "descripcion": "Instrumentos y aparatos de medicina, cirugía, odontología o veterinaria.",
            "keywords": "equipo medico ecografo rayos x estetoscopio monitor hospital agemed"
        },
        {
            "categoria": "🏥 Salud y Medicina",
            "producto": "Medicamentos y Fármacos de Uso Humano",
            "partida": "3004.90.20.00",
            "ga": 0.05,
            "ice": 0.0,
            "unidad": "Cajas / Frascos",
            "certificados": "Registro Sanitario AGEMED (Obligatorio)",
            "descripcion": "Medicamentos constituidos por productos mezclados o sin mezclar preparados para usos terapéuticos.",
            "keywords": "medicamento farmaco medicina pastilla jarabe remedio salud agemed"
        },

        # AGRO E INSUMOS
        {
            "categoria": "🌱 Agro e Insumos",
            "producto": "Fertilizantes e Insumos Agrícolas",
            "partida": "3105.20.00.00",
            "ga": 0.0,
            "ice": 0.0,
            "unidad": "Bolsas / Toneladas",
            "certificados": "Registro Sanitario SENASAG",
            "descripcion": "Abonos minerales o químicos con nitrógeno, fósforo y potasio.",
            "keywords": "fertilizante abono urea npk senasag agro quimico veneno plantas"
        },

        # TEXTIL, CALZADO Y HOGAR
        {
            "categoria": "👟 Calzado y Textil",
            "producto": "Calzado Deportivo y Zapatillas",
            "partida": "6404.11.00.00",
            "ga": 0.30,
            "ice": 0.0,
            "unidad": "Pares",
            "certificados": "Etiquetado de Origen / Normativa IBNORCA",
            "descripcion": "Calzado de deporte con suela de caucho o plástico y parte superior de materia textil.",
            "keywords": "zapatilla tenis calzado zapato deportivo nike adidas puma"
        },
        {
            "categoria": "👟 Calzado y Textil",
            "producto": "Prendas de Vestir / Camisetas de Algodón",
            "partida": "6109.10.00.00",
            "ga": 0.20,
            "ice": 0.0,
            "unidad": "Piezas",
            "certificados": "Certificado de Origen (si aplica tratado comercial)",
            "descripcion": "Camisetas de punto, de algodón para hombres, mujeres o niños.",
            "keywords": "ropa camiseta polera poleron camisa pantalon tela vestimenta"
        },
        {
            "categoria": "🪑 Muebles y Hogar",
            "producto": "Sillas de Oficina y Muebles Ergonomicos",
            "partida": "9401.30.00.00",
            "ga": 0.15,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Ninguno",
            "descripcion": "Asientos giratorios ajustables en altura para oficina o el hogar.",
            "keywords": "silla mueble escritorio oficina sillón gamer ergonómica"
        },

        # COSMÉTICOS Y ALIMENTOS
        {
            "categoria": "💄 Cosméticos y Belleza",
            "producto": "Cosméticos y Cremas de Cuidado Personal",
            "partida": "3304.99.00.00",
            "ga": 0.10,
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Registro Sanitario AGEMED",
            "descripcion": "Preparaciones para el maquillaje, belleza y cuidado de la piel.",
            "keywords": "cosmetico crema maquillaje perfume piel belleza agemed"
        },
        {
            "categoria": "🍎 Alimentos y Suplementos",
            "producto": "Suplementos Alimenticios y Vitaminas",
            "partida": "2106.90.90.00",
            "ga": 0.10,
            "ice": 0.0,
            "unidad": "Frascos / Cajas",
            "certificados": "Registro Sanitario SENASAG",
            "descripcion": "Preparaciones alimenticias no expresadas ni comprendidas en otra parte.",
            "keywords": "suplemento vitamina proteina senasag nutricion creatina colageno"
        }
    ]

# -----------------------------------------------------------------------------
# 2. ESTILOS CSS MODERNOS Y COMPATIBLES
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Estilos del contenedor de encabezado */
    .main-header {
        background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
        padding: 28px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        border: 1px solid rgba(255,255,255,0.1);
    }
    .main-header h1 {
        color: #ffffff !important;
        font-size: 2.3rem !important;
        font-weight: 800 !important;
        margin: 0 0 8px 0 !important;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #e0e6ed !important;
        font-size: 1.1rem !important;
        margin: 0 !important;
    }
    .badge-miguel {
        background-color: #ffc107;
        color: #111111;
        padding: 6px 16px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-block;
        margin-top: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .card-info {
        background-color: #ffffff;
        border: 1px solid #e1e8ed;
        border-left: 6px solid #2C5364;
        padding: 18px;
        border-radius: 10px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .card-info h4 {
        margin-top: 0;
        color: #1e293b;
    }
    .card-info ul {
        margin-bottom: 0;
        padding-left: 20px;
    }
    .status-badge-green {
        background-color: #d1fae5;
        color: #065f46;
        padding: 3px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. ENCABEZADO PRINCIPAL DE LA PLATAFORMA
# -----------------------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>🚢 📦 🛃 Portal de Importaciones y Landed Cost Bolivia 2026</h1>
    <p>Sistema Inteligente de Clasificación Arancelaria NANDINA, Costos Logísticos e Impuestos Aduaneros (ANB)</p>
    <div class="badge-miguel">👤 Desarrollado por: Miguel Macias</div>
</div>
""", unsafe_allow_html=True)

# Cargar base de datos optimizada
base_nandina = obtener_base_datos_nandina_2026()

# -----------------------------------------------------------------------------
# 4. BARRA LATERAL (CONFIGURACIÓN MONETARIA Y LOGÍSTICA)
# -----------------------------------------------------------------------------
st.sidebar.title("🛠️ Configuración General")
st.sidebar.markdown("**Autor:** Miguel Macias")
st.sidebar.markdown("---")

tipo_cambio = st.sidebar.number_input("💵 Tipo de Cambio Oficial (BOB / USD):", min_value=1.0, value=6.96, step=0.01)
modalidad_transporte = st.sidebar.selectbox("🚢 Vía de Transporte:", [
    "Marítimo FCL (Contenedor Completo)",
    "Marítimo LCL (Carga Consolidada)",
    "Aéreo Express / Courier",
    "Terrestre Internacional"
])

st.sidebar.markdown("---")
st.sidebar.success("✅ **Actualización 2026 Activa:** Incluye Decretos Supremos de diferimiento arancelario al **0% GA** para tecnología, energías renovables, maquinaria y vehículos ecológicos en Bolivia.")

# -----------------------------------------------------------------------------
# 5. PESTAÑAS PRINCIPALES DE LA APLICACIÓN
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🔎 1. Clasificación Arancelaria (NANDINA)",
    "🚚 2. Costos Logísticos e Impuestos",
    "📊 3. Resumen y Cotización Landed Cost",
    "💰 4. Simulador de Margen y Precio de Venta"
])

# -----------------------------------------------------------------------------
# PESTAÑA 1: CLASIFICACIÓN ARANCELARIA SIN ERRORES
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("Buscador Inteligente de Arancel NANDINA (Bolivia 2026)")
    st.markdown("Busca cualquier producto para determinar su partida arancelaria oficial de 10 dígitos, su Gravamen Arancelario (GA) actualizado y las certificaciones requeridas.")

    col_b1, col_b2 = st.columns([2, 1])

    with col_b1:
        busqueda_input = st.text_input("🔍 Escriba el producto, marca o palabra clave (ej. laptop, celular, tractor, ropa, panel solar):", value="Laptops y Computadoras Portátiles")
    
    with col_b2:
        # Selector opcional de categorías para restringir o explorar
        categorias_disponibles = ["Todas las Categorías"] + sorted(list(set(item["categoria"] for item in base_nandina)))
        cat_seleccionada = st.selectbox("Filtrar por Categoría:", categorias_disponibles)

    # ALGORITMO DE BÚSQUEDA INTELIGENTE SIN ERRORES (FUZZY / KEYWORD MATCHING)
    query_norm = normalizar_texto(busqueda_input)
    
    coincidencias = []
    for item in base_nandina:
        if cat_seleccionada != "Todas las Categorías" and item["categoria"] != cat_seleccionada:
            continue
        
        prod_norm = normalizar_texto(item["producto"])
        key_norm = normalizar_texto(item["keywords"])
        partida_norm = normalizar_texto(item["partida"])
        desc_norm = normalizar_texto(item["descripcion"])

        # Puntuación de coincidencia
        if query_norm in prod_norm or query_norm in key_norm or query_norm in partida_norm:
            coincidencias.append(item)
        else:
            # Buscar coincidencia por palabras individuales
            palabras_query = query_norm.split()
            if any(p in prod_norm or p in key_norm or p in desc_norm for p in palabras_query if len(p) > 2):
                coincidencias.append(item)

    # LÓGICA ROBUSTA SI NO HAY COINCIDENCIA EXACTA
    if coincidencias:
        producto_seleccionado = coincidencias[0]
        coincidencia_exacta = True
    else:
        # Fallback inteligente (Sin cuelgues ni errores)
        producto_seleccionado = {
            "categoria": "⚙️ Partida General Configurable",
            "producto": busqueda_input.strip() if busqueda_input else "Mercancía General",
            "partida": "8471.90.00.00",
            "ga": 0.10, # 10% estándar de reserva
            "ice": 0.0,
            "unidad": "Unidades",
            "certificados": "Verificación Aduanera ANB Estándar",
            "descripcion": "Clasificación general asignada. Puede ajustar manualmente el Gravamen Arancelario (GA) abajo.",
            "keywords": ""
        }
        coincidencia_exacta = False

    # Despliegue de Ficha Arancelaria
    st.markdown("---")
    
    if coincidencia_exacta:
        st.success(f"✅ **Partida NANDINA Encontrada:** `{producto_seleccionado['partida']}` — {producto_seleccionado['producto']}")
    else:
        st.warning(f"ℹ️ **Sugerencia de Partida General:** No se encontró una coincidencia exacta para *'{busqueda_input}'*. Se ha asignado una partida estándar con **10.0% GA**, pero puedes personalizar la tasa abajo.")

    # Mostrar detalles en tarjeta moderna
    ga_pct_orig = producto_seleccionado["ga"] * 100
    ice_pct_orig = producto_seleccionado["ice"] * 100

    st.markdown(f"""
    <div class="card-info">
        <h4>📋 Ficha Técnica Arancelaria (Aduana Nacional de Bolivia 2026)</h4>
        <ul>
            <li><b>Código NANDINA Oficial:</b> <code>{producto_seleccionado['partida']}</code></li>
            <li><b>Descripción Arancelaria:</b> {producto_seleccionado['descripcion']}</li>
            <li><b>Gravamen Arancelario (GA) Sugerido:</b> <span class="status-badge-green">{ga_pct_orig:.1f}% GA</span></li>
            <li><b>Impuesto al Consumo Específico (ICE):</b> {ice_pct_orig:.1f}%</li>
            <li><b>Certificaciones y Permisos Requeridos:</b> {producto_seleccionado['certificados']}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Permitir ajuste manual fácil y rápido para el cliente
    st.markdown("#### ⚙️ Personalizar Tasas Arancelarias (si aplica beneficio o tarifa especial)")
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        ga_aplicado = st.number_input(
            "Gravamen Arancelario (GA %) a aplicar en el cálculo:",
            min_value=0.0,
            max_value=40.0,
            value=float(ga_pct_orig),
            step=0.5,
            help="Seleccione o ingrese el porcentaje de GA correspondiente en Bolivia (0%, 5%, 10%, 15%, 20%, 30%, 40%)."
        ) / 100.0

    with col_a2:
        ice_aplicado = st.number_input(
            "Impuesto al Consumo Específico (ICE %) si corresponde:",
            min_value=0.0,
            max_value=80.0,
            value=float(ice_pct_orig),
            step=1.0,
            help="Aplica principalmente a vehículos a combustión, bebidas, cigarrillos u otros bienes específicos."
        ) / 100.0

# -----------------------------------------------------------------------------
# PESTAÑA 2: COSTOS LOGÍSTICOS E IMPUESTOS COMPLETO
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("Parámetros de Compra, Fletes e Impuestos Aduaneros")
    st.markdown("Ingrese el valor de compra en origen, fletes tramo por tramo y gastos aduaneros en Bolivia.")

    col_l1, col_l2 = st.columns(2)

    with col_l1:
        st.markdown("#### 📦 Datos de la Compra en Origen")
        cantidad_unidades = st.number_input("Cantidad total de unidades a importar:", min_value=1, value=100, step=1)
        precio_fob_unitario = st.number_input("Precio FOB Unitario ($USD):", min_value=0.01, value=45.00, step=1.0)
        
        fob_total_calculado = cantidad_unidades * precio_fob_unitario
        st.info(f"💵 **Valor FOB Total de Mercancía:** `${fob_total_calculado:,.2f} USD`")

        st.markdown("#### 🚢 Fletes y Seguros Internacionales")
        flete_tramo_1 = st.number_input("Flete Internacional Tramo 1 (Origen a Puerto de Transbordo - Arica/Iquique/Aeropuerto) ($USD):", min_value=0.0, value=350.0, step=10.0)
        flete_tramo_2 = st.number_input("Flete Terrestre Tramo 2 (Puerto/Frontera a Aduana Bolivia) ($USD):", min_value=0.0, value=180.0, step=10.0)
        seguro_internacional = st.number_input("Seguro Internacional de Carga ($USD):", min_value=0.0, value=40.0, step=5.0)

    with col_l2:
        st.markdown("#### 🛃 Gastos de Despacho y Almacenes en Bolivia")
        gastos_puerto_almacen = st.number_input("Servicios de Puerto y Almacenes Aduaneros (ASPB / DAB) ($USD):", min_value=0.0, value=90.0, step=5.0)
        honorarios_agente_ada = st.number_input("Honorarios Agente Despachante de Aduana (ADA) ($USD):", min_value=0.0, value=130.0, step=10.0)
        gastos_certificados = st.number_input("Trámites, Certificaciones (Senasag, Agemed, ATT) ($USD):", min_value=0.0, value=60.0, step=5.0)
        flete_local_almacen = st.number_input("Flete Local (Aduana Interna a Almacén del Cliente) ($USD):", min_value=0.0, value=50.0, step=5.0)

        st.markdown("#### 🏛️ Configuración de Alícuotas Tributarias")
        usar_iva_efectivo = st.checkbox("Aplicar Alícuota Efectiva IVA Importación (14.94%)", value=True, help="En Bolivia, por Ley Tributaria la alícuota sobre base imponible aduanera CIF+GA+ICE es del 14.94%.")
        alicuota_iva_final = 0.1494 if usar_iva_efectivo else 0.13

# -----------------------------------------------------------------------------
# CÁLCULOS MATEMÁTICOS OFICIALES DE LANDED COST EN BOLIVIA
# -----------------------------------------------------------------------------
cif_total_usd = fob_total_calculado + flete_tramo_1 + flete_tramo_2 + seguro_internacional
monto_ga_usd = cif_total_usd * ga_aplicado
monto_ice_usd = cif_total_usd * ice_aplicado

base_imponible_iva_usd = cif_total_usd + monto_ga_usd + monto_ice_usd
monto_iva_usd = base_imponible_iva_usd * alicuota_iva_final

total_gastos_operativos_usd = gastos_puerto_almacen + honorarios_agente_ada + gastos_certificados + flete_local_almacen
total_impuestos_aduaneros_usd = monto_ga_usd + monto_ice_usd + monto_iva_usd

costo_landed_total_usd = cif_total_usd + total_impuestos_aduaneros_usd + total_gastos_operativos_usd
costo_landed_unitario_usd = costo_landed_total_usd / cantidad_unidades

costo_landed_total_bob = costo_landed_total_usd * tipo_cambio
costo_landed_unitario_bob = costo_landed_unitario_usd * tipo_cambio

factor_importacion = costo_landed_unitario_usd / precio_fob_unitario

# -----------------------------------------------------------------------------
# PESTAÑA 3: RESUMEN Y COTIZACIÓN LANDED COST
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("📊 Resumen del Costo Puesto en Bolivia (Landed Cost)")
    st.markdown("A continuación se presentan los resultados clave y el desglose oficial de la póliza de importación.")

    # Tarjetas Métricas
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Costo Unitario Final (USD)", f"${costo_landed_unitario_usd:,.2f}", f"+{((factor_importacion - 1)*100):.1f}% vs FOB")
    m2.metric("Costo Unitario Final (BOB)", f"Bs. {costo_landed_unitario_bob:,.2f}")
    m3.metric("Costo Total Operación (USD)", f"${costo_landed_total_usd:,.2f}")
    m4.metric("Factor de Importación Multiplicador", f"{factor_importacion:.3f}x")

    st.markdown("---")
    st.subheader("📋 Desglose Detallado de la Operación")

    datos_desglose = [
        {"Concepto": "1. Valor FOB Mercancía en Origen", "USD": fob_total_calculado, "BOB": fob_total_calculado * tipo_cambio, "% Participación": (fob_total_calculado / costo_landed_total_usd)*100},
        {"Concepto": "2. Fletes Internacionales y Seguro", "USD": flete_tramo_1 + flete_tramo_2 + seguro_internacional, "BOB": (flete_tramo_1 + flete_tramo_2 + seguro_internacional) * tipo_cambio, "% Participación": ((flete_tramo_1 + flete_tramo_2 + seguro_internacional) / costo_landed_total_usd)*100},
        {"Concepto": "3. VALOR CIF ADUANA / FRONTERA", "USD": cif_total_usd, "BOB": cif_total_usd * tipo_cambio, "% Participación": (cif_total_usd / costo_landed_total_usd)*100},
        {"Concepto": f"4. Gravamen Arancelario GA ({ga_aplicado*100:.1f}%)", "USD": monto_ga_usd, "BOB": monto_ga_usd * tipo_cambio, "% Participación": (monto_ga_usd / costo_landed_total_usd)*100},
        {"Concepto": f"5. Impuesto ICE ({ice_aplicado*100:.1f}%)", "USD": monto_ice_usd, "BOB": monto_ice_usd * tipo_cambio, "% Participación": (monto_ice_usd / costo_landed_total_usd)*100},
        {"Concepto": f"6. IVA Importación Efectivo ({alicuota_iva_final*100:.2f}%)", "USD": monto_iva_usd, "BOB": monto_iva_usd * tipo_cambio, "% Participación": (monto_iva_usd / costo_landed_total_usd)*100},
        {"Concepto": "7. Gastos de Despacho, Almacenes y Flete Local", "USD": total_gastos_operativos_usd, "BOB": total_gastos_operativos_usd * tipo_cambio, "% Participación": (total_gastos_operativos_usd / costo_landed_total_usd)*100},
        {"Concepto": "TOTAL COSTO LANDED PUESTO EN ALMACÉN", "USD": costo_landed_total_usd, "BOB": costo_landed_total_bob, "% Participación": 100.0}
    ]

    df_desglose = pd.DataFrame(datos_desglose)
    st.dataframe(
        df_desglose.style.format({
            "USD": "${:,.2f}",
            "BOB": "Bs. {:,.2f}",
            "% Participación": "{:.1f}%"
        }),
        use_container_width=True
    )

    st.info(f"💡 **Explicación para el cliente:** Tu producto comprado en origin a **${precio_fob_unitario:,.2f} USD** llega a tu almacén en Bolivia con un costo real todo incluido de **${costo_landed_unitario_usd:,.2f} USD** (o **Bs. {costo_landed_unitario_bob:,.2f} BOB**). Tu factor de multiplicación es de **{factor_importacion:.3f}x**.")

    # Generación de archivo CSV para descarga rápida de cotización
    csv_cotizacion = df_desglose.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Cotización Oficial en CSV / Excel",
        data=csv_cotizacion,
        file_name=f"cotizacion_importacion_miguel_macias_{cantidad_unidades}ud.csv",
        mime="text/csv"
    )

# -----------------------------------------------------------------------------
# PESTAÑA 4: SIMULADOR DE MARGEN Y PRECIOS DE VENTA
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("💰 Simulador de Precios de Venta y Margen de Ganancia Neta")
    st.markdown("Fije su precio de venta al público (PVP) en Bolivianos para calcular la rentabilidad real tras deducir impuestos comerciales de Bolivia (IVA e IT).")

    col_v1, col_v2 = st.columns(2)

    with col_v1:
        st.markdown("#### 🏷️ Fijación de Precio de Venta")
        pvp_propuesto_bob = st.number_input(
            "Precio de Venta al Público por unidad (Bs. BOB):",
            min_value=0.0,
            value=float(round(costo_landed_unitario_bob * 1.35, 2)),
            step=10.0
        )
        gastos_marketing_bob = st.number_input("Gastos de Comercialización/Publicidad por unidad (Bs. BOB):", min_value=0.0, value=15.0, step=5.0)

    with col_v2:
        st.markdown("#### 🧾 Régimen Comercial (SIN Bolivia)")
        emitir_factura_comercial = st.checkbox("Emitir Factura Comercial al Vender (IVA 13% + IT 3%)", value=True)

        if emitir_factura_comercial:
            debito_iva_bob = pvp_propuesto_bob * 0.13
            impuesto_it_bob = pvp_propuesto_bob * 0.03
            credito_iva_recuperable_bob = (monto_iva_usd * tipo_cambio) / cantidad_unidades
            st.caption(f"**Crédito Fiscal IVA recuperado por la importación:** `Bs. {credito_iva_recuperable_bob:,.2f} / unidad`")
        else:
            debito_iva_bob = 0.0
            impuesto_it_bob = 0.0
            credito_iva_recuperable_bob = 0.0

    # Cálculos Financieros Comerciales
    ingresos_totales_bob = pvp_propuesto_bob * cantidad_unidades
    costo_total_venta_unitario_bob = costo_landed_unitario_bob + gastos_marketing_bob + debito_iva_bob + impuesto_it_bob - credito_iva_recuperable_bob
    
    utilidad_neta_unit_bob = pvp_propuesto_bob - costo_total_venta_unitario_bob
    utilidad_neta_unit_usd = utilidad_neta_unit_bob / tipo_cambio

    utilidad_neta_total_bob = utilidad_neta_unit_bob * cantidad_unidades
    utilidad_neta_total_usd = utilidad_neta_total_bob / tipo_cambio

    roi_porcentaje = (utilidad_neta_unit_bob / costo_landed_unitario_bob) * 100 if costo_landed_unitario_bob > 0 else 0.0
    margen_comercial_pct = (utilidad_neta_unit_bob / pvp_propuesto_bob) * 100 if pvp_propuesto_bob > 0 else 0.0

    st.markdown("---")
    st.subheader("📈 Proyección de Utilidad y Rentabilidad Neta")

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Ingreso Total Ventas (BOB)", f"Bs. {ingresos_totales_bob:,.2f}")
    r2.metric("Ganancia Neta por Unidad", f"Bs. {utilidad_neta_unit_bob:,.2f}", f"${utilidad_neta_unit_usd:,.2f} USD")
    r3.metric("Ganancia Neta Lote Completo", f"Bs. {utilidad_neta_total_bob:,.2f}", f"${utilidad_neta_total_usd:,.2f} USD")
    r4.metric("Retorno de Inversión (ROI)", f"{roi_porcentaje:.1f}%", f"{margen_comercial_pct:.1f}% sobre Venta")

    if utilidad_neta_unit_bob > 0:
        st.success(f"🎉 **Operación Altamente Rentable:** Al vender a **Bs. {pvp_propuesto_bob:,.2f}**, obtienes una ganancia neta libre de impuestos de **Bs. {utilidad_neta_unit_bob:,.2f}** por unidad (**${utilidad_neta_unit_usd:,.2f} USD**), alcanzando un ROI del **{roi_porcentaje:.1f}%**.")
    else:
        st.error(f"⚠️ **Precio Mínimo de Equilibrio:** Tu precio de venta está por debajo del costo real e impuestos. Necesitas vender a mínimo **Bs. {(costo_landed_unitario_bob + gastos_marketing_bob):,.2f}** para no generar pérdidas.")

# -----------------------------------------------------------------------------
# 6. PIE DE PÁGINA OFICIAL CON DERECHOS DE AUTOR
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.92rem; padding: 15px 0;">
    🚢 <b>Plataforma de Cálculo de Importaciones y Costos Landed Bolivia 2026</b><br>
    Desarrollado por <b>Miguel Macias</b> | Basado en Normativa Aduana Nacional de Bolivia (ANB) y Nomenclatura NANDINA
</div>
""", unsafe_allow_html=True)
