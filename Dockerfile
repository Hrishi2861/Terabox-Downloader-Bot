FROM hrishi2861/terabox:heroku
WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends zip unzip \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN uv venv
RUN uv pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["bash", "start.sh"]
