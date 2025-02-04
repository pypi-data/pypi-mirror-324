from __future__ import annotations

import glob
import json
import logging
import os
import sys
from typing import TYPE_CHECKING, Any, Literal, Union

from django.apps import apps
from django.core import serializers
from django.core.management.commands import loaddata
from django.db import models, transaction

from django_loaddata.models import ModelFieldHistory
from django_loaddata.utils import (
    better_model_to_dict,
    cache_with_status,
    get_object_or_none,
    transform_payload,
)

if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger(__name__)
logger.setLevel(1)

FixtureKeysType = Literal['model', 'pk', 'fields']

RecordsType = list[dict[FixtureKeysType, Union[str, int, dict[str, Any]]]]  # noqa: UP007

RecordsInfoType = list[dict[str, Union[ModelFieldHistory, list[str]]]]  # noqa: UP007


class Command(loaddata.Command):
    """
    - Расширение команды loaddata по умолчанию,
    функционалом (флаг --insert_only) фильтрации
    уже существующих в бд записей в фикстуре.
        - Тем самым не происходит перезаписи значений полей
        (которые возможно установил пользователь)
        в уже существующих записях при повторных запусках loaddata.

    ---

    - Проблема::

        После первой загрузки фикстуры если далее изменить значение поля в модели
        и попробовать заново загрузить файл-фикстуру, то значение этого поля
        будет изменено обратно на то которое записано в файле-фикстуры.

    - Решение::

        Отфильтровать те записи из файла-фикстуры которые уже есть в БД,
        и записать получившиеся данные во временный файл, для последующей загрузки.

    https://code.djangoproject.com/ticket/33427

    ---

    - Так же расширение команды loaddata по умолчанию,
    функционалом (флаг --check_fields) фильтрации
    уже существующих в бд записей в фикстуре
    и отслеживания актуальных полей в загружаемых моделях
    для того чтобы при добавлении нового поля в бд,
    фикстура для этого поля успешно накатилась.

    - Проблема::

        При добавлении нового поля в модель и добавлении этого поля в фикстуру с каким то значением,
        скрипт не понимает какое поле новое и нужно ли на него накатывать значение из фикстуры
        или это приведёт к перезаписи данных пользователя.

    - Решение::

        Добавить модель для сохранения актуальных полей для каждой модели.

    ---

    - Поведение `--check_fields` при разных кейсах::

        - Кейс 1. (таблица приложения пустая и ModelFieldHistory пустой)::
            Фикстура устанавливаеться в таблицу приложения без фильтрации
            и в ModelFieldHistory создается запись с названием этой таблицы и полями из этой таблицы.

        - Кейс 2. (таблица приложения НЕ пустая и ModelFieldHistory пустой)::
            Фикстура полностью пропускается
            и в ModelFieldHistory создается запись с названием этой таблицы и полями из этой таблицы.

        - Кейс 3. (таблица приложения НЕ пустая и ModelFieldHistory НЕ пустой)::
            Из фикстуры устанавливаются только новые записи или только новые поля в существующих записях,
            поля которых ещё нет в ModelFieldHistory.
    """

    def add_arguments(self, parser) -> None:
        super().add_arguments(parser)

        # Создаем взаимноисключающую группу,
        # можно будет использовать только один из параметров одновременно
        group = parser.add_mutually_exclusive_group(required=False)

        group.add_argument(
            '--insert_only', action='store_true', default=False, help='', dest='insert_only'
        )
        group.add_argument(
            '--check_fields', action='store_true', default=False, help='', dest='check_fields'
        )
        parser.add_argument('--debug', action='store_true', default=False, help='', dest='debug')

    def handle(self, *fixture_labels: tuple[str, ...], **options) -> None:
        self.insert_only = options['insert_only']
        self.check_fields = options['check_fields']
        self.debug = options['debug']

        super().handle(*fixture_labels, **options)

    def loaddata(self, fixture_labels: tuple[str, ...]) -> None:
        self.serialization_formats = serializers.get_public_serializer_formats()

        fixture_labels = self._keep_windows_compatibility(fixture_labels)

        temp_file_names = []
        try:
            if self.insert_only:
                temp_file_names = self._fixture_labels_processing(
                    fixture_labels, self._filter_exists_db_record
                )
            elif self.check_fields:
                temp_file_names = self._fixture_labels_processing(
                    fixture_labels, self._filter_old_fields_in_exists_db_record
                )

            # Передать имена файлов на фактическую загрузку данных (родительская функциональность)
            if self.insert_only or self.check_fields:
                super().loaddata(temp_file_names)
            else:
                super().loaddata(fixture_labels)
        except Exception as exc:
            # NOTE(Ars): При отсутствии полей в модели из фикстуры райсит:
            # <class 'django.core.serializers.base.DeserializationError'>
            logger.warning('Что-то пошло не так: %s \n %s', type(exc), exc)
        finally:
            if self.insert_only or self.check_fields:
                for file_name in temp_file_names:
                    os.remove(file_name)

    def _fixture_labels_processing(
        self, fixture_labels: tuple[str, ...], filter_func: Callable
    ) -> list[str]:
        """
        Вызывает процесс фильтрации и создания временных файлов с отфильтрованными данными.
        """
        temp_file_names = []

        for file_name in fixture_labels:
            json_records = self._read_source_file(file_name)

            if not json_records:
                if self.debug:
                    logger.info(
                        'Файл: "%s" будет пропущен, потому что в нём нет ни одной записи.', file_name
                    )
                continue

            filtered_json_records = filter_func(json_records)

            if not filtered_json_records:
                if self.debug:
                    logger.info(
                        'Файл: "%s" будет пропущен, потому что в нём '
                        'содержаться только записи которые уже есть в БД.',
                        file_name,
                    )
                continue

            file_name_temp = self._write_temp_file(file_name, filtered_json_records)

            temp_file_names.append(file_name_temp)

        return temp_file_names

    @staticmethod
    def _filter_exists_db_record(json_records: RecordsType) -> RecordsType:
        """
        Фильтрует записи, которые уже записаны в бд.
        """
        # NOTE(Ars): возможно было бы эффективнее пройтись по json,
        # собрать все model поля с их pk и за один запрос к бд
        # вычислить какие pk уже присутствуют в бд,
        # затем за повторный проход json, оставить только необходимые записи

        return list(
            filter(
                lambda json_record: (
                    not apps.get_model(*json_record['model'].split('.'))
                    .objects.filter(pk=json_record['pk'])
                    .exists()
                ),
                json_records,
            )
        )

    def _filter_old_fields_in_exists_db_record(self, json_records: RecordsType) -> RecordsType:
        """
        Фильтрует записи, которые уже записаны в бд,
        только в том случае, если не были добавлены новые поля в модель.
        Если новые поля были добавлены в модель то, оставляет в записи только новые поля.
        """
        filtered_json_records = []
        records_info = []

        # NOTE(Ars): До конца не понятно,
        # должны ли действия create/update ModelFieldHistory быть атомарными.
        with transaction.atomic():
            for json_record in json_records:
                #
                model_class = apps.get_model(*json_record['model'].split('.'))
                record = get_object_or_none(model_class, pk=json_record['pk'])

                model_history, model_history_created = self._get_or_create_model_history(
                    json_record['model'], model_class
                )

                if model_history_created and self.debug:
                    logger.info('ModelFieldHistory created: %s', model_history)

                if record:
                    if self.debug:
                        logger.info('record exists: %s', record)

                    if model_history_created:
                        logger.warning(
                            'В рамках этого запуска, модель: "%s" ещё не записана в ModelFieldHistory'
                            ' а запись относящаяся к модели: "%s" уже находиться в бд,'
                            ' поэтому запись в бд не будет перезаписана данными из фикстуры,'
                            ' но запись в ModelFieldHistory для модели "%s" будет создана.',
                            *[json_record['model']] * 3,
                        )
                        continue

                    new_fields, old_fields = self._calculate_new_and_old_fields(
                        json_record, model_history
                    )

                    records_info.append({'model_history': model_history, 'new_fields': new_fields})

                    if new_fields:
                        fields_data = self._get_record_data_by_fields(
                            json_record, record, new_fields, old_fields
                        )
                        # Записываем в бд только значения новых полей из json_record,
                        # другие поля игнорируем т.к.
                        # они потенциально могут быть изменененными пользователем.
                        filtered_json_records.append(
                            {
                                'model': json_record['model'],
                                'pk': json_record['pk'],
                                'fields': fields_data,  # same .update()
                            }
                        )
                else:
                    if self.debug:
                        logger.info('record does not exists: %s %s', model_class, json_record['pk'])

                    filtered_json_records.append(json_record)

            self._update_models_history(records_info)

        if self.debug:
            logger.info('filtered_json_records: %s', filtered_json_records)

        return filtered_json_records

    @classmethod
    def _get_or_create_model_history(
        cls, model: str, model_class: type[models.Model]
    ) -> tuple[ModelFieldHistory, bool]:
        """
        Возвращает запись из ModelFieldHistory.
        """
        field_names = tuple(field.name for field in model_class._meta.get_fields())

        model_history, model_history_created = cls._create_or_get_cached_model_history(
            model, field_names
        )

        # XXX(Ars): Хак для того чтобы переопределить булевый флаг
        # который кэшируется в _create_or_get_cached_model_history после создания записи в бд.
        if cls._create_or_get_cached_model_history.was_cached:
            # NOTE(Ars): если было попадание в кэш, значит запись в бд не была создана и это not created
            model_history_created = False

        return model_history, model_history_created

    @staticmethod
    @cache_with_status
    def _create_or_get_cached_model_history(
        model: str, field_names: tuple[str, ...]
    ) -> tuple[ModelFieldHistory, bool]:
        """
        Создаёт запись в ModelFieldHistory с полями из django Model
        для модели из фикстуры если запись для этой модели ещё не создана.
        """
        return ModelFieldHistory.objects.get_or_create(
            model=model, defaults={'fields': list(field_names)}
        )

    @staticmethod
    @transaction.atomic
    def _update_models_history(records_info: RecordsInfoType) -> None:
        # TODO(Ars): Это будет большая проблема
        # если записи относящиеся к одной таблице окажутся в разных файлах фикстур..
        # после корректной обработки записей из первого файла,
        # для второго файла в бд уже будут добавлены new_fields
        for record_info in records_info:
            if record_info['new_fields']:
                # Если новые поля есть, добавляем их к полям в истории модели
                record_info['model_history'].fields.extend(record_info['new_fields'])
                record_info['model_history'].save(update_fields=['fields'])

    @staticmethod
    def _get_record_data_by_fields(
        json_record: RecordsType,
        record: type[models.Model],
        new_fields: list[str],
        old_fields: list[str],
    ) -> dict:
        """
        Формирует данные которые будут записаны во временный файл фикстуры по принципу,
        все новые пары из исходной фикстуры и все старые пары из записи в бд.
        """
        # XXX(Ars): WTF.. Если в фикстуре не указать поле которое уже есть в бд,
        # то оно будет перезаписано значением из параметра default из поля в модели..
        # Поэтому приходиться формировать json_record с учётом значений полей из бд.

        new_items = {field: json_record['fields'][field] for field in new_fields}
        old_items = better_model_to_dict(record, old_fields)
        cleaned_old_items = transform_payload(old_items)

        # print('new_fields:', new_fields)
        # print('old_fields:', old_fields)
        # print('new_items:', new_items)
        # print('old_items:', old_items)
        # print('cleaned_old_items:', cleaned_old_items)

        return new_items | cleaned_old_items  # same .update()

    def _calculate_new_and_old_fields(
        self, json_record: RecordsType, model_history: ModelFieldHistory
    ) -> tuple[list[str], list[str]]:
        """
        Определяет какие поля новые (которых ещё нету в записи ModelFieldHistory)
        и какие поля старые (которые уже есть в записи ModelFieldHistory) и возвращает их.
        """
        # Если запись уже есть в бд, нужно узнать,
        # появились ли новые поля в фикстуре относительно полей в истории модели
        json_record_field_names = list(json_record['fields'].keys())

        # Находим новые поля которых ещё нету в записи ModelFieldHistory
        set_json_record_field_names = set(json_record_field_names)
        set_model_history_fields = set(model_history.fields)

        new_fields = list(set_json_record_field_names.difference(set_model_history_fields))
        old_fields = list(set_json_record_field_names.intersection(set_model_history_fields))

        if self.debug:
            logger.info('json_record_field_names: %s', json_record_field_names)
            logger.info('model_history.fields: %s', model_history.fields)
            logger.info('new_fields: %s', new_fields)
            logger.info('old_fields: %s', old_fields)

        return new_fields, old_fields

    def _read_source_file(self, file_name: str) -> RecordsType:
        """
        Читает исходный файл с расширениями из compression_formats с диска
        """
        for fixture_file, _, _ in self.find_fixtures(file_name):
            #
            _, _, cmp_fmt = self.parse_name(os.path.basename(fixture_file))
            open_method, mode = self.compression_formats[cmp_fmt]

        with open_method(fixture_file, mode) as file:
            return json.load(file)

    def _write_temp_file(self, file_name: str, json_records: RecordsType) -> str:
        """
        Создает временный ser_fmt-файл на диске
        """
        name, ser_fmt, _ = self.parse_name(os.path.basename(file_name))
        file_name_temp = f'{name}_temporary_file.{ser_fmt}'

        with open(file_name_temp, 'w', encoding='utf-8') as json_file_temp:
            json.dump(json_records, json_file_temp)

        return file_name_temp

    @staticmethod
    def _keep_windows_compatibility(fixture_labels: tuple[str, ...]) -> tuple[str, ...]:
        """
        Ищет все .json файлы в директории если указан знак *
        *.json syntax: https://stackoverflow.com/a/2229073/19276507
        """
        if sys.platform == 'win32':
            # Ищем все JSON файлы в указанной директории
            temp_fixture_labels = []
            for fixture_label in fixture_labels:
                #
                files = glob.glob(fixture_label)
                temp_fixture_labels.extend(files)

            fixture_labels = tuple(temp_fixture_labels)

        return fixture_labels
