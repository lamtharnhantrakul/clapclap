FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY clap_similarity.py .
COPY generate_mixtures.py .
COPY test_loudness_effect.py .

# Create directory for model cache
RUN mkdir -p /root/.cache/huggingface

CMD ["python", "clap_similarity.py"]
