FROM python:3.12

ENV PYTHONBUFFERED=1

WORKDIR /FastMovies

COPY requirements.txt .

RUN pip install --upgrade pip &&  \
    pip install -r requirements.txt


COPY ngnix.conf /etc/nginx/conf.d/default.conf

COPY . /FastMovies/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]