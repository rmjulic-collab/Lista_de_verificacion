"""
Base de datos de la lista de verificación integrada.

Estructura de alto nivel (HLS / Anexo SL) común a:
  - ISO 9001:2015  (Gestión de la calidad)
  - ISO 14001:2015 (Gestión ambiental)
  - ISO 45001:2018 (Seguridad y salud en el trabajo)

Las preguntas están redactadas con palabras propias (no son texto literal de las
normas). Las referencias numéricas apuntan a las cláusulas de cada norma.
Esta herramienta es de apoyo: no sustituye a las normas oficiales ni a una
auditoría de tercera parte.
"""

STANDARDS = {
    "9001": {"nombre": "ISO 9001", "tema": "Calidad"},
    "14001": {"nombre": "ISO 14001", "tema": "Ambiente"},
    "45001": {"nombre": "ISO 45001", "tema": "SST"},
}

CLAUSES = {
    4: "Contexto de la organización",
    5: "Liderazgo y participación",
    6: "Planificación",
    7: "Apoyo",
    8: "Operación",
    9: "Evaluación del desempeño",
    10: "Mejora",
}

ITEMS = []
_counters = {}


def _i(clause, tema, pregunta, q=None, e=None, s=None):
    """Registra un requisito. q=ISO 9001, e=ISO 14001, s=ISO 45001."""
    _counters[clause] = _counters.get(clause, 0) + 1
    refs = {}
    if q:
        refs["9001"] = q
    if e:
        refs["14001"] = e
    if s:
        refs["45001"] = s
    ITEMS.append(
        {
            "id": f"{clause}.{_counters[clause]:02d}",
            "clause": clause,
            "tema": tema,
            "pregunta": pregunta,
            "refs": refs,
        }
    )


# ---------------------------------------------------------------- Cláusula 4
_i(4, "Contexto de la organización",
   "¿Se han determinado y se revisan periódicamente las cuestiones externas e internas "
   "que afectan la dirección estratégica y los resultados previstos del sistema "
   "(incluyendo, cuando aplique, el cambio climático)?",
   q="4.1", e="4.1", s="4.1")
_i(4, "Partes interesadas",
   "¿Se identificaron las partes interesadas pertinentes (clientes, trabajadores, "
   "autoridades, proveedores, comunidad) y sus necesidades y expectativas, definiendo "
   "cuáles se convierten en requisitos legales y otros requisitos?",
   q="4.2", e="4.2", s="4.2")
_i(4, "Alcance del sistema de gestión",
   "¿Está definido y documentado el alcance del sistema de gestión integrado "
   "(límites, sedes, actividades, productos y servicios)?",
   q="4.3", e="4.3", s="4.3")
_i(4, "Sistema de gestión y procesos",
   "¿Están determinados los procesos necesarios (entradas, salidas, secuencia, "
   "interacciones, responsables e indicadores) y se mantiene el sistema integrado "
   "con mejora continua?",
   q="4.4", e="4.4", s="4.4")

# ---------------------------------------------------------------- Cláusula 5
_i(5, "Liderazgo y compromiso",
   "¿La alta dirección demuestra liderazgo: asume la rendición de cuentas, integra los "
   "requisitos del sistema en los procesos del negocio, asigna recursos y promueve la "
   "mejora?",
   q="5.1.1", e="5.1", s="5.1")
_i(5, "Enfoque al cliente",
   "¿Se determinan y cumplen los requisitos del cliente y los legales aplicables, y se "
   "consideran los riesgos que afectan la conformidad del producto/servicio y la "
   "satisfacción del cliente?",
   q="5.1.2")
_i(5, "Política (calidad)",
   "¿La política incluye el compromiso de satisfacer los requisitos aplicables y de "
   "mejorar continuamente el sistema de gestión de la calidad?",
   q="5.2.1")
_i(5, "Política (ambiental)",
   "¿La política ambiental incluye el compromiso de proteger el ambiente (incluida la "
   "prevención de la contaminación), cumplir los requisitos legales y otros, y mejorar "
   "el desempeño ambiental?",
   e="5.2")
_i(5, "Política (SST)",
   "¿La política de SST se compromete a proporcionar condiciones de trabajo seguras y "
   "saludables, eliminar peligros, reducir riesgos y a la consulta y participación de "
   "los trabajadores?",
   s="5.2")
_i(5, "Política: comunicación y disponibilidad",
   "¿La(s) política(s) está(n) documentada(s), es(son) apropiada(s) al contexto, está(n) "
   "comunicada(s) y entendida(s) dentro de la organización y disponible(s) para las "
   "partes interesadas?",
   q="5.2.2", e="5.2", s="5.2")
_i(5, "Roles, responsabilidades y autoridades",
   "¿Están asignadas y comunicadas las responsabilidades y autoridades para asegurar la "
   "conformidad del sistema, informar a la dirección sobre su desempeño y promover la "
   "mejora (incluyendo la responsabilidad de la dirección en SST)?",
   q="5.3", e="5.3", s="5.3")
