# realdealz
[![Django CI](https://github.com/ChicoState/realdealz/actions/workflows/django.yml/badge.svg)](https://github.com/ChicoState/realdealz/actions/workflows/django.yml)

# How to develop this project locally with docker compose

```
$ docker compose up
Creating network "django_default" with the default driver
Building web
Step 1/6 : FROM python:3.7-alpine
...
...
Status: Downloaded newer image for python:3.7-alpine
Creating django_web_1 ... done
```

In order to test python or parts of the application from within the container you can use the following commands:
__Please note that in this example realdealz-web-1 is the name of the container, you can find the name of the container by running `docker ps`__

`docker exec -it realdealz-web-1 ash`
- This Will open a shell in the container and you can run commands from there like a normal shell
- for using shell commands like `ls` or `cd`

`docker exec -it realdealz-web-1 ipython`
- This will open an interactive python shell in the container 
- for using a smart python shell


## Expected Results
```
❯ docker compose up
[+] Running 2/2
 ⠿ Network realdealz_default  Created                                             0.0s
 ⠿ Container realdealz-web-1  Created                                             0.0s
Attaching to realdealz-web-1
realdealz-web-1  | Watching for file changes with StatReloader
```

if you want to force a rebuild of the container you can use the `--build` flag
```
docker compose up --build 
``` 
i.e. 
1. Make a change to the requirements.txt file
2. use ctrl+c to stop the docker compose
3. run `docker compose up --build` to rebuild the container


After the application starts, navigate to `http://localhost:8000` in your web browser:

## When you are done
Stop and remove the containers
```
$ docker compose down
```


## Changelog 

urls.py: Added support for About Us, Contact, and Catalog pages for the website

views.py: Used a generic listview for the catalog and added support for the other pages

models.py: Added new features. (Note: Still need to add image support)

Added templates to library folder and made their urls functional

The catalog page now shows results from our database
