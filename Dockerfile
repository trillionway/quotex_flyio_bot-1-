FROM python:3.10-slim

RUN apt-get update && apt-get install -y wget gnupg unzip curl chromium chromium-driver

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]