import streamlit as st
import requests

# Устанавливаем заголовок страницы
st.title("Прогноз цены на жилье")

# Ввод данных пользователем
median_income = st.number_input("Медианный доход", value=3.0)
housing_median_age = st.number_input("Средний возраст жилья", value=20.0)
total_rooms = st.number_input("Общее количество комнат", value=1000.0)
total_bedrooms = st.number_input("Общее количество спален", value=200.0)
population = st.number_input("Население", value=1500.0)
households = st.number_input("Количество домохозяйств", value=500.0)
latitude = st.number_input("Широта", value=37.88)
longitude = st.number_input("Долгота", value=-122.23)

# Кнопка для отправки запроса
if st.button("Получить прогноз"):
    # Формирование данных для POST-запроса
    data = {
        "median_income": median_income,
        "housing_median_age": housing_median_age,
        "total_rooms": total_rooms,
        "total_bedrooms": total_bedrooms,
        "population": population,
        "households": households,
        "latitude": latitude,
        "longitude": longitude
    }
    
    # Отправка POST-запроса к API
    url = "https://test-regression.onrender.com/predict"
    response = requests.post(url, json=data)
    
    
    if response.status_code == 200:
        try:
            data = response.json()
            prediction = data.get('prediction')
            if prediction is not None:
                st.success(f"Прогнозируемая цена: ${prediction*1000:.2f}")
                st.subheader("Визуализация прогноза")
                st.bar_chart({"Прогноз": [prediction]})
            else:
                st.error("Ошибка: Ответ API не содержит прогноз.")
        except ValueError:
            st.error("Ошибка: Ответ API не является валидным JSON.")
    else:
        st.error(f"Ошибка: API вернул статус {response.status_code}")