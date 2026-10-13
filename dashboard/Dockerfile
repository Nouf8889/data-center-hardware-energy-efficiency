
FROM python:3.12-slim

WORKDIR /app

# Install dashboard dependencies
COPY dashboard/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy Streamlit application
COPY dashboard/ ./dashboard/

# Configure Cloud Run port
ENV PORT=8080

EXPOSE 8080

# Start Streamlit
CMD ["sh", "-c", "streamlit run dashboard/app.py --server.address=0.0.0.0 --server.port=${PORT} --server.headless=true"]
