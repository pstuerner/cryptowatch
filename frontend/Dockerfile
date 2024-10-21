FROM python:3.10

WORKDIR /app

COPY requirements.txt .
COPY setup.py .
RUN pip install --no-cache-dir -r requirements.txt
    
COPY frontend/ /app/frontend/
RUN pip install -e .

ENTRYPOINT ["streamlit", "run", "frontend/1_🕵️‍♂️_CryptoWatch.py"]