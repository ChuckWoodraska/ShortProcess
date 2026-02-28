FROM python:3.12-slim

# Install system dependencies
# - python3-tk: for tkinter (required by customtkinter)
# - curl: to download docker installation script (or install standard docker client)
# - docker.io: easier way to get the docker client on debian/ubuntu bases
RUN apt-get update && apt-get install -y \
    python3-tk \
    curl \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
# Using pip directly here for simplicity in Docker
COPY pyproject.toml .
# We need to install the optional dependencies or main dependencies.
# psutil, customtkinter, packaging are in the pyproject.toml we edited earlier.
# Let's just install them explicitly or parse pyproject.toml. 
# Since we didn't use a lock file manager in the Dockerfile logic yet, manual install or basic pip install . is good.
RUN pip install --no-cache-dir customtkinter psutil packaging

# Copy source code
COPY src/ src/

# Environment variables for display (can be overridden)
ENV DISPLAY=:0

# Command to run
CMD ["python", "src/main.py"]
