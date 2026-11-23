"""
Lista de verificación integrada de sistemas de gestión
ISO 9001 (Calidad) · ISO 14001 (Ambiente) · ISO 45001 (SST)

Ejecutar localmente:  streamlit run app.py
"""
import io
from datetime import date

import pandas as pd
import streamlit as st

from checklist_data import CLAUSES, ITEMS, STANDARDS

st.set_page_config(
    page_title="Lista de verificación integrada ISO 9001 · 14001 · 45001",
    page_icon="✅",
    layout="wide",
)

ESTADOS = ["Sin evaluar", "Cumple", "Parcial", "No cumple", "No aplica"]
PUNTOS = {"Cumple": 1.0, "Parcial": 0.5, "No cumple": 0.0}
HOJA = "Lista de verificación"

# ----------------------------------------------------------------- Estado
if "answers" not in st.session_state:
    st.session_state.answers = {
        it["id"]: {"estado": "Sin evaluar", "evidencia": "", "obs": ""} for it in ITEMS
    }
answers = st.session_state.answers


def _set_answer(item_id, estado, evidencia, obs):
    answers[item_id] = {"estado": estado, "evidencia": evidencia, "obs": obs}
    st.session_state[f"est_{item_id}"] = estado
    st.session_state[f"evi_{item_id}"] = evidencia
    st.session_state[f"obs_{item_id}"] = obs


def reiniciar():
    for it in ITEMS:
        _set_answer(it["id"], "Sin evaluar", "", "")


def importar(archivo):
    try:
        df = pd.read_excel(archivo, sheet_name=HOJA).fillna("")
    except Exception as exc:  # noqa: BLE001
        st.sidebar.error(f"No se pudo leer el archivo: {exc}")
        return
    if "ID" not in df.columns:
        st.sidebar.error("El archivo no tiene la columna 'ID'.")
        return
    n = 0
    for _, fila in df.iterrows():
        item_id = str(fila["ID"]).strip()
        if item_id in answers:
            estado = str(fila.get("Estado", "Sin evaluar"))
            if estado not in ESTADOS:
                estado = "Sin evaluar"
            _set_answer(
                item_id,
                estado,
                str(fila.get("Evidencia", "")),
                str(fila.get("Observaciones", "")),
            )
            n += 1
    st.sidebar.success(f"{n} requisitos importados.")


# ---------------------------------------------------------------- Sidebar
with st.sidebar:
    st.header("⚙️ Configuración")
    organizacion = st.text_input("Organización", key="org")
    responsable = st.text_input("Auditor / responsable", key="resp")
    fecha = st.date_input("Fecha de la evaluación", value=date.today(), key="fecha")

    seleccion = st.multiselect(
        "Normas aplicables",
        options=list(STANDARDS.keys()),
        default=list(STANDARDS.keys()),
        format_func=lambda k: f"{STANDARDS[k]['nombre']} · {STANDARDS[k]['tema']}",
    )
    modo = st.radio(
        "Requisitos a mostrar",
        ["Todos", "Solo comunes (integrados)", "Solo específicos de una norma"],
    )

    st.divider()
    st.subheader("📥 Importar avance")
    archivo = st.file_uploader("Excel exportado previamente", type=["xlsx"])
    if archivo is not None and st.button("Aplicar importación"):
        importar(archivo)

    if st.button("🗑️ Reiniciar evaluación"):
        reiniciar()
        st.rerun()

    st.caption(
        "Herramienta de apoyo. No sustituye a las normas oficiales ni a una auditoría "
        "de tercera parte."
    )

st.title("✅ Lista de verificación integrada")
st.caption("Sistema de gestión integrado · ISO 9001:2015 · ISO 14001:2015 · ISO 45001:2018")

if not seleccion:
    st.warning("Selecciona al menos una norma en la barra lateral.")
    st.stop()


