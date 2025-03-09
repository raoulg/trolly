# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY pyproject.toml .
COPY src .
COPY dist .
COPY index.html .
COPY script.js .
COPY styles.css .
COPY README.md .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .[all]

# Copy the rest of the application
COPY . .

# Install the wheel
RUN pip install --no-cache-dir /app/dist/*.whl

# Expose the port the app runs on
EXPOSE 80

# Run the application
CMD ["python", "-m", "src.trolly.app", "--port", "80"]
