FROM python:3.11-slim
WORKDIR /app
COPY requirements_backend.txt .
RUN pip install --no-cache-dir -r requirements_backend.txt
COPY app/ app/
EXPOSE 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]