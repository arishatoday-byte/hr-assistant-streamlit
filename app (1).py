import streamlit as st
import pandas as pd

# Заголовок
st.title("🤖 HR-ассистент с ИИ")

# Загрузка Excel
uploaded_file = st.file_uploader("Загрузите Excel с данными", type=["xlsx"])

if uploaded_file is not None:
    # Читаем файл
    df = pd.read_excel(uploaded_file)

    st.subheader("📊 Загруженные данные")
    st.dataframe(df)

    # Считаем Total Score если есть столбцы
    # ищем колонку с total score, даже если название отличается
possible_names = ["Total_Score", "Total Score", "total_score", "Сумма баллов"]
score_col = None
for name in possible_names:
    if name in df.columns:
        score_col = name
        break

if score_col:
    st.subheader("⭐ Сегментация сотрудников")
    df["Segment"] = pd.cut(
        df[score_col],
        bins=[0, 10, 13, 20],
        labels=["Low", "Medium", "High"]
    )
    st.dataframe(df)
        st.subheader("⭐ Сегментация сотрудников")
        df["Segment"] = pd.cut(
            df["Total_Score"],
            bins=[0, 10, 13, 20],
            labels=["Low", "Medium", "High"]
        )
        st.dataframe(df)

        # Рекомендации по сегментам
        st.subheader("💡 Рекомендации")
        st.write("👥 High — предложить лидерские позиции, премии, развитие.")
        st.write("🙂 Medium — поддерживать мотивацию, обучение.")
        st.write("⚠️ Low — индивидуальные планы развития, наставничество.")
    else:
        st.error("❌ В таблице нет столбца 'Total_Score'")
