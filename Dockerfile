FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

RUN pip install --upgrade pip 

COPY requirements.txt  /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN ls

# RUN python manage.py makemigrations && python manage.py migrate

EXPOSE 8000

CMD ["python", "stripe_payment/manage.py", "runserver", "0.0.0.0:8000"]
