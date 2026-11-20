import streamlit as st
import pandas as pd
import joblib
import json
import secrets
from pathlib import Path

# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="Clasificador de Adenocarcinoma Pulmonar",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# ESTILOS
# ============================================================

st.markdown("""
<style>

    .block-container {
        max-width: 1250px;
        padding-top: 1.1rem;
        padding-bottom: 1rem;
    }

    h1, h2, h3 {
        color: #17324d;
    }

    .subtitulo {
        color: #5f6b76;
        font-size: 1.03rem;
        margin-bottom: 1rem;
    }

    .firma {
        background: #f5f8fb;
        border: 1px solid #d9e3eb;
        border-radius: 12px;
        padding: 12px 18px;
        margin-bottom: 18px;
        color: #33475b;
    }

    .resultado-muy-bajo,
    .resultado-bajo,
    .resultado-moderado,
    .resultado-alto {
        border-radius: 12px;
        padding: 16px 22px;
        font-size: 1rem;
        line-height: 1.35;
        margin-top: 8px;
    }

    .resultado-muy-bajo {
        background: #eef8f1;
        border-left: 7px solid #4c9b67;
    }

    .resultado-bajo {
        background: #f5f8ec;
        border-left: 7px solid #8cae58;
    }

    .resultado-moderado {
        background: #fff8e8;
        border-left: 7px solid #d9a53a;
    }

    .resultado-alto {
        background: #fff2ee;
        border-left: 7px solid #c65a50;
    }

    .resultado-muy-bajo h3,
    .resultado-bajo h3,
    .resultado-moderado h3,
    .resultado-alto h3 {
        margin-top: 0;
        margin-bottom: 8px;
    }

    .resultado-muy-bajo p,
    .resultado-bajo p,
    .resultado-moderado p,
    .resultado-alto p {
        margin-top: 4px;
        margin-bottom: 0;
    }

    .nota-clinica {
        background: #eef4fa;
        border: 1px solid #d5e2ee;
        border-radius: 10px;
        padding: 12px 16px;
        margin-top: 12px;
        color: #33475b;
        font-size: 0.92rem;
        line-height: 1.4;
    }

    div[data-testid="stNumberInput"] input {
        font-size: 0.95rem;
    }

</style>
""", unsafe_allow_html=True)

# ============================================================
# CARGAR CLASIFICADOR Y FIRMA GÉNICA
# ============================================================

try:
    ruta = Path(__file__).resolve().parent
    clasificador = joblib.load(ruta / "modelo_5genes.pkl")

    with open(ruta / "genes_5.json", "r", encoding="utf-8") as archivo:
        nombres_genes = json.load(archivo)

    with open(ruta / "muestras_ejemplo.json", "r", encoding="utf-8") as archivo:
        muestras_ejemplo = json.load(archivo)

except Exception as e:
    st.error(f"No fue posible cargar la herramienta: {e}")
    st.stop()

# ============================================================
# FUNCIÓN: BARRA VISUAL
# ============================================================

def barra_calor(valor):

    posicion = max(0, min(float(valor) * 100, 100))
    puntuacion = f"{valor:.4f}".replace(".", ",")
    porcentaje = f"{valor * 100:.2f}".replace(".", ",")

    html = f"""
<div style="
    margin-top:16px;
    margin-bottom:18px;
    padding:16px 20px 12px 20px;
    background:white;
    border:1px solid #dce4ea;
    border-radius:12px;
">

<div style="
    display:flex;
    justify-content:space-between;
    align-items:baseline;
    flex-wrap:wrap;
    gap:8px;
    margin-bottom:10px;
">
<span style="font-size:1rem; font-weight:600; color:#17324d;">
Puntuación del modelo Random Forest para la clase tumoral
</span>
<span style="font-size:1.1rem; font-weight:700; color:#17324d;">
{puntuacion} ({porcentaje} %)
</span>
</div>

<div style="
    position:relative;
    width:100%;
    height:22px;
    border-radius:12px;
    background:linear-gradient(
        to right,
        #45945f 0%,
        #88b55c 30%,
        #efc44c 55%,
        #e58b42 75%,
        #c64949 100%
    );
">
</div>

<div style="
    position:relative;
    width:100%;
    height:32px;
">

<div style="
    position:absolute;
    left:calc({posicion}% - 10px);
    top:4px;
    width:0;
    height:0;
    border-left:10px solid transparent;
    border-right:10px solid transparent;
    border-bottom:18px solid #17324d;
">
</div>

</div>

<div style="
    display:flex;
    justify-content:space-between;
    font-size:0.82rem;
    color:#5c6873;
">

<div style="width:25%; text-align:left;">
Baja
</div>

<div style="width:25%; text-align:center;">
Intermedia
</div>

<div style="width:25%; text-align:center;">
Elevada
</div>

<div style="width:25%; text-align:right;">
Muy elevada
</div>

</div>

</div>
"""

    return html

