# OC Lettings — production image
FROM python:3.12-slim

# No .pyc files, unbuffered stdout (logs visible immediately)
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first: this layer is cached unless requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application (includes SQLite DB with demo data, deliberately)
COPY . .

EXPOSE 8000

# Collect static files at startup, then serve with gunicorn
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:8000"]
