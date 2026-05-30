FROM python:3.15-rc-trixie

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ..

CMD ["fastapi", "run", "app/main.py", "--port", "80"]