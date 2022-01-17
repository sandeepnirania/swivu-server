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

## ERD

To generate an Entity Relationship Diagram, run:

```
python manage.py graph_models -a > output.dot
```

Convert DOT to PNG using graphviz or any free online tool (for example, [https://onlineconvertfree.com/convert/dot/](https://onlineconvertfree.com/convert/dot/) )

