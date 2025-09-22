import streamlit as st
import pandas as pd

st.title("HR-ассистент по страхованию сотрудников")

uploaded_file = st.file_uploader("Загрузите Excel файл с данными сотрудников", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    df['Group'] = 'Остальные'

    df.loc[(df['age_score'] < 30) & (df['dependents_score'] == 0), 'Group'] = 'Молодые без детей'
    df.loc[(df['age_score'] < 30) & (df['dependents_score'] > 0), 'Group'] = 'Молодые с детьми'
    df.loc[(df['age_score'] >= 30) & (df['age_score'] < 50) & (df['dependents_score'] > 0), 'Group'] = 'Взрослые с детьми'
    df.loc[(df['age_score'] >= 50) | (df['health_score'] < 2), 'Group'] = 'Старшие / с рисками'
    df.loc[(df['seniority_score'] >= 10) | (df['Total_Score'] >= 14), 'Group'] = 'Опытные/лидеры'

    group_counts = df['Group'].value_counts().reset_index()
    group_counts.columns = ['Группа', 'Количество']

    st.subheader("Сегментация сотрудников")
    st.table(group_counts)

    recommendations = {
        "Молодые без детей": "Стандартный пакет + спортстраховка",
        "Молодые с детьми": "Стандартный пакет + детская страховка",
        "Взрослые с детьми": "Семейный пакет",
        "Старшие / с рисками": "Премиум пакет + чек-апы",
        "Опытные/лидеры": "Премиум пакет + корпоративные бонусы",
        "Остальные": "Стандартный пакет"
    }

    st.subheader("Рекомендации по группам")
    for group, rec in recommendations.items():
        count = group_counts.loc[group_counts['Группа'] == group, 'Количество'].values
        count_text = f" ({count[0]} сотрудников)" if len(count) else ""
        st.write(f"**{group}{count_text}:** {rec}")
