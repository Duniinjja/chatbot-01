# web/app.py — versão pública funcional
import csv
import re
import unicodedata
from pathlib import Path
from typing import Optional, List, Tuple

import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

APP_TITLE = "Chatbot (versão web) — Erick Alves"
DATA_PATH = Path(__file__).parent / "data" / "faq.csv"

# ---------- Normalização de texto ----------
def normalize_text(s: str) -> str:
    if not isinstance(s, str):
        s = "" if s is None else str(s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

# ---------- Leitura robusta de CSV ----------
def read_csv_robust(src) -> pd.DataFrame:
    try:
        return pd.read_csv(src, sep=None, engine="python", encoding="utf-8-sig")
    except Exception:
        pass
    for sep in [",", ";", "\t", "|"]:
        try:
            return pd.read_csv(src, sep=sep, engine="python", encoding="utf-8-sig", quoting=csv.QUOTE_MINIMAL)
        except Exception:
            continue
    return pd.read_csv(src, engine="python", encoding="utf-8-sig", on_bad_lines="skip")

# ---------- Carga e preparo da base ----------
@st.cache_data(show_spinner=False)
def load_faq(df_override: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    if df_override is not None:
        df = df_override.copy()
    else:
        if DATA_PATH.exists():
            df = read_csv_robust(DATA_PATH)
        else:
            df = pd.DataFrame({
                "pergunta": ["internet", "energia"],
                "resposta": ["Categoria sugerida: Internet", "Categoria sugerida: Energia"],
                "sinonimos": ["wifi;banda larga;roteador", "luz;enel;energia eletrica"]
            })

    df = df.rename(columns={c: str(c).strip().lower() for c in df.columns})
    if "pergunta" not in df.columns or "resposta" not in df.columns:
        raise ValueError("CSV precisa ter colunas: pergunta,resposta (opcional: sinonimos)")

    df["pergunta"] = df["pergunta"].fillna("").astype(str).str.strip()
    df["resposta"] = df["resposta"].fillna("").astype(str).str.strip()
    if "sinonimos" not in df.columns:
        df["sinonimos"] = ""
    df["sinonimos"] = df["sinonimos"].fillna("").astype(str)

    # Expande sinônimos como perguntas extras apontando para a mesma resposta
    rows = []
    for _, row in df.iterrows():
        base_q = row["pergunta"]
        base_a = row["resposta"]
        rows.append({"pergunta": base_q, "resposta": base_a, "_canonical": base_q, "_is_syn": False})
        syns = [s.strip() for s in row["sinonimos"].split(";") if s.strip()]
        for s in syns:
            rows.append({"pergunta": s, "resposta": base_a, "_canonical": base_q, "_is_syn": True})
    df2 = pd.DataFrame(rows)
    df2["_q_norm"] = df2["pergunta"].map(normalize_text)
    return df2

# ---------- Motor de busca ----------
class Retriever:
    def __init__(self, df: pd.DataFrame):
        self.df = df.reset_index(drop=True)
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=True)
        self.X = self.vectorizer.fit_transform(self.df["_q_norm"])

    def topk(self, query: str, k: int = 3) -> List[Tuple[str, float, str]]:
        if not query.strip():
            return []
        qv = self.vectorizer.transform([normalize_text(query)])
        sims = cosine_similarity(qv, self.X)[0]
        idxs = sims.argsort()[::-1][:k]
        out = []
        for i in idxs:
            row = self.df.iloc[i]
            out.append((row["resposta"], float(sims[i]), row["_canonical"]))
        return out

# ---------- UI ----------
st.set_page_config(page_title=APP_TITLE, page_icon="🤖", layout="centered")
st.title(APP_TITLE)
st.caption("Projeto pessoal — sem vínculo com empresas. Autor: **Erick Alves**")

with st.sidebar:
    st.markdown("### Base de conhecimento (CSV)")
    up = st.file_uploader("Envie um CSV com colunas: pergunta,resposta (opcional: sinonimos)", type=["csv"])
    threshold = st.slider("Confiança mínima", 0.0, 1.0, 0.20, 0.01)
    st.markdown("---")
    st.markdown("Dica: publique esta app no **Streamlit Cloud** com este repositório.")

try:
    df_override = read_csv_robust(up) if up is not None else None
except Exception as e:
    st.error(f"Erro ao ler CSV enviado: {e}")
    df_override = None

df = load_faq(df_override)
retriever = Retriever(df)

with st.sidebar:
    st.markdown(f"**Base carregada:** {len(df):,} entradas (perguntas + sinônimos)")

if 'history' not in st.session_state:
    st.session_state.history = []

for role, content in st.session_state.history:
    with st.chat_message(role):
        st.markdown(content)

prompt = st.chat_input('Digite sua pergunta...')
if prompt is not None:
    st.session_state.history.append(('user', prompt))
    hits = retriever.topk(prompt, k=3)
    if hits:
        best, score, canonical = hits[0]
        if score >= threshold:
            answer = best
        else:
            sugestoes = '\n'.join([f"- {ans} (confiança {sc:.2f})" for ans, sc, _ in hits])
            answer = (
                'Não encontrei resposta com confiança suficiente. Talvez você quis dizer:\n' + sugestoes
            )
    else:
        answer = 'Desculpe, não encontrei nada na base. Tente reformular ou adicione ao CSV.'

    with st.chat_message('assistant'):
        st.markdown(answer)
    st.session_state.history.append(('assistant', answer))
