# Versão Web (Streamlit) — Erick Alves

Esta pasta contém a versão web do seu chatbot. Ela lê um CSV com colunas `pergunta,resposta`, faz correspondência por similaridade (TF-IDF + cosseno) e roda em Streamlit.

## Como rodar localmente
```bash
cd web
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Acesse: http://localhost:8501

## Deploy no Streamlit Cloud
1. Faça login em https://share.streamlit.io/ com sua conta GitHub;
2. Crie um app selecionando este repositório;
3. Defina o caminho do app como `web/app.py`;
4. Adicione o arquivo `web/requirements.txt` nas dependências.

## Estrutura
```
web/
├─ app.py               # app Streamlit
├─ requirements.txt     # dependências mínimas
└─ data/
   └─ faq.csv           # base de exemplo (você pode trocar)
```

## Observações
- Projeto pessoal, sem vínculo com empresas.
- Autor: **Erick Alves**
- Se quiser evoluir, podemos adicionar intents, APIs, ou modelos de linguagem.
