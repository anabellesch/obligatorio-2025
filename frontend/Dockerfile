# Imagen base
FROM node:24

# Crea directorio
WORKDIR /app

# Copia archivos y dependencias
COPY package*.json ./
RUN npm install

# Copia el resto
COPY . .

# Construye la app
RUN npm run build

# Usa un servidor liviano para servir el build
RUN npm install -g serve
EXPOSE 3000
CMD ["serve", "-s", "build"]
