FROM python:3.12-slim
WORKDIR /app
COPY harness/requirements.txt /app/harness/requirements.txt
RUN pip install --no-cache-dir -r /app/harness/requirements.txt
COPY harness /app/harness
ENV PYTHONPATH=/app/harness
EXPOSE 8000
CMD ["python", "/app/harness/mcp_server.py"]