# ----------------------------------------------------------- Filtro de ítems
def aplica(item):
    normas_item = [s for s in item["refs"] if s in seleccion]
    if not normas_item:
        return False
    comun = len(item["refs"]) == len(STANDARDS)
    if modo == "Solo comunes (integrados)":
        return comun
    if modo == "Solo específicos de una norma":
        return len(item["refs"]) == 1
    return True


items_visibles = [it for it in ITEMS if aplica(it)]


def etiqueta_normas(item):
    return ", ".join(STANDARDS[s]["nombre"] for s in item["refs"])


def etiqueta_refs(item):
    return " | ".join(f"{s}: {r}" for s, r in item["refs"].items())


def tipo(item):
    return "Integrado" if len(item["refs"]) == len(STANDARDS) else "Específico"


def construir_df():
    filas = []
    for it in items_visibles:
        a = answers[it["id"]]
        filas.append(
            {
                "ID": it["id"],
                "Cláusula": it["clause"],
                "Capítulo": CLAUSES[it["clause"]],
                "Tema": it["tema"],
                "Requisito (pregunta)": it["pregunta"],
                "Tipo": tipo(it),
                "Normas": etiqueta_normas(it),
                "Referencias": etiqueta_refs(it),
                "Estado": a["estado"],
                "Evidencia": a["evidencia"],
                "Observaciones": a["obs"],
            }
        )
    return pd.DataFrame(filas)


def cumplimiento(sub):
    evaluados = sub[sub["Estado"].isin(PUNTOS)]
    if evaluados.empty:
        return None
    return round(100 * evaluados["Estado"].map(PUNTOS).sum() / len(evaluados), 1)


def avance(sub):
    aplicables = sub[sub["Estado"] != "No aplica"]
    if aplicables.empty:
        return None
    ev = aplicables[aplicables["Estado"] != "Sin evaluar"]
    return round(100 * len(ev) / len(aplicables), 1)


# ------------------------------------------------------------------ Render
def render_item(it):
    iid = it["id"]
    for pref, campo in (("est", "estado"), ("evi", "evidencia"), ("obs", "obs")):
        if f"{pref}_{iid}" not in st.session_state:
            st.session_state[f"{pref}_{iid}"] = answers[iid][campo]

    with st.container(border=True):
        st.markdown(f"**{iid} · {it['tema']}** &nbsp; `{tipo(it)}`")
        st.write(it["pregunta"])
        st.caption("📖 " + etiqueta_refs(it).replace("9001", "ISO 9001")
                   .replace("14001", "ISO 14001").replace("45001", "ISO 45001"))
        estado = st.radio(
            "Estado",
            ESTADOS,
            horizontal=True,
            key=f"est_{iid}",
            label_visibility="collapsed",
        )
        c1, c2 = st.columns(2)
        evidencia = c1.text_input("Evidencia objetiva", key=f"evi_{iid}")
        obs = c2.text_input("Observaciones / acción", key=f"obs_{iid}")
        answers[iid] = {"estado": estado, "evidencia": evidencia, "obs": obs}


tab_names = ["📊 Resumen"] + [f"{c}. {n}" for c, n in CLAUSES.items()]
tabs = st.tabs(tab_names)

# Primero se dibujan las cláusulas (para que el resumen use respuestas actualizadas)
for idx, clausula in enumerate(CLAUSES, start=1):
    with tabs[idx]:
        st.subheader(f"{clausula}. {CLAUSES[clausula]}")
        items_c = [it for it in items_visibles if it["clause"] == clausula]
        if not items_c:
            st.info("No hay requisitos para esta cláusula con el filtro actual.")
        for it in items_c:
            render_item(it)

df = construir_df()

