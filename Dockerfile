FROM python:3.7.5

WORKDIR /app/

COPY . .

COPY requirements.txt /
RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -r /requirements.txt

ENTRYPOINT ["python", "main.py"]