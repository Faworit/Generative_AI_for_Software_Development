"""
app_streamlit.py
Streamlit app: простой интерфейс для RAG-поиска отелей.
Run: streamlit run app_streamlit.py
"""
import os
import streamlit as st
from search_and_answer import search, build_prompt, call_llm

st.set_page_config(page_title="Hotel RAG Assistant", layout="centered")

st.title("Помощник по подбору отеля (RAG)")
st.write("Введите, что вам нужно: город, бюджет, удобства или общие пожелания.")

query = st.text_input("Ваш запрос", value="Нужен 4-звёздочный отель в Париже с бассейном и завтраком, до 150 EUR/ночь")
top_k = st.slider("Количество документов для поиска (top_k)", 1, 8, 4)

if st.button("Найти и спросить"):
    if not query.strip():
        st.warning("Введите запрос.")
    else:
        with st.spinner("Ищу похожие описания и формирую ответ..."):
            docs = search(query, top_k=top_k)
            if not docs:
                st.info("Не найдено релевантных документов.")
            else:
                st.subheader("Найденные отели (контекст)")
                for d in docs:
                    st.markdown(f"**{d.get('name')}** — {d.get('city')}, {d.get('country')} ({d.get('stars')}★)\n\n{d.get('description')}\n\nURL: {d.get('url')}")
                prompt = build_prompt(query, docs)
                answer = call_llm(prompt)
                st.subheader("Результат от LLM")
                st.write(answer)
