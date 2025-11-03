# Versão Web (Streamlit) — Erick Alves

Este diretório contém a versão web do seu chatbot.

## Executar localmente
```bash
cd web
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (Streamlit Cloud)
- Repo: `Duniinjja/chatbot-01`
- Branch: `main`
- App: `web/app.py`

## Estrutura
```
web/
├─ app.py
├─ requirements.txt
└─ data/
   └─ faq.csv
```
