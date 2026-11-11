import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Calculadora de Consumo Energético de Laboratorio",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ Calculadora de Consumo Energético de Laboratorio")
st.write(
    "Registra los equipos eléctricos del laboratorio para estimar su consumo "
    "energético y costo mensual."
)

# Estado temporal de la aplicación
if "equipos" not in st.session_state:
    st.session_state.equipos = []

if "tarifa" not in st.session_state:
    st.session_state.tarifa = 0.70


def calcular_resultados(equipos, tarifa):
    """Calcula el consumo y costo mensual de cada equipo."""
    filas = []
    for equipo in equipos:
        consumo = (
            equipo["potencia"] * equipo["cantidad"]
            * equipo["horas_diarias"] * equipo["dias_mensuales"] / 1000
        )
        costo = consumo * tarifa
        filas.append(
            {
                "Equipo": equipo["nombre"],
                "Potencia (W)": equipo["potencia"],
                "Cantidad": equipo["cantidad"],
                "Horas diarias": equipo["horas_diarias"],
                "Días mensuales": equipo["dias_mensuales"],
                "Consumo mensual (kWh)": consumo,
                "Costo mensual (S/)": costo,
            }
        )
    return pd.DataFrame(filas)


st.subheader("1. Tarifa eléctrica")
st.session_state.tarifa = st.number_input(
    "Tarifa eléctrica (S/ por kWh)",
    min_value=0.0,
    value=float(st.session_state.tarifa),
    step=0.01,
    format="%.4f",
    help="Se aplicará la misma tarifa a todos los equipos.",
)

st.subheader("2. Registrar un equipo")
with st.form("formulario_equipo", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre del equipo", placeholder="Ej. Computadora")
        potencia = st.number_input(
            "Potencia (W)", min_value=0.0, value=100.0, step=10.0
        )
        cantidad = st.number_input(
            "Cantidad de equipos", min_value=1, value=1, step=1
        )
    with col2:
        horas = st.number_input(
            "Horas de funcionamiento por día",
            min_value=0.0, max_value=24.0, value=8.0, step=0.5
        )
        dias = st.number_input(
            "Días de funcionamiento por mes",
            min_value=0, max_value=31, value=22, step=1
        )

    enviado = st.form_submit_button("Agregar equipo", type="primary")

    if enviado:
        if not nombre.strip():
            st.error("Ingresa un nombre para el equipo.")
        elif potencia <= 0:
            st.error("La potencia debe ser mayor que cero.")
        elif cantidad < 1:
            st.error("La cantidad debe ser al menos 1.")
        elif not (0 <= horas <= 24):
            st.error("Las horas diarias deben estar entre 0 y 24.")
        elif not (0 <= dias <= 31):
            st.error("Los días mensuales deben estar entre 0 y 31.")
        else:
            st.session_state.equipos.append(
                {
                    "nombre": nombre.strip(),
                    "potencia": float(potencia),
                    "cantidad": int(cantidad),
                    "horas_diarias": float(horas),
                    "dias_mensuales": int(dias),
                }
            )
            st.success(f"Se agregó «{nombre.strip()}» correctamente.")

st.subheader("3. Equipos registrados")
if st.session_state.equipos:
    for indice, equipo in enumerate(st.session_state.equipos):
        st.write(
            f"**{indice + 1}. {equipo['nombre']}** — "
            f"{equipo['potencia']:g} W | Cantidad: {equipo['cantidad']} | "
            f"{equipo['horas_diarias']:g} h/día | "
            f"{equipo['dias_mensuales']} días/mes"
        )

    opciones = {
        f"{i + 1}. {equipo['nombre']}": i
        for i, equipo in enumerate(st.session_state.equipos)
    }
    seleccion = st.selectbox(
        "Selecciona un equipo para eliminar",
        options=list(opciones.keys()),
        key="equipo_a_eliminar",
    )
    if st.button("Eliminar equipo seleccionado"):
        indice = opciones[seleccion]
        eliminado = st.session_state.equipos.pop(indice)
        st.success(f"Se eliminó «{eliminado['nombre']}».")
        st.rerun()

    if st.button("Eliminar todos los equipos"):
        st.session_state.equipos = []
        st.rerun()
else:
    st.info("Todavía no hay equipos registrados. Agrega uno usando el formulario.")

st.divider()
st.subheader("4. Resultados del consumo y costo mensual")

if st.session_state.equipos:
    resultados = calcular_resultados(
        st.session_state.equipos, st.session_state.tarifa
    )

    # Tabla de resultados
    st.dataframe(
        resultados.style.format(
            {
                "Potencia (W)": "{:,.2f}",
                "Horas diarias": "{:,.2f}",
                "Consumo mensual (kWh)": "{:,.2f}",
                "Costo mensual (S/)": "S/ {:,.2f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    consumo_total = resultados["Consumo mensual (kWh)"].sum()
    costo_total = resultados["Costo mensual (S/)"].sum()

    m1, m2, m3 = st.columns(3)
    m1.metric("Consumo total mensual", f"{consumo_total:,.2f} kWh")
    m2.metric("Costo total mensual", f"S/ {costo_total:,.2f}")
    m3.metric("Tarifa aplicada", f"S/ {st.session_state.tarifa:,.4f}/kWh")

    st.subheader("5. Comparación del consumo por equipo")
    grafico = resultados.set_index("Equipo")[["Consumo mensual (kWh)"]]
    st.bar_chart(grafico, y="Consumo mensual (kWh)", use_container_width=True)

    equipo_mayor = resultados.loc[
        resultados["Consumo mensual (kWh)"].idxmax()
    ]
    st.info(
        f"**Equipo con mayor consumo:** {equipo_mayor['Equipo']} "
        f"({equipo_mayor['Consumo mensual (kWh)']:,.2f} kWh al mes)."
    )

    # Archivo CSV descargable, compatible con Excel en configuración regional española.
    csv = resultados.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
    st.download_button(
        label="Descargar resultados en CSV",
        data=csv,
        file_name="resultados_consumo_energetico.csv",
        mime="text/csv",
    )
else:
    st.warning("Registra al menos un equipo para visualizar los resultados.")
