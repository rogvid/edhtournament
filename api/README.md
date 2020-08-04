# Smartliving Backend

The smartliving project uses a Django backend, and uses poetry as a package manager to speed up the build process.

## Getting Started
To get the backend up and running locally follow these steps:

Start by setting up a virtual environment
```bash
python3 -m venv .venv && source .venv/bin/activate
```

Install poetry in that virtual enviroment
```bash
pip install poetry
```

Install dependencies with poetry
```bash
poetry install
```

Start the backend
```bash
python manage.py runserver
```

## Getting Started (with docker)
If you want to get this up and running in a docker container and docker is your prefered tool, follow these steps:

NOTE: The dockerfile in this project is a multi-stage dockerfile and can be built for various different purposes

Build the development stage of the Dockerfile.
This takes a while if it is the first time you build it, so go grab a cup of coffee.
```bash
docker build -t smartliving_be:latest .
```

After the build has finished you can now start the container
```bash
docker run -tid -p 8000:8000 --name smartliving_be --rm smartliving_be:latest bash
```
which starts the docker container in detached mode, leaves it up and running, and removes it when stopped.
It is important to remove the container after execution since we've forced the name of the backend to be smartliving_be.

Now start the backend
```bash
docker exec -d smartliving_be python manage.py runserver 0.0.0.0:8000
```
