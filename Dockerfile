FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app

# 1. Copia SOLO el archivo de dependencias
COPY requirements.txt .

# 2. Instala dependencias (esta capa se cachea y solo se re-ejecuta si requirements.txt cambia)
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copia el resto del código (si solo cambia un .py, esta capa se reconstruye pero la de pip no)
COPY . .

CMD streamlit run app/main.py --server.port $PORT --server.address 0.0.0.0