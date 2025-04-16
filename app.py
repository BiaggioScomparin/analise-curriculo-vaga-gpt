import streamlit as st
import requests
import base64

st.set_page_config(page_title="Análise de Vaga e Currículo", layout="centered")

st.title("📄 Análise de Compatibilidade de Currículo com Vaga")
st.write("Carregue seu currículo em PDF e cole o link da vaga para receber um relatório de compatibilidade gerado com inteligência artificial (GPT-4).")

uploaded_file = st.file_uploader("📎 Upload do currículo (PDF)", type=["pdf"])
job_link = st.text_input("🔗 Link da vaga (ex: LinkedIn, Gupy, etc.)")

if uploaded_file and job_link:
    if st.button("🔍 Analisar Currículo"):
        st.info("Processando sua análise... Isso pode levar alguns segundos.")
        
        # Codifica o PDF em base64
        file_bytes = uploaded_file.read()
        encoded_file = base64.b64encode(file_bytes).decode("utf-8")

        # Prepara os dados para envio à API
        headers = {
            "Authorization": f"Bearer {st.secrets['openai']['api_key']}"
        }

        data = {
            "model": "gpt-4-1106-preview",
            "messages": [
                {"role": "system", "content": "Você é um avaliador de currículos experiente com foco em análise de compatibilidade com vagas de tecnologia e projetos."},
                {"role": "user", "content": f"Analise o seguinte currículo (em base64) e compare com a vaga neste link: {job_link}. Gere um JD Match em %, destaque palavras-chave compatíveis, as que faltam e sugestões de melhoria."},
                {"role": "user", "content": f"Currículo base64:\n{encoded_file}"}
            ]
        }

        # Requisição à API OpenAI
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            st.markdown("### ✅ Resultado da Análise")
            st.markdown(result["choices"][0]["message"]["content"])
        else:
            st.error("Erro ao processar a solicitação. Verifique seu token da OpenAI.")
