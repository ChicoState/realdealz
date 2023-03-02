# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.7-alpine AS builder
EXPOSE 8000
WORKDIR /app 
COPY requirements.txt /app
RUN apk add build-base 
RUN pip3 install ipython --no-cache-dir
RUN pip3 install -r requirements.txt --no-cache-dir
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
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