_i(5, "Consulta y participación de los trabajadores",
   "¿Existen procesos para consultar y hacer participar a los trabajadores (y sus "
   "representantes) en la identificación de peligros, evaluación de riesgos, "
   "investigación de incidentes y definición de controles, eliminando barreras a la "
   "participación?",
   s="5.4")

# ---------------------------------------------------------------- Cláusula 6
_i(6, "Riesgos y oportunidades",
   "¿Se han determinado los riesgos y oportunidades vinculados al contexto, a las "
   "partes interesadas y al alcance, y se planifican acciones proporcionales para "
   "abordarlos y evaluar su eficacia?",
   q="6.1", e="6.1.1", s="6.1.1")
_i(6, "Aspectos ambientales",
   "¿Se identifican los aspectos ambientales de actividades, productos y servicios "
   "(considerando perspectiva de ciclo de vida), se evalúan sus impactos y se determinan "
   "los significativos? ¿Se mantiene la información documentada?",
   e="6.1.2")
_i(6, "Identificación de peligros",
   "¿Existe un proceso continuo y proactivo de identificación de peligros (rutinarios y "
   "no rutinarios, factores humanos, emergencias, contratistas, cambios)?",
   s="6.1.2.1")
_i(6, "Evaluación de riesgos y oportunidades SST",
   "¿Se evalúan los riesgos para la SST, otros riesgos del sistema y las oportunidades "
   "de mejora de la SST, con metodología y criterios definidos?",
   s="6.1.2.2")
_i(6, "Requisitos legales y otros requisitos",
   "¿Se identifican, tienen acceso y se mantienen actualizados los requisitos legales y "
   "otros requisitos aplicables a los aspectos ambientales y a los peligros de SST, "
   "determinando cómo aplican a la organización?",
   e="6.1.3", s="6.1.3")
_i(6, "Planificación de acciones",
   "¿Se planifican acciones para abordar riesgos, oportunidades, aspectos significativos "
   "y requisitos legales, y para prepararse ante emergencias, integrándolas en los "
   "procesos del sistema?",
   q="6.1.2", e="6.1.4", s="6.1.4")
_i(6, "Objetivos y planificación para lograrlos",
   "¿Hay objetivos medibles coherentes con la política, con responsables, recursos, "
   "plazos e indicadores, que se comunican y actualizan?",
   q="6.2", e="6.2", s="6.2")

# ---------------------------------------------------------------- Cláusula 7
_i(7, "Recursos",
   "¿Se determinan y proporcionan los recursos necesarios (personas, infraestructura, "
   "financieros) para establecer, implementar, mantener y mejorar el sistema?",
   q="7.1", e="7.1", s="7.1")
_i(7, "Infraestructura y ambiente de los procesos",
   "¿Se proporciona y mantiene la infraestructura y el ambiente necesarios para operar "
   "los procesos y lograr la conformidad de productos y servicios?",
   q="7.1.3 / 7.1.4")
_i(7, "Seguimiento y medición (equipos)",
   "¿Los equipos de seguimiento y medición están identificados, calibrados o verificados "
   "y se conservan los registros?",
   q="7.1.5", e="9.1.1", s="9.1.1")
_i(7, "Conocimientos de la organización",
   "¿Se determinan, mantienen y ponen a disposición los conocimientos necesarios para "
   "operar los procesos?",
   q="7.1.6")
_i(7, "Competencia",
   "¿Se determina la competencia necesaria (educación, formación, experiencia), se "
   "asegura mediante formación u otras acciones y se conservan evidencias?",
   q="7.2", e="7.2", s="7.2")
_i(7, "Toma de conciencia",
   "¿Las personas conocen la política, los objetivos, su contribución, las implicaciones "
   "de no cumplir y, según aplique, los aspectos ambientales significativos, peligros, "
   "riesgos y su derecho a retirarse de situaciones de peligro grave?",
   q="7.3", e="7.3", s="7.3")
_i(7, "Comunicación",
   "¿Hay un proceso de comunicación interna y externa (qué, cuándo, a quién, cómo y "
   "quién comunica), considerando requisitos legales y la diversidad de los receptores?",
   q="7.4", e="7.4", s="7.4")
_i(7, "Información documentada",
   "¿Se crea, actualiza y controla la información documentada (identificación, "
   "aprobación, distribución, acceso, conservación y disposición) requerida por las "
   "normas y por la organización?",
   q="7.5", e="7.5", s="7.5")

# ---------------------------------------------------------------- Cláusula 8
_i(8, "Planificación y control operacional",
   "¿Se planifican, implementan y controlan los procesos operativos con criterios "
   "definidos, controles ambientales y de SST, y se conserva la información documentada "
   "necesaria para confiar en que se ejecutan según lo planificado?",
   q="8.1", e="8.1", s="8.1.1")
_i(8, "Jerarquía de controles (SST)",
   "¿Se eliminan peligros y reducen riesgos aplicando la jerarquía de controles: "
   "eliminación, sustitución, controles de ingeniería, administrativos y EPP?",
   s="8.1.2")
