FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . .

#CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8666"]
#
#EXPOSE 8666