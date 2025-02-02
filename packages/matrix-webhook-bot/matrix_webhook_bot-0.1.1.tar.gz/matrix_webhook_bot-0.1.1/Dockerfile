FROM debian:12-slim

# Add necessary paths to the environment
ENV PATH=/app/.venv/bin:$PATH
ENV PATH=/root/.local/bin:$PATH

WORKDIR /app
# Copy application files
COPY . /app

# Expose port and set up volume
EXPOSE 8228
VOLUME /app/matrix_webhook_bot/config

# Install dependencies and set up Python
RUN apt update && \
    apt install -y curl make g++ && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    uv python install 3.13 && \
    uv venv --python 3.13 /app/.venv && \
    uv sync && \
    python --version


# Set working directory
WORKDIR /app/matrix_webhook_bot

# Use the Python interpreter from the virtual environment
ENTRYPOINT ["python", "main.py"]