_i(8, "Perspectiva de ciclo de vida",
   "¿Se controlan o influyen los aspectos ambientales en el diseño, compras, "
   "transporte, uso, tratamiento final y disposición, y se comunican los requisitos "
   "ambientales a proveedores y partes externas?",
   e="8.1")
_i(8, "Gestión del cambio",
   "¿Se planifican y controlan los cambios (procesos, instalaciones, productos, "
   "personal, legislación), evaluando sus consecuencias sobre calidad, ambiente y SST?",
   q="6.3 / 8.5.6", e="8.1", s="8.1.3")
_i(8, "Compras, contratistas y externalización",
   "¿Se controlan los procesos, productos y servicios suministrados externamente "
   "(evaluación y selección de proveedores, criterios, coordinación con contratistas, "
   "requisitos de calidad, ambientales y de SST)?",
   q="8.4", e="8.1", s="8.1.4")
_i(8, "Requisitos de productos y servicios",
   "¿Se determinan, revisan y comunican los requisitos del cliente y los legales antes "
   "de comprometerse a suministrar, y se gestionan los cambios en los requisitos?",
   q="8.2")
_i(8, "Diseño y desarrollo",
   "¿Existe control del diseño y desarrollo (planificación, entradas, controles, "
   "salidas y cambios), considerando aspectos de calidad, ambientales y de SST?",
   q="8.3", e="8.1")
_i(8, "Producción y provisión del servicio",
   "¿La producción y provisión del servicio se realizan en condiciones controladas "
   "(información, recursos, validación, prevención del error humano, seguimiento)?",
   q="8.5.1")
_i(8, "Identificación y trazabilidad",
   "¿Se identifican las salidas y el estado de seguimiento, y se asegura la "
   "trazabilidad cuando es un requisito?",
   q="8.5.2")
_i(8, "Propiedad del cliente o de proveedores externos",
   "¿Se cuida, protege y reporta la propiedad perteneciente a clientes o proveedores "
   "externos mientras esté bajo control de la organización?",
   q="8.5.3")
_i(8, "Preservación, posentrega y liberación",
   "¿Se preserva el producto, se atienden las actividades posteriores a la entrega y se "
   "verifica la conformidad antes de liberar productos y servicios?",
   q="8.5.4 / 8.5.5 / 8.6")
_i(8, "Salidas no conformes",
   "¿Se identifican y controlan las salidas no conformes, se corrigen, se segregan y se "
   "conservan registros de la acción tomada?",
   q="8.7")
_i(8, "Preparación y respuesta ante emergencias",
   "¿Se han identificado emergencias potenciales (incendio, derrame, accidente, etc.), "
   "existen planes de respuesta, formación, simulacros periódicos, comunicación con "
   "partes interesadas y revisión tras eventos reales?",
   e="8.2", s="8.2")

# ---------------------------------------------------------------- Cláusula 9
_i(9, "Seguimiento, medición, análisis y evaluación",
   "¿Se determina qué, cómo y cuándo medir y analizar (indicadores de calidad, ambiente "
   "y SST), y se conservan registros que permitan evaluar el desempeño y la eficacia?",
   q="9.1.1 / 9.1.3", e="9.1.1", s="9.1.1")
_i(9, "Satisfacción del cliente",
   "¿Se hace seguimiento de la percepción del cliente sobre el grado en que se cumplen "
   "sus necesidades y expectativas?",
   q="9.1.2")
_i(9, "Evaluación del cumplimiento legal",
   "¿Se evalúa periódicamente el cumplimiento de los requisitos legales y otros "
   "requisitos, se toman acciones y se conservan los resultados?",
   e="9.1.2", s="9.1.2")
_i(9, "Auditoría interna",
   "¿Existe un programa de auditorías internas con criterios, alcance, frecuencia, "
   "auditores imparciales, informes a la dirección y seguimiento de hallazgos?",
   q="9.2", e="9.2", s="9.2")
_i(9, "Revisión por la dirección",
   "¿La alta dirección revisa el sistema a intervalos planificados, considerando las "
   "entradas requeridas y dejando decisiones y acciones documentadas?",
   q="9.3", e="9.3", s="9.3")

# --------------------------------------------------------------- Cláusula 10
_i(10, "Generalidades de la mejora",
   "¿Se determinan y seleccionan oportunidades de mejora para cumplir requisitos, "
   "aumentar la satisfacción y mejorar el desempeño ambiental y de SST?",
   q="10.1", e="10.1", s="10.1")
_i(10, "No conformidad y acción correctiva",
   "¿Se reacciona ante no conformidades, se analizan sus causas, se implementan y "
   "revisan acciones correctivas y se conservan registros?",
   q="10.2", e="10.2", s="10.2")
_i(10, "Investigación de incidentes",
   "¿Se investigan los incidentes con participación de los trabajadores, determinando "
   "causas raíz, necesidad de acciones y comunicando resultados?",
   s="10.2")
_i(10, "Mejora continua",
   "¿Se mejora de forma continua la idoneidad, adecuación y eficacia del sistema, "
   "promoviendo una cultura que apoye el sistema y la participación de los "
   "trabajadores?",
   q="10.3", e="10.3", s="10.3")
