# Borderless is your new way of bringing creative ideas to life
## Instalation

* Download Project
* Navigate to directory containing requirements.txt
* Run `pip3 install -r requirements.txt`

## Starting localhost server

* Navigate to directory containing manage.py
* Run `python3 manage.py runserver`
* Open browser at `localhost:8000/`

## Running Tests

* Navigate to directory containing manage.py
* Run `python3 manage.py test`
* To run induvidual tests run bash> python3 manage.py test {app_name}

## Authenticating

* The api uses jwt token authentication.
* Get a token by POSTing your `username` and `password` to `localhost:8000/api-token-auth`
* For every request, send your token in the `Authentication` header.
* Tokens expire after 10 mins.
* Refresh your token by POSTing your "token" to `localhost:8000/api-token-refresh`
