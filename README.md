# swivu-server

Swivu server.

Includes Bryntum sync protocol support.


## Getting Started

Create a virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

Create postgres database.

```
createdb swivu-server
```

## Dev

Create a superuser

```
python manage.py createsuperuser
```

(Provide the information prompted for.)

Run server (also installs required modules and runs migrations, as needed)

```
make run
```
