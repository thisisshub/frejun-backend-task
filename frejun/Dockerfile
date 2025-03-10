# Use the official Python image as a base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy pyproject.toml and uv.lock into the container
COPY pyproject.toml uv.lock /app/

# Install dependencies using uv
RUN uv sync

# Copy the entire project into the container
COPY . /app/

# Run migrations (optional, uncomment if needed)
# RUN python manage.py migrate

# Expose the port the app runs on
EXPOSE 8000

# Set up entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]