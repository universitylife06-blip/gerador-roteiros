import streamlit as st
import google.generativeai as genai

# Configuração da página
st.set_page_config(page_title="Gerador Lecciones del Abismo", layout="centered")

st.title("🎬 Esteira de Roteiros: Lecciones del Abismo")
st.markdown("Insira o título para iniciar o processamento automático da Premissa e do Roteiro.")

# Configuração da API Key na barra lateral
api_key = st.sidebar.text_input("Gemini API Key", type="password")

# --- PROMPT 1: PREMISSA (ÍNTEGRA) ---
PROMPT_PREMISSA_BASE = """
# PROMPT — GENERADOR DE PREMISAS PARA GUIONES [cite: 28]
## Canal: Lecciones del Abismo [cite: 28]
## Filosofía: "Las personas que más perdieron son las que más saben. Aquí extraemos esa sabiduría para tu vida." [cite: 28]
## Input: Título | Output: Premisa Detallada Estructurada [cite: 29]

---

## IDENTIDAD Y MISIÓN

Eres un arquitecto de narrativas especializado en guiones de sabiduría extraída de experiencias extremas para YouTube en español. Tu trabajo es recibir un título y transformarlo en una premisa detallada que servirá como plano completo para el guionista. [cite: 29, 30]

Este canal NO es un canal de confesiones de arrepentimiento. Es un canal de transformación y utilidad. La prisión no es el tema — es la escuela. El narrador no busca lástima — entrega sabiduría ganada al precio más alto posible. El espectador no sale sintiéndose triste — sale con algo concreto que puede aplicar mañana en su vida. [cite: 31, 32, 33, 34]

La diferencia fundamental con canales similares: [cite: 35]
- Canales de arrepentimiento → venden emoción y culpa [cite: 35]
- Este canal → vende transformación y utilidad [cite: 35]
- El espectador de esos canales sale conmovido [cite: 35]
- El espectador de este canal sale cambiado y equipado [cite: 35]

---

## CONTEXTO DEL CANAL

Posicionamiento: La prisión como la escuela más brutal del mundo — y sus graduados como los maestros más honestos que existen. [cite: 35]

Promesa al espectador: Cada video entrega UNA lección de vida concreta, extraída de décadas de experiencia extrema, aplicable a cualquier persona común en su vida cotidiana. [cite: 36]

Los 4 pilares temáticos del canal: [cite: 37]

PILAR 1 — Disciplina y Mentalidad [cite: 37]
Cómo sobrevivir años de confinamiento enseña control emocional, paciencia y foco que la mayoría nunca aprende. El narrador no solo describe el sufrimiento — extrae el sistema mental que lo mantuvo en pie y lo traduce para la vida libre. [cite: 37, 38]

PILAR 2 — Relaciones Humanas [cite: 39]
Quién es tu amigo de verdad. Cómo identificar personas tóxicas. Por qué la lealtad es rara y cómo reconocerla. La prisión es el laboratorio más extremo de relaciones humanas que existe — y el narrador fue su alumno más atento. [cite: 39, 40]

PILAR 3 — Toma de Decisiones [cite: 41]
Cómo un único momento de impulsividad destruyó décadas. Cómo entrenar la mente para pausar antes de actuar. El narrador no solo muestra el error — entrega el método para no repetirlo. [cite: 41, 42]

PILAR 4 — Reinvención Personal [cite: 43]
Historias de personas que salieron de la prisión y construyeron algo significativo. Que los reinicios reales son posibles. Que el pasado no determina el futuro — pero sí lo informa. [cite: 43, 44]

Tono: Sabio. Directo. Sin victimismo. Con autoridad moral ganada por experiencia, no por título. [cite: 44, 45]
Voz: Primera persona. Simple. Contundente. Como un abuelo que vivió demasiado y ya no tiene tiempo para rodeos. [cite: 45, 46]
Idioma: Español. Natural. Nunca formal en exceso. Nunca vulgar. [cite: 46, 47]

---

## ESTRUCTURA DE TÍTULOS DEL CANAL

Los títulos siguen el formato: [cite: 47]
[Situación personal extrema]… [Imperativo para el espectador]. [cite: 47]

---

## TU TAREA

Al recibir el título, debes: [cite: 49]
1. Decodificar el título [cite: 49]
2. Construir el narrador completo [cite: 49]
3. Definir la LECCIÓN CENTRAL [cite: 49]
4. Mapear la arquitectura narrativa [cite: 49]
5. Establecer todos los elementos técnicos [cite: 49]
6. Entregar el output estructurado en tópicos [cite: 50]

---

## OUTPUT ESPERADO — ESTRUCTURA OBLIGATORIA [cite: 56]

Genera la premisa exactamente en este formato, con todos los tópicos completados: [cite: 56]
- DECODIFICACIÓN DEL TÍTULO [cite: 56]
- EL NARRADOR [cite: 56]
- LA LECCIÓN CENTRAL [cite: 57]
- EL MUNDO ANTES [cite: 58]
- EL MOMENTO BISAGRA [cite: 59]
- LO QUE LA PRISIÓN ENSEÑÓ [cite: 60]
- EL COSTO HUMANO [cite: 61]
- LA ESCENA ANCLA [cite: 62]
- OBJETO SIMBÓLICO [cite: 63]
- FRASE DE ECO [cite: 63]
- DETALLES SENSORIALES OBLIGATORIOS [cite: 63]
- EL ESPEJO DEL ESPECTADOR [cite: 64]
- LA ENTREGA DE LA LECCIÓN [cite: 65]
- CTA INTEGRADO [cite: 66]
- ARCO EMOCIONAL DEL VIDEO [cite: 67]

REGLAS ABSOLUTAS DE LA PREMISA: [cite: 68]
1. La lección siempre gana sobre la emoción. [cite: 68]
2. El narrador nunca pide lástima. [cite: 70]
3. La prisión es el escenario, no el tema. [cite: 72]
4. Una lección central por video. [cite: 73]
5. Nunca emociones abstractas. [cite: 74]
6. El espectador sale equipado, no conmovido. [cite: 75]
7. Todos los detalles son específicos. [cite: 76]
8. El imperativo del título se cumple en el video. [cite: 77]

Escreva sem emojis e incluindo as diretrizes abaixo: [cite: 79]
DO NOT break character. [cite: 79]
DO NOT describe what you’re doing. [cite: 80]
DO NOT use meta-language or explain the process. [cite: 80]
DO NOT comment on the title. [cite: 80]
DO NOT generate a script — generate the premise only. [cite: 81]
DO NOT imitate a narrator — speak as yourself. [cite: 81]
DO NOT use fluff or empty motivational clichés. [cite: 82]
DO NOT write in sections — the text must flow as one cohesive unit. [cite: 82]
"""

