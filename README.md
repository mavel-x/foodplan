# foodplan
A meal planning web app


### Development
#### Dump recipe test data
```commandline
venv/bin/python manage.py dumpdata recipes.Allergy recipes.MealType recipes.Ingredient recipes.Recipe recipes.Amount --indent 4 --natural-primary --natural-foreign > data/testdata.json
```
#### Load recipe test data
```commandline
venv/bin/python manage.py loaddata data/testdata.json
```