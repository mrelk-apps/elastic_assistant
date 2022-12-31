FROM python:3.11-alpine
WORKDIR /usr/src/elastic_assistant
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT [ "python", "webapp.py" ]  