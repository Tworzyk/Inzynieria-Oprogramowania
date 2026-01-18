FROM python:3.10-slim
WORKDIR /app
# Instalacja paczek potrzebnych dla Postgresa
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy wszystko (w tym folder Services)
COPY . .

# Dzięki temu Python będzie widział folder Services jako pakiet
ENV PYTHONPATH=/app