FROM python:3.11-slim

WORKDIR /repo

COPY app/requirements.txt app/
RUN pip install --no-cache-dir -r app/requirements.txt

COPY app/ app/

EXPOSE 5000

CMD ["python", "app/app.py"]
