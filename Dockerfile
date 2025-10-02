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

# Copy test data
COPY test_data/ /app/test_data/

# Copy sanity check scripts
COPY data_sanity_checks/ /app/data_sanity_checks/

# Create directory for model cache
RUN mkdir -p /root/.cache/huggingface

CMD ["python", "clap_similarity.py"]
