# Imagen base
FROM python:3.13-slim

# Crea directorio
WORKDIR /app

# Copia los archivos
COPY requirements.txt .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Expone el puerto donde corre Flask
EXPOSE 5000

# Comando de inicio
CMD ["python", "app.py"]
