# Fresh Start Instructions
1. Install pipenv https://docs.pipenv.org/
2. Install mongodb `brew update && brew install mongodb`
3. Start mongodb by running `mongod` in terminal
3. Run `pipenv install` to install dependences from Pipfile.lock
4. Activate the virtual environment with `pipenv shell`
5. Navigate to `django_starter/website`
6. Run `python manage.py makemigrations && python manage.py migrate` to create the schema in the database.
7. Run `python manage.py createsuperuser` to create an admin account to access the database.
8. Start the django server `python manage.py runserver`
9. Navigate to `http://localhost:8000/admin/` and create Irises. Sample 6.9, 3.2, 5.7, 2.3
10. Go to `http://localhost:8000/data/` and click on the hyperlink to see the predicted class.
