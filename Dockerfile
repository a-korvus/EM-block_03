FROM python:3.13.2
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /temp/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /temp/requirements.txt

COPY website /website
WORKDIR /website

EXPOSE 8000
