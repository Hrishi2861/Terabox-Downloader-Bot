FROM hrishi2861/terabox:heroku
WORKDIR /app
COPY requirements.txt .
RUN uv venv
RUN uv pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["bash", "start.sh"]
