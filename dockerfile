FROM python:3.9-slim

# Nastavení pracovní složky
WORKDIR /app

# Instalace systémových knihoven a Chromium + ChromeDriver
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unzip \
    wget \
    fonts-liberation \
    libasound2 \
    libnss3 \
    libxss1 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm-dev \
    libgtk-3-0 \
    libu2f-udev \
    libvulkan1 \
    xdg-utils \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# 📌 Zajištění cesty k Chromium a Chromedriver
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV PATH="/usr/bin:$PATH"

# Instalace Python knihoven
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 📦 Kopírování tvého kódu
COPY . .

# 🔧 Spuštění skriptu
CMD ["python", "main.py"]
