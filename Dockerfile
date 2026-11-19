FROM hrishi2861/terabox:heroku
WORKDIR /app
# zip is optional: the bot falls back to 7z/7za and then Python's zipfile.
# Keep this best-effort so an old/minimal base image can never break the build.
RUN if [ "$(id -u)" = "0" ] && command -v apt-get >/dev/null 2>&1; then \
        (apt-get -o Acquire::http::Timeout=10 -o Acquire::https::Timeout=10 \
                 -o Acquire::Retries=1 update \
         && apt-get install -y --no-install-recommends zip unzip) \
        || echo "zip/unzip not installed; using 7z or Python zipfile fallback"; \
        rm -rf /var/lib/apt/lists/*; \
    fi
COPY requirements.txt .
RUN uv venv
RUN uv pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["bash", "start.sh"]