# ============================================================
# FUNCIÓN PARA LIMPIAR CAMPOS
# ============================================================

def limpiar_campos():

    for gen in nombres_genes:
        st.session_state[f"valor_{gen}"] = 0.0

    st.session_state["mostrar_resultado"] = False
    st.session_state["muestra_ejemplo"] = None


def registrar_edicion_manual():
    st.session_state["muestra_ejemplo"] = None
    st.session_state["mostrar_resultado"] = False


def cargar_muestra_ejemplo():
    seleccion = st.session_state["tipo_ejemplo"]
    clase = {"Cualquiera": None, "Tumoral": 1, "Normal": 0}[seleccion]
    candidatas = [
        muestra for muestra in muestras_ejemplo
        if clase is None or muestra["Clase"] == clase
    ]
    muestra = secrets.choice(candidatas)

    for gen in nombres_genes:
        st.session_state[f"valor_{gen}"] = float(muestra[gen])

    st.session_state["muestra_ejemplo"] = {
        "Sample_ID": muestra["Sample_ID"],
        "Clase": muestra["Clase"],
    }
    st.session_state["mostrar_resultado"] = False

# ============================================================
# ENCABEZADO
# ============================================================

st.title("🧬 Clasificador de Adenocarcinoma Pulmonar")

st.markdown(
    """
    <div class="subtitulo">
        Prototipo académico de clasificación transcriptómica mediante Random Forest
        y la firma de cinco genes seleccionada por Forward Selection.
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# FIRMA GÉNICA
# ============================================================

firma_texto = " &nbsp;&nbsp; • &nbsp;&nbsp; ".join(nombres_genes)

st.markdown(
    f"""
    <div class="firma">
        <b>Firma génica utilizada:</b>
        &nbsp;&nbsp; {firma_texto}
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# INICIALIZAR CAMPOS
# ============================================================

for gen in nombres_genes:

    if f"valor_{gen}" not in st.session_state:
        st.session_state[f"valor_{gen}"] = 0.0

if "mostrar_resultado" not in st.session_state:
    st.session_state["mostrar_resultado"] = False

if "muestra_ejemplo" not in st.session_state:
    st.session_state["muestra_ejemplo"] = None

# ============================================================
# INGRESO DE DATOS
# ============================================================

st.subheader("Valores de expresión de la muestra")

st.caption("Ingrese los cinco valores de expresión de una misma muestra, normalizados en una escala compatible con el entrenamiento.")

columnas = st.columns(5)

for i, gen in enumerate(nombres_genes):

    with columnas[i]:

        st.number_input(
            label=f"Gen {gen}",
            format="%.10f",
            key=f"valor_{gen}",
            on_change=registrar_edicion_manual,
        )

# Los ejemplos provienen exclusivamente de la base de prueba, no del entrenamiento.
col_tipo, col_ejemplo = st.columns([1, 2])

with col_tipo:
    st.selectbox(
        "Tipo de muestra de ejemplo",
        ["Cualquiera", "Tumoral", "Normal"],
        key="tipo_ejemplo",
    )

with col_ejemplo:
    st.write("")
    st.button(
        "🎲 Cargar muestra de ejemplo",
        use_container_width=True,
        on_click=cargar_muestra_ejemplo,
    )

if st.session_state["muestra_ejemplo"] is not None:
    ejemplo = st.session_state["muestra_ejemplo"]
    st.caption(
        f"Ejemplo cargado: {ejemplo['Sample_ID']} · "
        "Muestra real de la base de prueba. "
        "Su clase conocida se mostrará al analizarla."
    )

# ============================================================
# BOTONES
# ============================================================

col_analizar, col_limpiar = st.columns([3, 1])

with col_analizar:

    analizar = st.button(
        "🔬 Analizar muestra",
        use_container_width=True,
        type="primary"
    )

with col_limpiar:

    st.button(
        "↻ Limpiar valores",
        use_container_width=True,
        on_click=limpiar_campos
    )

# ============================================================
# ANÁLISIS
# ============================================================

if analizar:

    valores = [
        st.session_state[f"valor_{gen}"]
        for gen in nombres_genes
    ]

    df_usuario = pd.DataFrame(
        [valores],
        columns=nombres_genes
    )

    try:

        probabilidades = clasificador.predict_proba(df_usuario)[0]

        valor_indicios = float(probabilidades[1])
        prediccion = int(clasificador.predict(df_usuario)[0])

        st.session_state["ultimo_valor"] = valor_indicios
        st.session_state["ultima_prediccion"] = prediccion
        st.session_state["ultimos_datos"] = valores
        st.session_state["mostrar_resultado"] = True

    except Exception as e:

        st.error(f"No fue posible realizar el análisis: {e}")

# ============================================================
# MOSTRAR RESULTADO
# ============================================================

if st.session_state.get("mostrar_resultado", False):

    valor_indicios = st.session_state["ultimo_valor"]

    st.divider()

    st.subheader("Resultado del análisis")

    if st.session_state["muestra_ejemplo"] is not None:
        ejemplo = st.session_state["muestra_ejemplo"]
        clase_real = "Tumoral (1)" if ejemplo["Clase"] == 1 else "Normal (0)"
        prediccion = st.session_state["ultima_prediccion"]
        clase_estimada = "Tumoral (1)" if prediccion == 1 else "Normal (0)"
        coincide = "Sí" if prediccion == ejemplo["Clase"] else "No"
        st.info(
            f"**Muestra de prueba:** {ejemplo['Sample_ID']} · "
            f"**Clase real:** {clase_real} · "
            f"**Predicción del modelo:** {clase_estimada} · "
            f"**¿Coinciden?:** {coincide}. "
            "Comparación académica; no constituye un diagnóstico."
        )

    # --------------------------------------------------------
    # BARRA VISUAL
    # --------------------------------------------------------

    st.markdown(
        barra_calor(valor_indicios),
        unsafe_allow_html=True
    )

    # ========================================================
    # MUY BAJO
    # ========================================================

    if valor_indicios < 0.20:

        st.markdown("""
<div class="resultado-muy-bajo">

<h3>🟢 Puntuación tumoral muy baja</h3>

<p>
El clasificador Random Forest asignó una puntuación inferior a 0,20 a la clase tumoral. Esto describe exclusivamente la salida estadística del modelo, sin determinar un riesgo clínico ni descartar una enfermedad.
</p>

</div>
""", unsafe_allow_html=True)

    # ========================================================
    # BAJO
    # ========================================================

    elif valor_indicios < 0.40:

        st.markdown("""
<div class="resultado-bajo">

<h3>🟢 Puntuación tumoral baja</h3>

<p>
El clasificador Random Forest asignó una puntuación de 0,20 a menos de 0,40 a la clase tumoral. Esta cifra no está calibrada como probabilidad clínica y no permite extraer conclusiones diagnósticas.
</p>

</div>
""", unsafe_allow_html=True)

    # ========================================================
    # MODERADO
    # ========================================================

    elif valor_indicios < 0.70:

        st.markdown("""
<div class="resultado-moderado">

<h3>🟠 Puntuación tumoral intermedia</h3>

<p>
El clasificador Random Forest asignó una puntuación de 0,40 a menos de 0,70 a la clase tumoral. Es una puntuación del modelo para investigación, no una recomendación sobre pruebas o atención médica.
</p>

</div>
""", unsafe_allow_html=True)

    # ========================================================
    # PRIORITARIO
    # ========================================================

    else:

        st.markdown("""
<div class="resultado-alto">

<h3>🔴 Puntuación tumoral elevada</h3>

<p>
El clasificador Random Forest asignó una puntuación igual o superior a 0,70 a la clase tumoral. Se trata de una medida estadística no validada para establecer urgencia o decisiones médicas.
</p>

</div>
""", unsafe_allow_html=True)

    # ========================================================
    # NOTA DE SEGURIDAD
    # ========================================================

    st.markdown("""
<div class="nota-clinica">

<b>Importante:</b> prototipo de investigación académica, no una herramienta diagnóstica. La puntuación de la clase tumoral no equivale a una probabilidad clínica de cáncer. Los niveles de color son únicamente una representación visual de esta puntuación y no indican prioridad médica.

</div>
""", unsafe_allow_html=True)

    # ========================================================
    # DETALLE DE LOS VALORES
    # ========================================================

    with st.expander("🔍 Ver valores de expresión utilizados"):

        tabla = pd.DataFrame({
            "Gen": nombres_genes,
            "Valor de expresión": [
                f"{v:.10f}"
                for v in st.session_state["ultimos_datos"]
            ]
        })

        st.dataframe(
            tabla,
            use_container_width=True,
            hide_index=True
        )
