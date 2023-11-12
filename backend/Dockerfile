FROM python:3.10.12

# Set work directory
WORKDIR /app

# Install system dependencies
# RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Install system dependencies
# --no-install-recommends
RUN apt-get update && \
    apt-get install -y apt-utils && \
    apt-get install -y netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.cfg /app/
RUN pip install --no-cache-dir -r requirements.cfg

# Copy project
COPY . /app/

# Collect static files
# RUN python manage.py collectstatic --noinput

# # Run migrations
# RUN python manage.py migrate

# Expose port 8000 to the outside world
EXPOSE 8000/tcp

# Make sure the entrypoint.sh script is executable
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Run the entrypoint script
CMD ["/app/entrypoint.sh"]


