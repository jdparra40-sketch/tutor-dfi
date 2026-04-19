from flask import Flask, render_template, request, jsonify
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# ── Casos disponibles ────────────────────────────────────────────────────────

CASOS = {
    "caso1": {
        "id": "caso1",
        "titulo": "Caso 1",
        "nombre": "Aceite de oliva en vidrio con bomba dosificadora metálica",
        "emoji": "🫒",
        "resumen": "1.800 botellas 500ml con bomba de acero inox → Alemania. Empaque 100% sin plástico, trazabilidad, UV.",
        "contexto": """
PRODUCTO: Aceite de oliva virgen extra (líquido lipídico, no peligroso) en botella de
vidrio de 500 ml con cuello reforzado y bomba dispensadora de acero inoxidable para
uso culinario directo. Producto existente reformulado en nueva presentación.

ESTRATEGIA: Venta B2B a cadenas de restaurantes y tiendas gourmet.
"Eliminación de plásticos de un solo uso en canal HoReCa."

DESTINO: Restaurantes gourmet y tiendas especializadas en áreas metropolitanas de
Múnich y Frankfurt, Alemania. Clima portuario con HR promedio 75-85%. Infraestructura
con alta conectividad ferroviaria hacia el interior y estrictos controles de seguridad
alimentaria en aduana. El cliente exige entrega en plataformas de recepción con horario
restringido y documentación digital previa.

CANTIDAD: 1.800 unidades.

CARACTERÍSTICAS TÉCNICAS por unidad:
- Dimensiones: 8×8×28 cm
- Peso bruto: 580 g/unidad
- Sensible a luz UV (degrada el aceite)
- Sensible a golpes (vidrio)
- Sensible a inclinación prolongada >45° (fuga por la bomba)

EXIGENCIAS DEL CLIENTE:
- Garantía de cero fugas por vibración y movimiento marítimo
- Empaque secundario 100% libre de plástico y reciclable en circuito cerrado
- Trazabilidad obligatoria de lote y fecha de cosecha en el sistema del receptor
- Resistencia a apilamiento de 4 alturas en almacén sin climatización

RESTRICCIONES DE ESTIBA:
- Pallet EUR (1.200×800 mm)
- Altura máxima recomendada: 1,4 m
- Peso máximo por pallet: 900 kg

REGULACIÓN CLAVE:
- Unión Europea: Reglamento (UE) 29/2012 — etiquetado obligatorio de aceites de oliva
- Reglamento (CE) 178/2002: trazabilidad alimentaria obligatoria en toda la cadena
- Reglamento (UE) 1169/2011: información alimentaria al consumidor (etiqueta en alemán)
- RASFF (Sistema de Alerta Rápida de la UE): controles estrictos en aduana para alimentos
- Empaque: Directiva UE de envases y residuos — el cliente exige empaque 100% sin plástico
- TLC Colombia-UE (vigente desde 2013): arancel preferencial con certificado de origen EUR.1
- HS Code Colombia: 1509.10 (aceite de oliva virgen)
- Aduana Alemania: ATLAS (sistema electrónico aduanal); documentación digital previa obligatoria
"""
    },
    "caso2": {
        "id": "caso2",
        "titulo": "Caso 2",
        "nombre": "Cápsulas de café compostables para estaciones corporativas",
        "emoji": "☕",
        "resumen": "45.000 cápsulas compostables (celulosa + válvula desgasificación) → Los Ángeles y San Francisco. Sin poliestireno.",
        "contexto": """
PRODUCTO: Café torrefacto molido (sólido orgánico) en cápsulas de 12g con barrera de
celulosa activada y válvula de desgasificación. Producto existente reformulado.
Presentación individual, 100% compostable.

ESTRATEGIA: Venta corporativa con modelo de reposición mensual.
"Huella de carbono cero y frescura garantizada."

DESTINO: Oficinas corporativas y espacios de coworking en área metropolitana de
Los Ángeles y San Francisco, EE.UU. Clima portuario seco pero con picos de temperatura
en patio (>35°C). Alta rotación de contenedores y estrictos controles fitosanitarios
para productos orgánicos. El cliente requiere entrega en edificios con acceso restringido
y ventanas de recepción de 2 horas.

CANTIDAD: 45.000 unidades (presentación individual).

CARACTERÍSTICAS TÉCNICAS por cápsula:
- Dimensiones: 6×6×3 cm
- Peso: 12 g/unidad
- Sensible a humedad >60% HR
- Sensible a calor >40°C
- Sensible a compresión prolongada
- La válvula de desgasificación libera CO₂ post-tostión — el empaque debe permitir
  la salida de gas sin dejar entrar oxígeno

EXIGENCIAS DEL CLIENTE:
- Validación de control de O₂ residual en el empaque secundario
- Caja secundaria capaz de soportar 3 niveles de pallet en tránsito sin colapso
- Sistema de codificación con trazabilidad de lote, fecha de tueste y vencimiento,
  más código de venta al detalle
- PROHIBIDO uso de poliestireno o films no compostables en el empaque terciario

RESTRICCIONES DE ESTIBA:
- Pallet estándar (1.219×1.016 mm) — equivalente al pallet GMA norteamericano
- Altura máxima recomendada: 1,3 m
- Peso máximo por pallet: 700 kg

REGULACIÓN CLAVE:
- FDA EE.UU.: Food Safety Modernization Act (FSMA) — controles para alimentos importados;
  el importador debe estar registrado en FDA
- USDA: controles fitosanitarios para productos orgánicos certificados
- CBP (Customs and Border Protection): Prior Notice obligatorio para alimentos 2-5 días antes
- Etiqueta en inglés obligatoria con información nutricional (Nutrition Facts)
- TLC Colombia-EE.UU. (CTPA, vigente 2012): café con certificado de origen puede
  ingresar con arancel preferencial
- Compostabilidad: certificación ASTM D6400 o equivalente para empaques compostables en EE.UU.
- HS Code Colombia: 0901.21 (café tostado sin descafeinar) o 2101 si es extracto
"""
    },
    "caso3": {
        "id": "caso3",
        "titulo": "Caso 3",
        "nombre": "Alimento seco para mascotas en pouches al vacío planos",
        "emoji": "🐾",
        "resumen": "3.200 pouches al vacío de 2kg → Ámsterdam y Róterdam. Anti-perforación, trazabilidad, 4 alturas de pallet.",
        "contexto": """
PRODUCTO: Croquetas para perros adultos (proteína vegetal/animal, bajo contenido húmedo)
en pouches de 2 kg con sellado térmico y forma aplanada. Producto existente reformulado.
Estrategia de reducción de volumen unitario en 40% vs bolsa tradicional.

ESTRATEGIA: Venta a suscriptores urbanos y distribución masiva.
"Ahorro de espacio en hogar y transporte."

DESTINO: Tiendas de mascotas y centros de cumplimiento de suscripciones en área de
Ámsterdam y Róterdam, Países Bajos. El cliente recibe entregas en viviendas con espacio
limitado y exige empaques compactos y fáciles de almacenar.

CANTIDAD: 3.200 unidades.

CARACTERÍSTICAS TÉCNICAS por pouch:
- Dimensiones: 30×20×4 cm
- Peso: 2 kg/unidad
- Sensible a puncturas (sellado al vacío — una perforación = pérdida del vacío = oxidación)
- Sensible a humedad >65% HR
- Sensible a compresión lateral

EXIGENCIAS DEL CLIENTE:
- Pouches a prueba de perforación por esquinas de cajas adyacentes
- Caja secundaria que permita inspección visual rápida sin romper sello primario
- Sistema de codificación con trazabilidad de fecha de vencimiento, lote y peso neto
- Resistencia a 4 alturas de pallet durante 21 días sin deformación estructural

RESTRICCIONES DE ESTIBA:
- Pallet EUR (1.200×800 mm)
- Altura máxima recomendada: 1,6 m
- Peso máximo por pallet: 1.000 kg

REGULACIÓN CLAVE:
- UE — Reglamento (CE) 767/2009: etiquetado de alimentos para animales de compañía
  (obligatorio en neerlandés para mercado holandés)
- UE — Reglamento (CE) 1069/2009: productos de origen animal — requisitos sanitarios
  para subproductos animales en alimentos para mascotas
- NVWA (Nederlandse Voedsel en Warenautoriteit): autoridad holandesa de seguridad
  alimentaria, realiza inspecciones en importación
- TLC Colombia-UE (vigente 2013): arancel preferencial con certificado de origen EUR.1
- Puerto de Róterdam: mayor puerto de Europa, hub logístico principal para distribución
  intra-europea; aduana eficiente con sistema ICS2 (Import Control System 2)
- HS Code Colombia: 2309.10 (alimentos para perros o gatos, acondicionados para la venta al por menor)
"""
    },
    "caso4": {
        "id": "caso4",
        "titulo": "Caso 4",
        "nombre": "Cerveza artesanal en lata de 1L con tapa reutilizable",
        "emoji": "🍺",
        "resumen": "2.500 latas de 1L IPA 5,2% (lata aluminio + tapa rosca polímero) → Chile. Sector outdoor, glamping, festivales.",
        "contexto": """
PRODUCTO: Cerveza tipo IPA (India Pale Ale), estilo Ale de alta fermentación,
5,2% Alc/Vol., líquido carbonatado, en lata de aluminio de 1L con tapa rosca
de polímero alimentario reutilizable. Producto existente reformulado.

ESTRATEGIA: Distribución a sector outdoor, glamping y festivales.
"Bebida compartible sin desperdicio." Enfoque en resistencia a transporte rudo
y experiencia de usuario.

DESTINO: Centros de recreación al aire libre, sitios de glamping y organizadores
de festivales en valles andinos y zonas costeras de Chile. Clima portuario costero
húmedo. Restricciones locales para manejo de carga líquida en tránsito y necesidad
de ventilación adecuada en almacenamiento previo a distribución terrestre.
El cliente opera en ubicaciones remotas con acceso vehicular limitado y exige
empaques resistentes a manipulación manual intensiva.

CANTIDAD: 2.500 unidades.

CARACTERÍSTICAS TÉCNICAS por lata:
- Dimensiones: 10×10×22 cm
- Peso: 1,05 kg/unidad
- Sensible a golpes laterales (la lata puede abollar y perder el sello)
- Sensible a calor >30°C (aceleración de la fermentación residual)
- Sensible a congelación (expansión del líquido — ruptura de la lata)
- Líquido carbonatado: presión interna — no comprimir

EXIGENCIAS DEL CLIENTE:
- Caja secundaria con refuerzo anti-abolladura en esquinas
- Pictogramas de manejo claros y advertencias de conservación
- Sistema de trazabilidad para registro de fermentación, lote y control de
  reutilización de tapa

RESTRICCIONES DE ESTIBA:
- Pallet estándar (1.200×1.000 mm)
- Altura máxima recomendada: 1,4 m
- Peso máximo por pallet: 950 kg

REGULACIÓN CLAVE:
- Chile — SAG (Servicio Agrícola y Ganadero): controles fitosanitarios en importación
- Chile — SNA / Aduana: bebidas alcohólicas deben cumplir Ley 19.925 (Ley del Alcoholismo)
  y Decreto Supremo 78 sobre etiquetado de bebidas alcohólicas
- Etiqueta en español con: graduación alcohólica, contenido neto, país de origen,
  importador chileno, leyenda "Beber con moderación. Prohibida la venta a menores de 18 años"
- ¿Es mercancía peligrosa?: Cerveza 5,2% Alc/Vol. — el alcohol etílico diluido en
  concentraciones menores a 24% generalmente NO clasifica como mercancía peligrosa
  bajo el Código IMDG. Verificar con el transportista.
- Acuerdo de Libre Comercio Colombia-Chile (vigente 2009): arancel 0% para la mayoría
  de productos colombianos con certificado de origen
- Aduana Chile: Sistema SICEX para declaraciones electrónicas; DUS (Documento Único
  de Salida) desde Colombia
- HS Code Colombia: 2203.00 (cerveza de malta)
- Ruta marítima: Colombia (Buenaventura o Cartagena) → Canal de Panamá → Puerto de
  San Antonio o Valparaíso (Chile). Tránsito ~15-20 días.
"""
    },
    "caso5": {
        "id": "caso5",
        "titulo": "Caso 5",
        "nombre": "Detergente en polvo pre-dosificado en película hidrosoluble",
        "emoji": "🧴",
        "resumen": "15.000 pods PVOH (sensibles a humedad y compresión) → Bangkok y resorts de Tailandia.",
        "contexto": """
PRODUCTO: Detergente industrial para lavandería (surfactantes aniónicos, pH neutro) en pods
de 30g envueltos en película PVOH (alcohol polivinílico) hidrosoluble, dentro de caja dispensadora.

ESTRATEGIA: Venta institucional a cadenas hoteleras. "Cero manejo de polvo, precisión de dosis,
seguridad laboral."

DESTINO: Bangkok, Phuket y Krabi, Tailandia. Clima tropical, HR ambiental 75-85%, lluvias
frecuentes. Manipulación intensiva con equipos móviles y requisitos de desarmado rápido de
empaque terciario para verificaciones sanitarias. Bodegas hoteleras con control de humedad
limitado, personal con capacitación básica en logística.

CANTIDAD: 15.000 unidades.

CARACTERÍSTICAS TÉCNICAS por pod:
- Dimensiones: 8×8×5 cm, peso: 30 g
- Sensible a humedad: >50% HR disuelve la película PVOH
- Sensible a compresión: >200 kg/m² daña el pod
- La película PVOH se disuelve en contacto directo con agua a >15°C

EXIGENCIAS DEL CLIENTE:
- Cero fugas o desintegración por vibración durante tránsito marítimo
- Caja dispensadora con perforaciones pre-cortadas y refuerzo estructural
- Pictografía de manejo, conservación y advertencias de integridad
- Trazabilidad de lote

RESTRICCIONES DE ESTIBA:
- Pallet estándar: 1.100×1.100 mm
- Altura máxima recomendada: 1,2 m
- Peso máximo por pallet: 650 kg

REGULACIÓN CLAVE:
- Tailandia: Hazardous Substance Act B.E. 2535 — surfactantes aniónicos deben declararse ante DIW
- Etiqueta en tailandés obligatoria (nombre, ingredientes, fabricante, importador, país de origen)
- No existe TLC Colombia-Tailandia → arancel NMF ~10% + VAT 7%
- Verificar SGP tailandés: posible certificado de origen Forma A para reducción arancelaria
- HS Code Colombia: 3402.20 (preparaciones tensoactivas acondicionadas para venta al por menor)
- Producto NO es mercancía peligrosa IMDG en su concentración de uso (surfactante pH neutro)
"""
    }
}


