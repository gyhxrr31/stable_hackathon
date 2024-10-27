from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import matplotlib.pyplot as plt
import base64

# Инициализация FastAPI приложения
app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Измените на нужные домены в продакшене
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    # Проверка формата файла
    if not file.filename.endswith('.csv'):
        return JSONResponse(status_code=400, content={"message": "Файл должен быть в формате CSV"})

    try:
        # Чтение CSV файла
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents), encoding='utf-8')

        # Проверка наличия колонки 'new_value'
        if 'new_value' not in df.columns:
            return JSONResponse(status_code=400, content={"message": "CSV файл должен содержать колонку 'new_value'"})

        # Генерация диаграмм
        status_counts = df['new_value'].value_counts()
        plot_url_bar = create_bar_chart(status_counts)
        plot_url_pie = create_pie_chart(status_counts)

        return JSONResponse(content={"bar_chart": plot_url_bar, "pie_chart": plot_url_pie})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

def create_bar_chart(status_counts):
    plt.figure(figsize=(12, 6))
    plt.bar(status_counts.index, status_counts.values, color='skyblue')
    plt.title('Количество изменений для каждого нового статуса')
    plt.xlabel('Новый статус')
    plt.ylabel('Количество изменений')
    plt.xticks(rotation=45)

    # Сохранение графика в память
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    # Кодируем в base64
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def create_pie_chart(status_counts):
    threshold = 0.05 * status_counts.sum()
    major_statuses = status_counts[status_counts >= threshold]
    other_statuses = pd.Series({'Другие': status_counts[status_counts < threshold].sum()})
    status_counts_normalized = pd.concat([major_statuses, other_statuses])

    plt.figure(figsize=(8, 8))
    plt.pie(status_counts_normalized.values, labels=status_counts_normalized.index, autopct='%1.1f%%', startangle=140)
    plt.title('Процентное соотношение новых статусов (нормализовано)')

    # Сохранение графика в память
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    # Кодируем в base64
    return base64.b64encode(buf.getvalue()).decode('utf-8')
