FROM hrishi2861/terabox:latest
WORKDIR /app
RUN pip3 install flask
COPY . .
CMD ["bash", "start.sh"]
