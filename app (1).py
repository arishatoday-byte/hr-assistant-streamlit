import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

    # 4️⃣ График распределения сотрудников по группам (разные оттенки зелёного)
    st.subheader("График распределения сотрудников по группам")
    colors = plt.cm.Greens(np.linspace(0.4, 0.9, len(group_stats)))
    fig, ax = plt.subplots()
    ax.bar(group_stats['Group'], group_stats['Количество'], color=colors)
    plt.xticks(rotation=20, ha='right')
    st.pyplot(fig)

    # 5️⃣ Чёткие рекомендации
    def generate_recommendation(group):
        if "Молодые без детей" in group:
            return """**Тариф:** Стандартный пакет + спортстраховка  
            Доп. опции (за отдельную плату): фитнес-абонементы, онлайн-консультации врачей, страхование от травм."""
        elif "Молодые с детьми" in group:
            return """**Тариф:** Стандартный пакет + детская страховка  
            Доп. опции: стоматология для детей, вакцинация, программы «здоровая семья»."""
        elif "Взрослые с детьми" in group:
            return """**Тариф:** Семейный пакет  
            Доп. опции: расширенное покрытие для детей и супругов, стоматология, страховка путешествий."""
        elif "Старшие" in group:
            return """**Тариф:** Премиум пакет + чек-апы  
            Доп. опции: страхование от сердечно-сосудистых заболеваний, онкострахование, расширенные госпитальные программы."""
        elif "Опытные" in group:
            return """**Тариф:** Премиум пакет + корпоративные бонусы  
            Доп. опции: страхование семьи, корпоративные пенсионные программы, персональный менеджер."""
        else:
            return """**Тариф:** Базовый пакет  
            Доп. опции: стандартные медуслуги + консультации онлайн."""
    
    group_stats['Рекомендация'] = group_stats['Group'].apply(generate_recommendation)

    # 6️⃣ Фильтр по группе
    st.subheader("Выберите группу для просмотра рекомендаций")
    selected_group = st.selectbox("Группа сотрудников", options=group_stats['Group'].tolist())

    filtered = group_stats[group_stats['Group'] == selected_group]
    for idx, row in filtered.iterrows():
        st.markdown(f"### {row['Group']} ({row['Количество']} сотрудников)")
        st.markdown(row['Рекомендация'])
