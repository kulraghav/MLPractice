FROM python:3.6

WORKDIR /app/

COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT python application.py