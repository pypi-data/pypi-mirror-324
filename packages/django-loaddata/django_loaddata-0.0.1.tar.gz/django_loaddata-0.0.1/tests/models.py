# this file is necessary for some reason for test models such as tests/test_loaddata.py

import uuid

from django.db import models


class BaseLoadDataTestModel(models.Model):
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LoadDataTestModel(BaseLoadDataTestModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='uuid')
    field1 = models.CharField(max_length=254, blank=True)
    # Добавляется динамически во время теста
    # field2 = models.CharField(max_length=254, blank=True)

    class Meta:
        app_label = 'tests'

    def __str__(self) -> str:
        return f'(f1={self.field1!r})(f2={getattr(self, "field2", None)!r})(pk={self.pk})'


class LoadDataSecondTestModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='uuid')
    field3 = models.CharField(max_length=254, blank=True)
    # Добавляется динамически во время теста
    # field4 = models.CharField(max_length=254, blank=True)

    class Meta:
        app_label = 'tests'

    def __str__(self) -> str:
        return f'(f3={self.field3!r})(f4={getattr(self, "field4", None)!r})(pk={self.pk})'
