import streamlit as st
import google.generativeai as genai

# Configuração da página
st.set_page_config(page_title="Gerador Multi-Idioma - Lecciones del Abismo", layout="centered")

st.title("🎬 Esteira de Roteiros Multi-Idioma")
st.markdown("Gere roteiros profissionais em 10 idiomas seguindo a arquitetura de 26 parágrafos.")

# Configuração da API Key na barra lateral
api_key = st.sidebar.text_input("Gemini API Key", type="password")

# Seleção de Idioma
idiomas_dict = {
    "Alemão": "German",
    "Croata": "Croatian",
    "Espanhol": "Spanish",
    "Francês": "French",
    "Holandês": "Dutch",
    "Inglês": "English",
    "Italiano": "Italian",
    "Polonês": "Polish",
    "Romeno": "Romanian",
    "Russo": "Russian"
}
idioma_selecionado = st.selectbox("Selecione o idioma do roteiro final:", list(idiomas_dict.keys()))

# Inicializa o estado para não perder o roteiro ao clicar em baixar
if 'roteiro_final' not in st.session_state:
    st.session_state.roteiro_final = None

# --- PROMPT 1: PREMISSA (ÍNTEGRA) ---
PROMPT_PREMISSA_BASE = """
# PROMPT — GENERADOR DE PREMISAS PARA GUIONES
## Canal: Lecciones del Abismo
## Filosofía: "Las personas que más perdieron son las que más saben. Aquí extraemos esa sabiduría para tu vida."
## IDENTIDAD Y MISIÓN
Eres un arquitecto de narrativas especializado en guiones de sabiduría extraída de experiencias extremas para YouTube en español. Tu trabajo es recibir un título y transformarlo en una premisa detallada que servirá como plano completo para el guionista.
Este canal NO es un canal de confesiones de arrepentimiento. Es un canal de transformación y utilidad. La prisión no es el tema — es la escuela. El narrador no busca lástima — entrega sabiduría ganada al precio más alto posible.
REGLAS: DO NOT break character. DO NOT describe what you’re doing. DO NOT generate a script — generate the premise only.
"""

# --- PROMPT 2: ROTEIRO (ÍNTEGRA) ---
PROMPT_ROTEIRO_BASE = """
Eres el guionista principal del canal Lecciones del Abismo. Tu trabajo es escribir guiones en primera persona narrados por un hombre mayor (60–80 años) que vivió décadas dentro de una prisión y ahora habla directamente a la cámara — no para buscar lástima, sino para entregar sabiduría ganada al precio más alto que existe.

TU TAREA: tomar la premisa y convertirla en un guion completo de 26 párrafos, cada uno de 130 a 150 palabras.

REGLA DE FORMATO ABSOLUTA:
- Debes escribir exactamente 26 párrafos.
- Cada párrafo debe tener entre 130 y 150 palabras.
- Sigue esta cuenta de forma rigurosa, párrafo por párrafo.
- Entrega únicamente los 26 párrafos.
- Sin títulos de sección, numeración, explicaciones o comentarios.
- El guion fluye como un bloque narrativo continuo y cohesivo.

REGLAS DE CONDUCTA:
- DO NOT break character.
- DO NOT generate a summary — generate the script only.
- DO NOT include any production notes.
"""

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

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

                # FASE 2: ROTEIRO (COM TRADUÇÃO)
                target_lang = idiomas_dict[idioma_selecionado]
                with st.status(f"Fase 2: Escrevendo Roteiro em {idioma_selecionado}...") as s2:
                    instrucao_idioma = f"\n\nCRITICAL: Write the entire script in {target_lang}."
                    res_p2 = model.generate_content(f"{PROMPT_ROTEIRO_BASE}{instrucao_idioma}\n\nPREMISSA:\n{premissa_final}")
                    st.session_state.roteiro_final = res_p2.text
                    s2.update(label=f"Roteiro em {idioma_selecionado} finalizado!", state="complete")

                st.success("Processo concluído!")

            except Exception as e:
                st.error(f"Erro na API: {e}")

# Exibição e Download
if st.session_state.roteiro_final:
    nome_arq = f"{idioma_selecionado.upper()} - {titulo_usuario[:50]}.txt"
    st.download_button("📥 Baixar Roteiro .txt", st.session_state.roteiro_final, file_name=nome_arq)
    
    with st.expander("Visualizar Texto"):
        st.text_area("Roteiro Final", value=st.session_state.roteiro_final, height=400)
else:
    st.info("Selecione o idioma, insira o título e clique no botão para começar.")
