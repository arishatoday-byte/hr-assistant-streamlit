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
    if "Total_Score" in df.columns:
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
