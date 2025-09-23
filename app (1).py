import streamlit as st
import pandas as pd

st.title("HR Insurance Segmentation App")

# Загружаем Excel
uploaded_file = st.file_uploader("Загрузите Excel с данными сотрудников", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Проверяем, есть ли нужные колонки
    required_cols = ["age_score", "dependents_score", "marital_score", "health_score", "seniority_score", "Total_Score"]
    if all(col in df.columns for col in required_cols):

        # Простая сегментация по возрасту и Total_Score
        def segment(row):
            if row["age_score"] <= 2 and row["dependents_score"] == 0 and row["health_score"] <= 2:
                return "Молодые сотрудники"
            elif row["age_score"] <= 3 and row["dependents_score"] >= 1:
                return "Сотрудники среднего возраста с детьми"
            else:
                return "Опытные сотрудники"

        df["Группа"] = df.apply(segment, axis=1)

        # Рекомендации
        recommendations = {
            "Молодые сотрудники": {
                "Тариф": "Standard (Low)",
                "Дополнительно": [
                    "Расширенная стоматология",
                    "Офтальмология (линзы/операции на зрение)",
                    "Программа 'ЗОЖ' (фитнес, спорт, нутрициолог)",
                    "Телемедицина 24/7"
                ]
            },
            "Сотрудники среднего возраста с детьми": {
                "Тариф": "Medium",
                "Дополнительно": [
                    "Семейное страхование (супруги, дети)",
                    "Педиатрия премиум (выезд врача на дом)",
                    "Вакцинация и профилактика",
                    "Страхование путешествий"
                ]
            },
            "Опытные сотрудники": {
                "Тариф": "Premium (High)",
                "Дополнительно": [
                    "Страхование от ССЗ и онкологии",
                    "Ежегодные чек-апы",
                    "Реабилитация и восстановительные программы",
                    "Санаторно-курортное лечение",
                    "Расширенный полис для семьи"
                ]
            }
        }

        st.subheader("📊 Сегментация сотрудников")
        st.write(df.groupby("Группа").size())

        st.subheader("💡 Рекомендации по группам")
        for group, rec in recommendations.items():
            st.markdown(f"### 👥 {group}")
            st.write(f"**Тариф:** {rec['Тариф']}")
            st.write("**Дополнительные опции:**")
            for option in rec["Дополнительно"]:
                st.markdown(f"- {option}")
            st.markdown("---")

    else:
        st.error("В Excel не хватает обязательных колонок. Проверьте структуру файла.")
