# 🤖 Chatbot 01 — Erick Alves

Este projeto marca a **evolução de um chatbot criado originalmente em Excel/VBA** para uma **versão web moderna e interativa** desenvolvida em **Python com Streamlit**.

---

## 🧩 Evolução do Projeto

- 🧮 **Versão Excel/VBA** — primeira implementação, criada para uso local e offline.
- 💡 **Versão Web (Python + Streamlit)** — reescrita com tecnologias modernas para ser acessível via navegador, gratuita e open-source.
- 🌐 **Disponível online:** [https://chatbot-01-000001.streamlit.app/](https://chatbot-01-000001.streamlit.app/)

Esta nova versão traz a experiência original para a web, permitindo que qualquer pessoa use, teste e contribua com o projeto.

---

## 🧠 Funcionalidades

- Base de conhecimento personalizável via **CSV**.
- Reconhecimento de sinônimos e similaridade semântica.
- Interface leve e responsiva feita com **Streamlit**.
- Totalmente **open-source** e sem vínculo empresarial.

---

## 🚀 Como Executar Localmente

```bash
git clone https://github.com/Duniinjja/chatbot-01.git
cd chatbot-01/web

python -m venv .venv
.venv\Scripts\activate  # (Windows)
source .venv/bin/activate   # (Mac/Linux)

pip install -r requirements.txt
streamlit run app.py
```

Acesse: [http://localhost:8501](http://localhost:8501)

---

## ☁️ Hospedagem no Streamlit Cloud

1. Acesse [https://share.streamlit.io](https://share.streamlit.io)
2. Configure:
   - **Repo:** `Duniinjja/chatbot-01`
   - **Branch:** `main`
   - **Main file path:** `web/app.py`
3. Clique em **Deploy** 🚀

Seu app ficará disponível publicamente no link gerado.

---

## 🗃 Estrutura

```bash
web/
├─ app.py                # Aplicação principal
├─ requirements.txt      # Dependências
├─ data/
│  └─ faq.csv            # Base de conhecimento pública
└─ README_WEB.md         # Guia específico da versão web
```

---

## ✨ Autor

**Erick Alves**  
💡 Projeto pessoal e educativo, livre para uso e colaboração.  
🌍 Disponível online: [https://chatbot-01-000001.streamlit.app/](https://chatbot-01-000001.streamlit.app/)