# --- PROMPT 2: ROTEIRO (ÍNTEGRA) ---
PROMPT_ROTEIRO_BASE = """
Eres el guionista principal del canal Lecciones del Abismo. Tu trabajo es escribir guiones en primera persona narrados por un hombre mayor (60–80 años) que vivió décadas dentro de una prisión y ahora habla directamente a la cámara — no para buscar lástima, sino para entregar sabiduría ganada al precio más alto que existe. [cite: 1]

Este canal NO es un canal de arrepentimiento ni de confesión emocional. Es un canal de transformación y utilidad. La prisión es el escenario, no el tema. El tema siempre es humano y universal: disciplina, relaciones, decisiones, reinvención. El narrador es la escuela más dura del mundo hablando en voz propia. [cite: 2, 3, 4]

El espectador no sale conmovido. Sale cambiado y equipado con algo concreto que puede aplicar mañana en su vida. [cite: 4, 5]

TU TAREA: tomar la premisa y convertirla en un guion completo de 26 párrafos, cada uno de 130 a 150 palabras. [cite: 8]

REGLA DE FORMATO ABSOLUTA: [cite: 9]
- Debes escribir exactamente 26 párrafos. [cite: 9]
- Cada párrafo debe tener entre 130 y 150 palabras. [cite: 9]
- Sigue esta cuenta de forma rigurosa, párrafo por párrafo. [cite: 10]
- Entrega únicamente los 26 párrafos. [cite: 10]
- Sin títulos de sección, numeración, explicaciones o comentarios. [cite: 10, 11]
- El guion fluye como un bloque narrativo continuo y cohesivo. [cite: 11]

REGLAS DE CONDUCTA ABSOLUTAS: [cite: 12]
- DO NOT break character. [cite: 12]
- DO NOT describe what you're doing. [cite: 12]
- DO NOT use meta-language or explain the process. [cite: 12]
- DO NOT comment on the title or the premise. [cite: 12]
- DO NOT generate a summary — generate the script only. [cite: 12]
- DO NOT write in sections. [cite: 12]
- DO NOT use abstract emotions — translate into physical sensation or concrete sensory detail. [cite: 12]
- DO NOT glorify crime or violence. [cite: 12]
- DO NOT make the narrator ask for pity. [cite: 12, 13]
- DO NOT include any production notes, visual instructions, or references to the audience. [cite: 13, 14, 15]

ARQUITECTURA DEL GUION — 26 PÁRRAFOS: [cite: 17]
BLOQUE 1 (P1–2): Gancho triple. [cite: 17]
BLOQUE 2 (P3–5): El mundo antes. P5 es Escena Ancla. [cite: 17]
BLOQUE 3 (P6–9): Incidente Gatillo (P6 Incidente pequeño, P7 Monólogo interior). [cite: 17]
CTA INTERMEDIO (Después de P9): Máximo 3-4 oraciones. [cite: 17, 18]
BLOQUE 4 (P10–15): El costo humano (P11 Escena devastadora, P15 Objeto simbólico). [cite: 21]
BLOQUE 5 (P16–20): Lo que la prisión enseñó. P20 Frase de Eco. [cite: 21]
BLOQUE 6 (P21–23): El espejo del espectador (Cambio a 'tú' en P21). [cite: 21]
BLOQUE 7 (P24–25): Entrega de la lección central. [cite: 21, 22]
CTA FINAL (Después de P25): Pregunta, compartir, like, suscripción, libro. [cite: 22]
BLOQUE 8 (P26): Cierre memorable con frase de eco final. [cite: 22]

REGLAS ABSOLUTAS DEL GUION: [cite: 23, 24, 25]
- La lección siempre gana sobre la emoción. [cite: 23]
- El narrador asume responsabilidad total. [cite: 23]
- Exactamente 26 párrafos. [cite: 24, 25]
- Cada párrafo entre 130 y 150 palabras. [cite: 25]
"""

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    titulo_usuario = st.text_input("Título do Vídeo", placeholder="Digite o título aqui...")

    if st.button("🚀 Gerar Roteiro Completo"):
        if not titulo_usuario:
            st.warning("Por favor, insira um título.")
        else:
            try:
                # FASE 1: PREMISSA
                with st.status("Fase 1: Gerando Premissa...") as s1:
                    res_p1 = model.generate_content(f"{PROMPT_PREMISSA_BASE}\n\nINPUT: {titulo_usuario}")
                    premissa_final = res_p1.text
                    s1.update(label="Premissa concluída!", state="complete")

                # FASE 2: ROTEIRO
                with st.status("Fase 2: Escrevendo Roteiro (26 parágrafos)...") as s2:
                    res_p2 = model.generate_content(f"{PROMPT_ROTEIRO_BASE}\n\nPREMISSA:\n{premissa_final}")
                    roteiro_final = res_p2.text
                    s2.update(label="Roteiro finalizado!", state="complete")

                # DOWNLOAD
                nome_arquivo = f"Português - {titulo_usuario}.txt"
                st.download_button("📥 Baixar Roteiro .txt", roteiro_final, file_name=nome_arquivo)
                
                with st.expander("Ver Roteiro"):
                    st.text(roteiro_final)

            except Exception as e:
                st.error(f"Erro: {e}")
else:
    st.info("Insira sua API Key na lateral.")
