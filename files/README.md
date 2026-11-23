# ✅ Lista de verificación integrada ISO 9001 · 14001 · 45001

Aplicación web en **Streamlit** para evaluar un sistema de gestión integrado
(Calidad, Ambiente y SST) siguiendo la estructura de alto nivel común (cláusulas 4 a 10).

## Funciones
- 49 requisitos organizados por cláusula, con referencia a ISO 9001:2015, ISO 14001:2015 e ISO 45001:2018.
- Selección de las normas aplicables; el checklist se adapta (requisitos comunes vs. específicos).
- Estado por requisito: Cumple / Parcial / No cumple / No aplica / Sin evaluar, con evidencia y observaciones.
- Resumen: % de cumplimiento y avance global, por norma y por cláusula, y lista de hallazgos.
- Exportación a Excel/CSV e importación del Excel para continuar la evaluación.

## Cálculo
Cumple = 1, Parcial = 0,5, No cumple = 0. "No aplica" y "Sin evaluar" no entran en el % de cumplimiento.

## Ejecutar localmente
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicar en streamlit.app
1. Sube esta carpeta a un repositorio de GitHub (`app.py` en la raíz).
2. Entra a https://share.streamlit.io e inicia sesión con GitHub.
3. **Create app** → elige el repositorio, la rama y `app.py` como archivo principal → **Deploy**.

## Aviso
Las preguntas están redactadas con palabras propias; no reproducen el texto de las normas.
Es una herramienta de apoyo y no sustituye a las normas oficiales ni a una auditoría certificadora.
