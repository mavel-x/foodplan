# foodplan
A meal planning web app


### Development
#### Dump recipe test data
```commandline
venv/bin/python manage.py dumpdata recipes --indent 4 --natural-primary --natural-foreign > testdata.json
```
#### Load recipe test data
```commandline
venv/bin/python manage.py loaddata testdata.json
```