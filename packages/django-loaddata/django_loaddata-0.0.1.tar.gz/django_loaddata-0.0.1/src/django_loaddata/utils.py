from __future__ import annotations

import itertools
import json
import sys
from collections.abc import Callable, Hashable, Iterable
from functools import cache, wraps
from json import JSONEncoder
from typing import TYPE_CHECKING, Any, Generic, Literal, NamedTuple, TypedDict, TypeVar, cast, final

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from django.db.models.fields import Field
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.shortcuts import _get_queryset

try:
    from rest_framework.utils.encoders import JSONEncoder as JsonEncoder  # type: ignore
except ImportError:
    from django.core.serializers.json import DjangoJSONEncoder as JsonEncoder


if TYPE_CHECKING:
    from django.db.models.options import Options


class ObjectNotFoundError(Exception):
    pass


DBModelType = TypeVar(
    'DBModelType', Model, type[Model], Manager, type[Manager], QuerySet, type[QuerySet]
)


def _create_validation_error(
    exc_cls: ObjectNotFoundError, object_name: str, **kwargs
) -> ObjectNotFoundError:
    """Создаёт экземпляр ошибки валидации с переданными параметрами"""
    stringify_params = {
        str(k): (list({str(x): 0 for x in v}.keys()) if isinstance(v, Iterable) else str(v))
        for k, v in kwargs.items()
    }
    return exc_cls(f'{object_name} с {stringify_params} не существует.')


def _get_object_base(
    exc_cls: ObjectNotFoundError, klass: DBModelType, method: Literal['get', 'filter'], **kwargs
):
    """Базовая функция для запросов с помощью get/filter через Django ORM."""

    if method not in ['get', 'filter']:
        raise ValueError(
            "Аргумент method для _get_object_base() должен быть 'get' или 'filter' строкой, "
            "а не '%s'." % method
        )

    if not kwargs:
        raise ValueError('Аргумент kwargs для _get_object_base() не должен быть пустым.')

    queryset: QuerySet = _get_queryset(klass)

    if not hasattr(queryset, method):
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            'Аргумент klass для _get_object_base() должен быть Model, Manager, '
            "или QuerySet, а не '%s'." % klass__name
        )
    try:
        qs = getattr(queryset, method)(**kwargs)
        if not qs:
            raise _create_validation_error(exc_cls, queryset.model._meta.object_name, **kwargs)
        return qs
    except ObjectDoesNotExist as exc:
        raise _create_validation_error(exc_cls, queryset.model._meta.object_name, **kwargs) from exc


def get_object_or_none(model: DBModelType, **kwargs) -> DBModelType | None:
    """
    Возвращает `object` если он найден в `model` иначе `None`\n
    В качестве `model` так же может принимать:\n
    >>> SomeModel.objects.select_related("field")\n
    и т.д.
    """
    try:
        return _get_object_base(ObjectNotFoundError, model, 'get', **kwargs)
    except ObjectNotFoundError:
        return None


def transform_payload(payload: dict, encoder: JSONEncoder = JsonEncoder) -> dict:
    """
    Преобразует "date/time, decimal types, and UUIDs" к строке.

    Доступные кодировщики::

        from rest_framework.utils.encoders import JSONEncoder as DrfJSONEncoder
        from django.core.serializers.json import DjangoJSONEncoder
    """
    return json.loads(json.dumps(payload, cls=encoder))


def _allowed_field_name(field_name, fields, exclude):
    return not (
        (fields is not None and field_name not in fields)
        or (exclude is not None and field_name in exclude)
    )


def better_model_to_dict(instance: Model, fields=None, exclude=None):
    """
    - Расширение `django.forms.model_to_dict` для решения проблемы:
        - Не создаёт пары полей которые попали в модель
        с помощью наследования от abstract модели.

    https://stackoverflow.com/a/29088221/19276507

    ---

    Return a dict containing the data in ``instance`` suitable for passing as
    a Form's ``initial`` keyword argument.

    ``fields`` is an optional list of field names. If provided, return only the
    named.

    ``exclude`` is an optional list of field names. If provided, exclude the
    named from the returned dict, even if they are listed in the ``fields``
    argument.
    """

    opts: Options = instance._meta
    data = {}
    for f in cast(list[Field], itertools.chain(opts.concrete_fields, opts.private_fields)):
        if _allowed_field_name(f.name, fields, exclude):
            data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        if _allowed_field_name(f.name, fields, exclude):
            data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data


def not_in_cmd(prefix: str | tuple[str, ...]) -> bool:
    """Возвращает True если в sys.argv нету строк(и) с prefix, иначе False"""
    return not any(arg.startswith(prefix) for arg in sys.argv)


_T = TypeVar('_T')


class _CacheInfo(NamedTuple):
    hits: int
    misses: int
    maxsize: int | None
    currsize: int


class _CacheParameters(TypedDict):
    maxsize: int
    typed: bool


@final
class _lru_cache_wrapper(Generic[_T]):  # noqa: N801
    __wrapped__: Callable[..., _T]
    was_cached: bool

    def __call__(self, *args: Hashable, **kwargs: Hashable) -> _T: ...
    def cache_info(self) -> _CacheInfo: ...
    def cache_clear(self) -> None: ...
    def cache_parameters(self) -> _CacheParameters: ...
    def __copy__(self) -> _lru_cache_wrapper[_T]: ...
    def __deepcopy__(self, memo: Any, /) -> _lru_cache_wrapper[_T]: ...


def cache_with_status(user_function: Callable[..., _T], /) -> _lru_cache_wrapper[_T]:
    """
    Simple lightweight unbounded cache. Sometimes called "memoize".\n
    Расширенный новым флагом `was_cached`, был ли взят результат из кэша в этом вызове.
    (было ли попадание в кэш)
    """
    cached_func = cache(user_function)

    @wraps(cached_func)
    def wrapper(*args, **kwargs):
        before_hits = cached_func.cache_info().hits
        result = cached_func(*args, **kwargs)
        wrapper.was_cached = cached_func.cache_info().hits > before_hits
        return result

    wrapper.cache_info = cached_func.cache_info
    wrapper.cache_clear = cached_func.cache_clear
    return wrapper
