# FROM python:3.10.12
#
# # Set environment variables
# ENV POSTGRES_DB lets_take_a_ride
# ENV POSTGRES_USER rider
# ENV POSTGRES_PASSWORD ss5Secure!
# ENV DJANGO_SECRET_KEY=django-insecure-7&p7fb+_*u%r)d4$ohzjd02q0lw-+o8d6r+6f-pu5@zjv#9dy$
# ENV DJANGO_TIME_ZONE=UTC
# ENV DATABASE_URL=postgres://rider:ss5Secure!@localhost:5438/lets_take_a_ride
# ENV DJANGO_AUTH0_DOMAIN=dev-1w8bd2btom2xomge.eu.auth0.com
# ENV DJANGO_AUTH0_AUDIENCE=https://dev-1w8bd2btom2xomge.eu.auth0.com/api/v2/

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