# ----------------------------------------------------------------- Resumen
with tabs[0]:
    if df.empty:
        st.info("No hay requisitos con los filtros actuales.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        glob = cumplimiento(df)
        av = avance(df)
        c1.metric("Cumplimiento global", f"{glob} %" if glob is not None else "—")
        c2.metric("Avance de la evaluación", f"{av} %" if av is not None else "—")
        c3.metric("No cumple", int((df["Estado"] == "No cumple").sum()))
        c4.metric("Parcial", int((df["Estado"] == "Parcial").sum()))
        st.progress(int(av or 0) / 100, text="Avance de la evaluación")

        st.markdown("### Cumplimiento por norma")
        filas_norma = []
        for s in seleccion:
            nombre = STANDARDS[s]["nombre"]
            sub = df[df["Normas"].str.contains(nombre, regex=False)]
            filas_norma.append(
                {
                    "Norma": f"{nombre} ({STANDARDS[s]['tema']})",
                    "Requisitos": len(sub),
                    "Cumple": int((sub["Estado"] == "Cumple").sum()),
                    "Parcial": int((sub["Estado"] == "Parcial").sum()),
                    "No cumple": int((sub["Estado"] == "No cumple").sum()),
                    "No aplica": int((sub["Estado"] == "No aplica").sum()),
                    "Sin evaluar": int((sub["Estado"] == "Sin evaluar").sum()),
                    "Cumplimiento %": cumplimiento(sub),
                }
            )
        df_norma = pd.DataFrame(filas_norma)
        st.dataframe(df_norma, hide_index=True, use_container_width=True)

        st.markdown("### Cumplimiento por cláusula")
        filas_cl = []
        for c, nombre in CLAUSES.items():
            sub = df[df["Cláusula"] == c]
            if sub.empty:
                continue
            filas_cl.append(
                {
                    "Cláusula": f"{c}. {nombre}",
                    "Requisitos": len(sub),
                    "Cumplimiento %": cumplimiento(sub),
                    "Avance %": avance(sub),
                }
            )
        df_cl = pd.DataFrame(filas_cl)
        col_a, col_b = st.columns([3, 2])
        col_a.dataframe(df_cl, hide_index=True, use_container_width=True)
        col_b.bar_chart(
            df_cl.set_index("Cláusula")[["Cumplimiento %"]].fillna(0), horizontal=True
        )

        st.markdown("### Hallazgos (No cumple / Parcial)")
        hall = df[df["Estado"].isin(["No cumple", "Parcial"])][
            ["ID", "Tema", "Estado", "Referencias", "Evidencia", "Observaciones"]
        ]
        if hall.empty:
            st.success("Sin hallazgos registrados.")
        else:
            st.dataframe(hall, hide_index=True, use_container_width=True)

        # ------------------------------------------------------- Exportar
        st.markdown("### 📤 Exportar")
        meta = pd.DataFrame(
            {
                "Campo": ["Organización", "Auditor / responsable", "Fecha", "Normas"],
                "Valor": [
                    organizacion,
                    responsable,
                    str(fecha),
                    ", ".join(STANDARDS[s]["nombre"] for s in seleccion),
                ],
            }
        )
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=HOJA, index=False)
            df_norma.to_excel(writer, sheet_name="Resumen por norma", index=False)
            df_cl.to_excel(writer, sheet_name="Resumen por cláusula", index=False)
            hall.to_excel(writer, sheet_name="Hallazgos", index=False)
            meta.to_excel(writer, sheet_name="Datos", index=False)
            for ws in writer.book.worksheets:
                for col in ws.columns:
                    largo = max(len(str(c.value)) if c.value is not None else 0 for c in col)
                    ws.column_dimensions[col[0].column_letter].width = min(max(12, largo), 60)
        nombre_archivo = f"checklist_integrada_{date.today().isoformat()}.xlsx"
        st.download_button(
            "Descargar Excel",
            data=buffer.getvalue(),
            file_name=nombre_archivo,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        st.download_button(
            "Descargar CSV",
            data=df.to_csv(index=False).encode("utf-8-sig"),
            file_name=nombre_archivo.replace(".xlsx", ".csv"),
            mime="text/csv",
        )
