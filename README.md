# database-django
### Baseline

To manage Django's projects and apps, here are some pre-requisites:
- Have Python, Brew, PostgreSQL installed
- Have some fluency in python, html, css, and javascript

### Get Started

**Note: For MacOS, add a '3' behind 'python' or 'pip': 'python3' / 'pip3'**

First, download the LIMSWebTemplate. Unzip the folder and go into the folder. Then, create a virtual environment:

```
: terminal
python -m venv "virtual_environment_name"
```

Once complete, start your virtual environment:

```
: terminal
source virtual_environment_name/bin/active
```

Then, install the following packages (information on the packages are found in references):

```
: terminal
pip install django
pip install psycopg2-binary
pip install django-import-export
pip install django-taggit
```

### Connect to Database

Go into `settings.py` and find the line where it reads `DATABASES` (line 87). Fill in the correct credentials for connecting to your postgreSQL database. 

If you have not created the database and its schemas in postgreSQL, there will be an error if you directly try to establish connection. You will need to create a schema for each app in the template. Or, you can remove the app from the template and settings.py.

When finished, migrate all the data structures built within this template:

```
python3 manage.py migrate
```

Once finished, create your credentials as a superuser (follow the terminal instructions after this command to complete the process):

```
python3 manage.py createsuperuser
```

### Launch server
For current iMac:
```
ssh uhlemann@156.145.55.229
```

Password: core1234
**You won't be able to see what you type when entering in the password**

```
cd Documents/sandbox-launched/
source virtualenv/bin/activate
python3 manage.py runserver 0.0.0.0:8000
```

## References:
1. [Django](https://www.djangoproject.com/)
2. [Psycopg2](https://www.psycopg.org/docs/)
3. [Django Import Export](https://django-import-export.readthedocs.io/en/latest/)
4. [Django Taggit](https://django-taggit.readthedocs.io/en/latest/)
5. [ApexCharts](https://apexcharts.com/)
