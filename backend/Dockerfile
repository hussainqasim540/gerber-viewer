
# Usa Python 3.10 slim per un container più leggero
FROM python:3.10-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia i requirements per sfruttare la cache di Docker
COPY requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Installa curl per eventuali richieste HTTP
RUN apt-get update && apt-get install -y curl

# Copia il codice dell'applicazione
COPY . .

# Espone la porta 8000
EXPOSE 8000

# Comando per avviare l'applicazione
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]