# ── Prompt base del tutor (se completa con el contexto del caso) ─────────────

def build_system_prompt(caso):
    return f"""
Eres un tutor experto en Distribución Física Internacional (DFI) y transporte internacional,
diseñado para acompañar a estudiantes de la Especialización en Gerencia Logística de la
Universidad de la Sabana.

El alumno está trabajando el {caso['titulo']}: "{caso['nombre']}".

## FILOSOFÍA PEDAGÓGICA

No existe una única solución correcta. En logística real, múltiples decisiones pueden ser
válidas siempre que sean técnicamente factibles, económicamente razonables y cumplan
la normativa aplicable. Tu rol es ayudar al alumno a explorar el espacio de soluciones
posibles, no guiarlo hacia una respuesta predeterminada.

Actúas como tutor socrático y consultor logístico: haces preguntas, cuestionas supuestos,
señalas consecuencias de cada decisión y abres nuevas perspectivas.
Si una propuesta es válida pero diferente a lo convencional, reconócela explícitamente.

## CRITERIOS DE EVALUACIÓN

Evalúa cada propuesta del alumno contra tres criterios:

1. FACTIBILIDAD TÉCNICA: ¿Respeta las restricciones físicas y técnicas del producto?
2. CUMPLIMIENTO NORMATIVO: ¿Cumple la regulación del país de exportación (Colombia),
   tránsito y destino? ¿Aplica correctamente los acuerdos comerciales vigentes?
3. COHERENCIA ESTRATÉGICA: ¿Es coherente con la estrategia comercial, el canal,
   el cliente final y el contexto logístico del caso?

## COMPORTAMIENTO EN LA CONVERSACIÓN

- Propuesta VIABLE: valídala, explica por qué funciona, pregunta si consideró alternativas.
- Propuesta VIABLE CON RIESGOS: señala los riesgos específicos, pregunta cómo los mitigaría.
- Propuesta NO VIABLE: no la rechaces directamente. Haz una pregunta que lleve al alumno
  a descubrir el problema por sí mismo.
- Propuesta INUSUAL PERO VÁLIDA: reconócela explícitamente. La creatividad logística
  bien fundamentada es bienvenida.
- Cuando el alumno escriba "resumen final": entrega una síntesis de sus decisiones,
  qué las hace viables o cuestionables y qué variables adicionales podría explorar.
- Responde siempre en español.

## CONTEXTO DEL CASO

{caso['contexto']}

## INICIO DE SESIÓN

Al comenzar, preséntate así:
"Hola, estás trabajando el {caso['titulo']}: {caso['nombre']}. Mi rol no es decirte cuál
es la respuesta correcta — en logística real, varias soluciones pueden funcionar. Vamos a
explorar tus propuestas juntos: te haré las preguntas difíciles para que evalúes si tu
solución es técnicamente factible, cumple la normativa y es coherente con la estrategia
del negocio. ¿Por dónde quieres empezar?"
"""


# ── Rutas ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/casos", methods=["GET"])
def get_casos():
    lista = [
        {
            "id": c["id"],
            "titulo": c["titulo"],
            "nombre": c["nombre"],
            "emoji": c["emoji"],
            "resumen": c["resumen"],
        }
        for c in CASOS.values()
    ]
    return jsonify(lista)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])
    caso_id = data.get("caso_id", "caso5")

    caso = CASOS.get(caso_id, CASOS["caso5"])
    system_prompt = build_system_prompt(caso)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=system_prompt,
        messages=messages,
    )

    return jsonify({"response": response.content[0].text})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print("Tutor DFI — Universidad de la Sabana")
    print("Casos disponibles:", len(CASOS))
    print(f"Abre tu navegador en: http://localhost:{port}")
    app.run(debug=False, host="0.0.0.0", port=port)
