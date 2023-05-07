# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder
EXPOSE 8000
WORKDIR /app 
# Install build dependencies
RUN apk add build-base 

RUN apk add --no-cache \
    libjpeg-turbo-dev \
    zlib-dev libffi-dev

RUN pip install --upgrade pip

RUN apk add --no-cache nodejs npm
COPY package*.json ./
RUN npm install

# Python Dependencies
COPY requirements.txt /app
COPY dev_tools.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
# Copy the rest of the app code
COPY . /app 
ENTRYPOINT ["python3"] 
CMD ["manage.py", "runserver", "0.0.0.0:8000"]

# Note the entrypoint is set to python3
FROM builder as dev-envs
RUN <<EOF
apk update
apk add git
EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF
# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /
CMD ["npm", "manage.py", "runserver", "0.0.0.0:8000"]
