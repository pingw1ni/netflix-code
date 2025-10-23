import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Netflix Data Explorer", layout="wide")

st.title("🍿 Netflix Movies & TV Shows Explorer")
st.write("Исследуйте каталог Netflix — фильмы и сериалы по странам, жанрам и годам!")

# === 1️⃣ Автоматическая или ручная загрузка файла ===
file_path = "netflix_titles.csv"
uploaded_file = st.file_uploader("📂 Или загрузите CSV-файл вручную", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("Файл успешно загружен вручную ✅")
elif os.path.exists(file_path):
    df = pd.read_csv(file_path)
    st.success("Файл 'netflix_titles.csv' найден и загружен автоматически ✅")
else:
    st.error("Файл не найден! Загрузите CSV вручную или поместите 'netflix_titles.csv' рядом с app.py.")
    st.stop()

# === 2️⃣ Основная информация ===
st.subheader("📊 Общая информация о данных")
st.write(f"Количество записей: {df.shape[0]}")
st.write(f"Количество колонок: {df.shape[1]}")
st.dataframe(df.head())

# === 3️⃣ Боковая панель фильтров ===
st.sidebar.header("🎛 Фильтры")
type_filter = st.sidebar.multiselect(
    "Тип контента", 
    df["type"].dropna().unique(), 
    default=df["type"].unique()
)

# обработка пропусков в столбце country
countries = df["country"].dropna().unique().tolist()
countries.sort()
country_filter = st.sidebar.selectbox("Страна", ["Все"] + countries)

year_filter = st.sidebar.slider(
    "Год выпуска", 
    int(df["release_year"].min()), 
    int(df["release_year"].max()), 
    (2010, 2021)
)

show_desc = st.sidebar.checkbox("Показать статистику DataFrame")
chart_choice = st.sidebar.radio("Тип графика", ["Распределение по годам", "Рейтинг жанров"])
color = st.sidebar.color_picker("Цвет графика", "#E50914")

# === 4️⃣ Применение фильтров ===
filtered_df = df[df["type"].isin(type_filter)]
filtered_df = filtered_df[
    (filtered_df["release_year"] >= year_filter[0]) & 
    (filtered_df["release_year"] <= year_filter[1])
]
if country_filter != "Все":
    filtered_df = filtered_df[filtered_df["country"] == country_filter]

st.subheader("🔍 Отфильтрованные данные")
st.write(f"Отображено записей: {filtered_df.shape[0]}")
st.dataframe(filtered_df.head(10))

# === 5️⃣ Статистика ===
if show_desc:
    st.write(filtered_df.describe(include="all"))

# === 6️⃣ Визуализация ===
st.subheader("📈 Визуализация данных")

if chart_choice == "Распределение по годам":
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(data=filtered_df, x="release_year", hue="type", palette="Set2", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif chart_choice == "Рейтинг жанров":
    genres = filtered_df["listed_in"].dropna().str.split(", ").explode().value_counts().head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=genres.values, y=genres.index, color=color, ax=ax)
    plt.xlabel("Количество")
    plt.ylabel("Жанр")
    st.pyplot(fig)

