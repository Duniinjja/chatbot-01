import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

APP_TITLE = "Chatbot (versão web) — Erick Alves"
DATA_PATH = Path(__file__).parent / 'data' / 'faq.csv'

@st.cache_data(show_spinner=False)
def load_faq(df_override: pd.DataFrame | None = None):
    if df_override is not None:
        df = df_override.copy()
    else:
        if not DATA_PATH.exists():
            # Fallback de exemplo
            df = pd.DataFrame({
                'pergunta': [
                    'O que é este projeto?',
                    'Como ativo as macros no Excel?',
                    'Quem é o autor?'
                ],
                'resposta': [
                    'Um chatbot criado em Excel/VBA, disponibilizado também em versão web para demonstração.',
                    'No Excel Desktop: Arquivo > Opções > Central de Confiabilidade > Configurações de Macros > Habilitar.',
                    'Erick Alves.'
                ]
            })
        else:
            df = pd.read_csv(DATA_PATH)
    # Garantir colunas
    df = df.rename(columns={c: c.lower() for c in df.columns})
    assert {'pergunta','resposta'}.issubset(set(df.columns)), "CSV precisa ter colunas: pergunta,resposta"
    return df

class Retriever:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.vectorizer = TfidfVectorizer(ngram_range=(1,2), lowercase=True)
        self.X = self.vectorizer.fit_transform(df['pergunta'].fillna(''))

    def match(self, query: str, threshold: float = 0.25):
        if not query.strip():
            return None, 0.0
        qv = self.vectorizer.transform([query])
        sims = cosine_similarity(qv, self.X)[0]
        idx = sims.argmax()
        score = float(sims[idx])
        if score < threshold:
            return None, score
        row = self.df.iloc[idx]
        return row['resposta'], score

st.set_page_config(page_title=APP_TITLE, page_icon='🤖', layout='centered')

st.title(APP_TITLE)
st.caption('Projeto pessoal — sem vínculo com empresas. Autor: **Erick Alves**')

with st.sidebar:
    st.markdown('### Base de conhecimento (CSV)')
    up = st.file_uploader('Envie um CSV com colunas: pergunta,resposta', type=['csv'])
    threshold = st.slider('Confiança mínima', 0.0, 1.0, 0.25, 0.01)
    st.markdown('---')
    st.markdown('Dica: publique esta app no **Streamlit Cloud** com este repositório.')

if 'history' not in st.session_state:
    st.session_state.history = []  # lista de (role, content)

try:
    df_override = pd.read_csv(up) if up is not None else None
except Exception as e:
    st.error(f'Erro ao ler CSV: {e}')
    df_override = None

df = load_faq(df_override)
retriever = Retriever(df)

# UI de chat
for role, content in st.session_state.history:
    with st.chat_message(role):
        st.markdown(content)

prompt = st.chat_input('Digite sua pergunta...')
if prompt is not None:
    st.session_state.history.append(('user', prompt))
    answer, score = retriever.match(prompt, threshold=threshold)
    if answer is None:
        answer = 'Desculpe, não encontrei uma resposta na base. Tente reformular ou adicione ao CSV.'
    with st.chat_message('assistant'):
        st.markdown(answer)
    st.session_state.history.append(('assistant', answer))
