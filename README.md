# Flask App built via TDD

This is a repo after following the TDD Flaskr tutorial available [here](https://github.com/mjhea0/flaskr-tdd)

### Running Tests:
```
python -m pytest
```


### Run the flask server:
```
FLASK_APP=project/app.py python -m flask run
```

### Initializing DB
from inside python shell
```
from project.app import init_db
init_db()
```