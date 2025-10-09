# Python 3.12 slim Debian
FROM python:3.12-slim

# Обновляем системные пакеты и ставим необходимые библиотеки
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    ffmpeg \
    libjpeg-dev \
    libtiff-dev \
    libpng-dev \
    libpq-dev \
    libgl1 \
    libglib2.0-0 \
    ca-certificates \
    libnss3 \
    libxss1 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxshmfence1 \
    libgtk-3-0 \
    libasound2 \
    libgbm1 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    xdg-utils \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*


# Создаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt


RUN playwright install chromium

# Копируем весь проект
COPY . .

# Открываем порт для FastAPI
EXPOSE 8000

# Запуск сервера
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
