# Utilizar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos de requerimientos para instalar dependencias
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . /app

# Exponer el puerto para Flask
EXPOSE 5000

# Configurar la variable de entorno para el entorno de desarrollo
ENV FLASK_ENV=development

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]
