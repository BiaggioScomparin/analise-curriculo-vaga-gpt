import streamlit as st
import requests
import base64

st.set_page_config(page_title="Análise de Currículo x Vaga", layout="centered")

# Cabeçalho
st.title("📄 Análise de Currículo com Inteligência Artificial")
st.write("Faça upload do seu currículo (PDF) e cole o link da vaga para analisar a compatibilidade.")

# Upload do currículo
uploaded_file = st.file_uploader("📎 Currículo em PDF", type=["pdf"])

# Campo para link da vaga
job_link = st.text_input("🔗 Cole o link da vaga")

# Botão de envio
if uploaded_file and job_link:
    if st.button("🔍 Analisar"):
        try:
            # Codificação do currículo em base64
            file_bytes = uploaded_file.read()
            encoded_file = base64.b64encode(file_bytes).decode("utf-8")

            # Cabeçalho de autenticação (lido dos secrets do Streamlit)
            headers = {
                "Authorization": f"Bearer {st.secrets['openai']['api_key']}"
            }

            # Dados para envio à API
            data = {
                "model": "gpt-4-1106-preview",
                "messages": [
                    {"role": "system", "content": "Você é um avaliador de currículos e especialista em análise de compatibilidade com descrições de vagas."},
                    {"role": "user", "content": f"Compare o seguinte currículo com a vaga no link: {job_link}. Dê um JD Match (em %) e liste palavras-chave presentes e ausentes. Ofereça sugestões para melhorar a aderência."},
                    {"role": "user", "content": f"Currículo em base64:\n{encoded_file}"}
                ]
            }

            # Enviando a solicitação
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            analysis = result["choices"][0]["message"]["content"]

            # Exibição do resultado
            st.markdown("### ✅ Resultado da Análise")
            st.markdown(analysis)

        except requests.exceptions.HTTPError as e:
            st.error(f"Erro HTTP: {e.response.status_code} – {e.response.text}")
        except KeyError:
            st.error("🔑 Erro ao acessar a chave da OpenAI. Verifique seu arquivo `secrets.toml` ou configurações no Streamlit Cloud.")
        except Exception as e:
            st.error(f"⚠️ Erro inesperado: {str(e)}")
else:
    st.info("Por favor, carregue o currículo e informe o link da vaga para prosseguir.")

