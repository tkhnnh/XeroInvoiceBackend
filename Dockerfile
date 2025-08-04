FROM python:3.13-slim

# Install Poetry
RUN pip install --no-cache-dir poetry==2.1.2

WORKDIR /app

COPY . .

# Install dependencies
RUN poetry install

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI with uvicorn
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
