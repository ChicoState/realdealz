# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder
EXPOSE 8000
WORKDIR /app 
# Install build dependencies
RUN apk add --no-cache \
    build-base 

RUN apk add --no-cache \
    libjpeg-turbo-dev \
    zlib-dev libffi-dev \

RUN apk add --no-cache \
    git

RUN pip install --upgrade pip
# Python Dependencies
COPY requirements.txt /app
COPY dev_tools.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
# Copy the rest of the app code
COPY . /app 
# ----------------------------------------------------------
FROM builder as dev-env
WORKDIR /app 

RUN addgroup -S docker && \
    adduser -S --shell /bin/bash --ingroup docker vscode

RUN /app/postCreate.sh
# Start the web app server 
ENTRYPOINT ["python3"] 
CMD ["manage.py", "runserver", "0.0.0.0:8000"]

# ----------------------------------------------------------

FROM builder as prod-env
WORKDIR /app
ENTRYPOINT ["python3"] 
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
