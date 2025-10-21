from fastapi import FastAPI
import pickle
import numpy as np
from pydantic import BaseModel

app = FastAPI()

# Далее идет класс

class InputData(BaseModel):
    median_income: float
    housing_median_age: float
    total_rooms: float
    total_bedrooms: float
    population: float
    households: float
    latitude: float
    longitude: float

# Загрузка модели и пайплайна
with open("best_regression_model.pkl", "rb") as f:
    saved_objects = pickle.load(f)
loaded_feature_engineering = saved_objects["pipeline"]
loaded_model = saved_objects["model"]

@app.post("/predict")
async def predict(input_data: InputData):
    # Преобразование входных данных в numpy массив
    X_new = np.array([[
        input_data.median_income,
        input_data.housing_median_age,
        input_data.total_rooms,
        input_data.total_bedrooms,
        input_data.population,
        input_data.households,
        input_data.latitude,
        input_data.longitude
    ]])
    
    # Преобразование данных с использованием пайплайна
    X_new_transformed = loaded_feature_engineering.transform(X_new)
    
    # Предсказание
    prediction = loaded_model.predict(X_new_transformed)
    
    # Возвращаем предсказание как вещественное число
    return {"prediction": float(prediction[0])}