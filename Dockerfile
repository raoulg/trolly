# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY pyproject.toml .
COPY src src
COPY index.html .
COPY script.js .
COPY styles.css .
COPY README.md .

# Install dependencies and package
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .[all] gunicorn

# Expose the port the app runs on
EXPOSE $PORT

# Run the application
CMD ["python", "-m", "src.trolly.app", "--port", "$PORT"]
