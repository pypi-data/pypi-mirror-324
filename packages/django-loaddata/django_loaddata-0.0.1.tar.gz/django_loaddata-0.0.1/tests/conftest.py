import django
from django.conf import settings


def pytest_configure() -> None:
    settings.configure(
        INSTALLED_APPS=[
            'django_loaddata',
            'tests',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        USE_TZ=True,
    )
    django.setup()
