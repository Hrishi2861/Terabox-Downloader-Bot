FROM hrishi2861/terabox:latest
WORKDIR /app
RUN pip3 install RUN pip install --no-cache-dir --break-system-packages -r requirements.txt
COPY . .
CMD ["bash", "start.sh"]
