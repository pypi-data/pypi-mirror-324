from django.db import models


class ModelFieldHistory(models.Model):
    model = models.CharField('Путь к модели', max_length=254, blank=True)
    fields: list[str] = models.JSONField('Массив полей модели', default=list)

    def __str__(self) -> str:
        return f'({self.model})({self.fields})(pk={self.pk})'
