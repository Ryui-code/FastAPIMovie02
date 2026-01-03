FROM python:3.12

ENV PYTHONBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip &&  \
    pip install -r requirements.txt


COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY . /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]