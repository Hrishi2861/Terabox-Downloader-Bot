FROM hrishi2861/terabox:latest
WORKDIR /app
COPY . .
CMD ["bash", "start.sh"]
