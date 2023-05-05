FROM python:3.8

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["flask", "run", "--host", "0.0.0.0"]