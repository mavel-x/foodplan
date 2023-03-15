# foodplan
A meal planning web app


### Development
#### Dump test data
```commandline
venv/bin/python manage.py dumpdata --indent 4 --natural-primary --natural-foreign > testdata.json
```
#### Load test data
```commandline
venv/bin/python manage.py loaddata testdata.json
```