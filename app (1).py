import streamlit as st
import pandas as pd
import numpy as np

st.title("HR-ассистент по страхованию сотрудников (динамические рекомендации)")

# 1️⃣ Загрузка Excel
uploaded_file = st.file_uploader("Загрузите Excel файл с данными сотрудников", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # 2️⃣ Сегментация
    df['Group'] = 'Остальные'
    df.loc[(df['age_score'] < 30) & (df['dependents_score'] == 0) & (df['health_score'] >= 3), 'Group'] = 'Молодые без детей, низкий риск'
    df.loc[(df['age_score'] < 30) & ((df['dependents_score'] > 0) | (df['health_score'] == 2)), 'Group'] = 'Молодые с детьми / средний риск'
    df.loc[(df['age_score'] >= 30) & (df['age_score'] < 50) & (df['dependents_score'] > 0), 'Group'] = 'Взрослые с детьми / средний риск'
    df.loc[(df['age_score'] >= 50) | (df['health_score'] < 2), 'Group'] = 'Старшие / высокие риски'
    df.loc[(df['seniority_score'] >= 10) | (df['Total_Score'] >= 14), 'Group'] = 'Опытные / лидеры'

    # 3️⃣ Подсчёт количества и средних значений
    group_stats = df.groupby('Group').agg(
        Количество=('Group', 'count'),
        Средний_Total_Score=('Total_Score', 'mean'),
        Средний_health_score=('health_score', 'mean')
    ).reset_index()

    st.subheader("Сегментация сотрудников")
    st.table(group_stats)

    # 4️⃣ Надежный bar chart
    st.subheader("График распределения сотрудников по группам")
    st.bar_chart(group_stats.set_index('Group')['Количество'])

    # 5️⃣ Генерация динамических рекомендаций
    def generate_recommendation(row):
        template_options = [
            "Рекомендуется {package}. Средний уровень Total_Score: {score:.1f}, средний риск здоровья: {health:.1f}. Можно добавить дополнительные опции по здоровью и бонусам.",
            "Пакет {package} идеально подходит для этой группы. Количество сотрудников: {count}. Учитывая средний Total_Score {score:.1f}, стоит предложить дополнительные страховые опции.",
            "Для группы предлагается {package}. Средний health_score: {health:.1f}, средний Total_Score: {score:.1f}. Дополнительно можно предложить гибкие условия и бонусы."
        ]
        if "Молодые без детей" in row['Group']:
            package = "Стандартный пакет + спортстраховка"
        elif "Молодые с детьми" in row['Group']:
            package = "Стандартный пакет + детская страховка"
        elif "Взрослые с детьми" in row['Group']:
            package = "Семейный пакет"
        elif "Старшие" in row['Group']:
            package = "Премиум пакет + чек-апы"
        elif "Опытные" in row['Group']:
            package = "Премиум пакет + корпоративные бонусы"
        else:
            package = "Стандартный пакет"
        template = np.random.choice(template_options)
        return template.format(package=package, count=row['Количество'], score=row['Средний_Total_Score'], health=row['Средний_health_score'])

    group_stats['Рекомендация'] = group_stats.apply(generate_recommendation, axis=1)

    # 6️⃣ Фильтр по группе
    st.subheader("Выберите группу для просмотра рекомендаций")
    selected_group = st.selectbox("Группа сотрудников", options=group_stats['Group'].tolist())

    filtered = group_stats[group_stats['Group'] == selected_group]
    for idx, row in filtered.iterrows():
        st.write(f"**{row['Group']} ({row['Количество']} сотрудников):** {row['Рекомендация']}")
