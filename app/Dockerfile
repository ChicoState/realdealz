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


#Install Javascript Testing Environment Components
RUN apk add --no-cache \
    nodejs npm



# Generates a UML Diagram
RUN apk add --no-cache \
    graphviz graphviz-dev gcc musl-dev
    
ENV GRAPHVIZ_DOT=/usr/bin/dot
# Run this command on terminal to generate: python manage.py graph_models -a -o my_models.svg

# Python Dependencies
COPY requirements.txt /app
COPY dev_tools.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir


#Run this command on terminal to generate from APP folder:
#Generate Complexity Report
# radon cc realDealz
# ---------------------

# Copy the rest of the app code
COPY . /app 
RUN npm install
# Run this command on terminal to generate: npx jest

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
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
