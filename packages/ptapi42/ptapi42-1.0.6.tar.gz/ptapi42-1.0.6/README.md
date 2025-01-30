# ptapi42

A python package that simplifies the process of making API requests to 42's API.
With this package, developers can quickly and easily access the 42 API's
functionality, without having to deal with the complexities of working directly
with it.

## Acknowledgments

This API is highly influenced by [dropi](https://github.com/42-Portugal/dropi),
which is available as a package as well.
However, with 42 API's updates from earlier this year, dropi became obsolete, or
difficult to use, as it isn't being maintained.
As a result, we decided to create a new API based on dropi, but with some
differences.

## Differences from dropi

While our API is heavily influenced by dropi, it includes some extra features:

* **Configurable Logger**: We've implemented a logging system using the logging
library, which provides you with more control over the messages being logged.
You can use it to debug and monitor your application. The logger's level can be
set to different levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) to filter out
the messages that aren't relevant to your needs.

* **Exception Raising**: You can configure the API to raise exceptions whenever
there's an error. This way, you'll be able to handle the errors in your own
way, rather than having the API fail silently.

* **Rate Limiting**: You can configure the number of requests per second you
want to do to the API. This can help you avoid reaching the API's rate limit
and getting blocked.

* **Maintenance and New Features**: This project is actively maintained, so you
can expect it to be updated with new features and fixes when needed. We're also
working on adding a better `mass_request` function to simplify requests that
involve multiple API endpoints.

## Support

ptapi42 is maintained by the 42 Portugal association, which provides resources
and support to improve the API and address any issues. If you have any
questions or feedback, feel free to reach out to us in
[issues](https://github.com/42-Portugal/ptapi42/issues).

## How to install (in prog)

```zsh
pip install ptapi42
```

## How To Use Api

```python
from ptapi42 import Api42, Api42Request

api: Api42 = Api42()

# Making a simple GET request
campus_id = 'porto'
params: dict = {
	'filter': {
		'pool_month': 'february',
		'pool_year': '2023'
	}
}
url = f'campus/{campus_id}/users'
users = api.get(url=url, params=params)

# Making a mass_request
reqs: list = []
for user in users:
	api_req = Api42Request(url=f"users/{user['id']}")
	reqs.append(api_req)
user_info = api.mass_request('GET', reqs)
```

## Api Reference

## How To Configure Api

The Api has some configurations.
```python
from ptapi42 import Api42

api: Api42 = Api42()
```

### Configure if you want Api42 to raise exceptions

```python
api.raises = True
```

### Configure the max number of requests per second
```python
api.requests_per_second = 8
```

### Configure Api log level
```python
api.log_lvl = 'DEBUG'
api.log_lvl = 'INFO'
api.log_lvl = 'WARNING'
api.log_lvl = 'ERROR'
api.log_lvl = 'FATAL'
```

## Running Tests (dev)

1. Cloning the repository and switching to the testing branch
```zsh
git clone git@github.com:42-Portugal/ptapi42.git
cd ptapi42
```

2. Create a python environment and install the required packages
```zsh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Run the tests
```zsh
python tests.py
```

4. Check for test coverage
```zsh
coverage run tests.py
coverage report
Name                     Stmts   Miss  Cover
--------------------------------------------
ptapi42/__init__.py          1      0   100%
ptapi42/api42.py           219     29    87%
ptapi42/api42_token.py      26      5    81%
ptapi42/config.py           14      1    93%
tests.py                   163      0   100%
--------------------------------------------
TOTAL                      423     35    92%
```
