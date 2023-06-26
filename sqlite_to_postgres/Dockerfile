FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

WORKDIR /opt/app
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копирования кода приложения
COPY .  .

CMD ["python3", "/opt/app/load_data.py"]
