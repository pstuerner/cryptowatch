FROM python:3.10

WORKDIR /app

COPY requirements.txt .
COPY setup.py .
RUN pip install --no-cache-dir -r requirements.txt
    
COPY backend/ /app/backend/
RUN pip install -e .

ENTRYPOINT ["tail", "-f", "/dev/null"]