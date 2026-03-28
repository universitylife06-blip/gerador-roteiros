import streamlit as st
import google.generativeai as genai
import time

# Configuração da página
st.set_page_config(page_title="Gerador de Roteiros Multi-idiomas", layout="wide")
st.title("🎬 Automação de Roteiros para o YouTube")

# Barra lateral para a chave da API
st.sidebar.header("Configurações")
api_key = st.sidebar.text_input("Insira sua API Key do Gemini:", type="password")
st.sidebar.markdown("*(Você pode gerar uma chave gratuita no Google AI Studio)*")

# Entrada do título original
titulo_original = st.text_input("Título original do vídeo (em português):")

# Áreas para você colar as suas diretrizes de prompt
st.markdown("### Seus Prompts de Geração")
st.info("Personalize as instruções abaixo. O aplicativo vai substituir automaticamente as tags `{titulo}`, `{premissa}` e `{idioma}` durante a execução.")

prompt_premissa_base = st.text_area(
    "Diretrizes do Prompt de Premissa:",
    "Atue como um produtor de conteúdo experiente. Com base no título '{titulo}', crie uma premissa intrigante e um resumo de 1 parágrafo para um vídeo do YouTube. Escreva o resultado em {idioma}."
)

prompt_roteiro_base = st.text_area(
    "Diretrizes do Prompt de Roteiro:",
    "Atue como um roteirista de YouTube de alta retenção. Usando a seguinte premissa: '{premissa}', crie um roteiro completo (Introdução, Desenvolvimento e Conclusão). Escreva todo o roteiro em {idioma}."
)

idiomas_alvo = [
    "Alemão", "Croata", "Espanhol", "Francês", "Holandês", 
    "Inglês", "Italiano", "Polonês", "Romeno", "Russo"
]

if st.button("🚀 Iniciar Automação"):
    if not api_key or not titulo_original:
        st.warning("Por favor, preencha a API Key e o Título original para começar.")
    else:
        # Configura a API com a chave fornecida
        genai.configure(api_key=api_key)
        # Usando o modelo flash por ser mais rápido e ideal para tarefas em lote
        model = genai.GenerativeModel('gemini-2.5-flash') 

        st.success("Iniciando a produção dos roteiros...")

        # Loop passando por todos os 10 idiomas
        for idioma in idiomas_alvo:
            st.markdown(f"## 🌍 Idioma: {idioma}")
            
            with st.spinner(f"Processando {idioma}..."):
                try:
                    # Passo 1: Traduzir o título
                    prompt_traducao = f"Traduza o seguinte título de vídeo para {idioma}. Responda APENAS com a tradução, sem aspas: {titulo_original}"
                    titulo_traduzido = model.generate_content(prompt_traducao).text.strip()
                    st.write(f"**Título:** {titulo_traduzido}")
                    time.sleep(1) # Pequena pausa para evitar sobrecarga na API

                    # Passo 2: Gerar a Premissa
                    prompt_premissa_final = prompt_premissa_base.format(titulo=titulo_traduzido, idioma=idioma)
                    premissa = model.generate_content(prompt_premissa_final).text.strip()
                    
                    with st.expander("Ver Premissa Gerada"):
                        st.write(premissa)
                    time.sleep(1)

                    # Passo 3: Gerar o Roteiro
                    prompt_roteiro_final = prompt_roteiro_base.format(premissa=premissa, idioma=idioma)
                    roteiro = model.generate_content(prompt_roteiro_final).text.strip()
                    
                    with st.expander("Ver Roteiro Completo", expanded=False):
                        st.write(roteiro)
                    
                except Exception as e:
                    st.error(f"Ocorreu um erro ao processar o {idioma}: {e}")
            
            st.divider()
