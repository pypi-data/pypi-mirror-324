## Extended django loaddata command for uploading fixtures

<div align="center">

| Project   |     | Status                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|-----------|:----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CI/CD     |     | [![Latest Release](https://github.com/Friskes/django-loaddata/actions/workflows/publish-to-pypi.yml/badge.svg)](https://github.com/Friskes/django-loaddata/actions/workflows/publish-to-pypi.yml)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Quality   |     | [![Coverage](https://codecov.io/github/Friskes/django-loaddata/graph/badge.svg?token=vKez4Pycrc)](https://codecov.io/github/Friskes/django-loaddata)                                                                                                                                                                                                                                                                                                                               |
| Package   |     | [![PyPI - Version](https://img.shields.io/pypi/v/django-loaddata?labelColor=202235&color=edb641&logo=python&logoColor=edb641)](https://badge.fury.io/py/django-loaddata) ![PyPI - Support Python Versions](https://img.shields.io/pypi/pyversions/django-loaddata?labelColor=202235&color=edb641&logo=python&logoColor=edb641) ![Project PyPI - Downloads](https://img.shields.io/pypi/dm/django-loaddata?logo=python&label=downloads&labelColor=202235&color=edb641&logoColor=edb641)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Meta      |     | [![types - Mypy](https://img.shields.io/badge/types-Mypy-202235.svg?logo=python&labelColor=202235&color=edb641&logoColor=edb641)](https://github.com/python/mypy) [![License - MIT](https://img.shields.io/badge/license-MIT-202235.svg?logo=python&labelColor=202235&color=edb641&logoColor=edb641)](https://spdx.org/licenses/) [![code style - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/format.json&labelColor=202235)](https://github.com/astral-sh/ruff) |

</div>

## Benefits of using this cli
> 1. Adds the --insert_only flag to the loaddata command, which filters existing database records from the fixture and leaves only new records to insert, thereby preventing overwriting of field values (which may have been changed by the user) in existing records when loaddata is run again.
> 2. Adds the --check_fields flag, which performs the same functions as the --insert_only flag, but additionally remembers the current fields of the loaded table when the fixture is loaded for the first time, so that when adding a new field to the table and restarting loaddata, only the records from the fixture for these new fields are successfully installed, the old fields will not be changed.

## Install
1. Install package
    ```bash
    pip install django-loaddata
    ```

2. Add app name to `INSTALLED_APPS`
    ```python
    INSTALLED_APPS = [
        'django_loaddata',
    ]
    ```

### Command to run the program:
```
python manage.py loaddata
```

## Contributing
We would love you to contribute to `django-loaddata`, pull requests are very welcome! Please see [CONTRIBUTING.md](https://github.com/Friskes/django-loaddata/blob/main/CONTRIBUTING.md) for more information.
