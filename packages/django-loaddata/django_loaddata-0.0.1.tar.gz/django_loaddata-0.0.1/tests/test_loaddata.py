from unittest import skipIf

from django.core.management import call_command
from django.db import connection, models
from django.db.migrations.recorder import MigrationRecorder
from django_test_migrations.contrib.unittest_case import MigratorTestCase

from django_loaddata.management.commands.loaddata import Command as LoadDataCommand
from django_loaddata.models import ModelFieldHistory
from django_loaddata.utils import not_in_cmd
from tests.models import LoadDataSecondTestModel, LoadDataTestModel


@skipIf(
    not_in_cmd(
        (
            'tests.test_loaddata.TestLoadDataCmd.',
            'tests/test_loaddata.py::TestLoadDataCmd::',
        )
    ),
    'Не работает если запустить класс целиком, работает ок если запускать тесты по отдельности.',
)
class TestLoadDataCmd(MigratorTestCase):
    """
    This class is used to test direct migrations.

    https://stackoverflow.com/questions/42786734/how-to-register-django-models-that-are-only-used-in-tests
    https://stackoverflow.com/a/57897422/19276507
    """

    migrate_from = ('tests', '0001_initial')
    migrate_to = ('tests', '0002_loaddatasecondtestmodel_field2_and_more')

    loaddata_debug = False

    def prepare(self):
        """
        Prepare some data before the migration.
        """
        self._determine_check_fields()

        FakeLoadDataTestModel = self.old_state.apps.get_model('tests', 'LoadDataTestModel')  # noqa: N806
        FakeLoadDataSecondTestModel = self.old_state.apps.get_model(  # noqa: N806
            'tests', 'LoadDataSecondTestModel'
        )
        django_migrations = MigrationRecorder(connection).Migration

        self.assertEqual(
            [record.name for record in django_migrations.objects.filter(app='tests')],
            ['0001_initial'],
        )
        self.assertEqual(
            [x.name for x in FakeLoadDataTestModel._meta.get_fields()],
            ['created_at', 'updated_at', 'id', 'field1'],
        )
        self.assertIsNone(FakeLoadDataTestModel.objects.first())
        self.assertEqual(
            [x.name for x in FakeLoadDataSecondTestModel._meta.get_fields()], ['id', 'field3']
        )
        self.assertIsNone(FakeLoadDataSecondTestModel.objects.first())

        call_command(
            # 'loaddata',
            # Передаю экземпляр класса команды
            # для того чтобы вызвать переопределенный loaddata а не родительский
            LoadDataCommand(),
            './tests/test_loaddata1.json',
            check_fields=self.check_fields,  # dest
            debug=self.loaddata_debug,  # dest
        )

        self.assertEqual(
            [record.name for record in django_migrations.objects.filter(app='tests')],
            ['0001_initial'],
        )
        self.assertEqual(
            [x.name for x in FakeLoadDataTestModel._meta.get_fields()],
            ['created_at', 'updated_at', 'id', 'field1'],
        )
        self.assertEqual(
            [
                (record.field1, getattr(record, 'field2', None))
                for record in FakeLoadDataTestModel.objects.all()
            ],
            [('field1_first', None), ('field1_second', None)],
        )
        self.assertEqual(
            [x.name for x in FakeLoadDataSecondTestModel._meta.get_fields()], ['id', 'field3']
        )
        self.assertEqual(
            [
                (record.field3, getattr(record, 'field4', None))
                for record in FakeLoadDataSecondTestModel.objects.all()
            ],
            [('field3_first', None), ('field3_second', None)],
        )

        FakeLoadDataTestModel.objects.filter(pk='e32beb7f-8ef0-4d31-82c8-c273d404ccc3').update(
            field1='field1_first_updated'
        )
        FakeLoadDataTestModel.objects.filter(pk='03f32933-c0a9-4d3f-b95c-a635687ed561').update(
            field1='field1_second_updated'
        )
        FakeLoadDataSecondTestModel.objects.filter(pk='257e97de-ac49-45b0-bd77-2ed02e66e250').update(
            field3='field3_first_updated'
        )
        FakeLoadDataSecondTestModel.objects.filter(pk='0224bc79-8342-4199-ac47-56e637ce7670').update(
            field3='field3_second_updated'
        )

    def _determine_check_fields(self):
        called_test_method_name = self.id().rsplit('.', 1)[-1]
        if called_test_method_name == 'test_with_check_fields_flag':
            self.check_fields = True
        elif (
            called_test_method_name == 'test_without_check_fields_flag'
            or called_test_method_name == 'test_with_check_fields_flag_if_fixture_records_exists'
        ):
            self.check_fields = False
        else:
            self.check_fields = True

    @staticmethod
    def _apply_hack_to_model():
        # XXX(Ars): Хак для динамического добавления поля в модель,
        # классическое присваивание CharField в атрибут не сработает,
        # потому что после инициализации модели оно превращается в DeferredAttribute объект.
        field2 = models.CharField(max_length=254, blank=True)
        field2.contribute_to_class(LoadDataTestModel, 'field2')
        field4 = models.CharField(max_length=254, blank=True)
        field4.contribute_to_class(LoadDataSecondTestModel, 'field4')

    def test_with_check_fields_flag(self):
        """
        Run the test itself.
        """
        self._apply_hack_to_model()

        FakeLoadDataTestModel = self.new_state.apps.get_model('tests', 'LoadDataTestModel')  # noqa: N806
        FakeLoadDataSecondTestModel = self.new_state.apps.get_model(  # noqa: N806
            'tests', 'LoadDataSecondTestModel'
        )
        django_migrations = MigrationRecorder(connection).Migration

        self.assertEqual(
            [record.name for record in django_migrations.objects.filter(app='tests')],
            ['0001_initial', '0002_loaddatasecondtestmodel_field2_and_more'],
        )
        self.assertEqual(
            [x.name for x in FakeLoadDataTestModel._meta.get_fields()],
            ['created_at', 'updated_at', 'id', 'field1', 'field2'],
        )
        self.assertEqual(
            [
                (record.field1, getattr(record, 'field2', None))
                for record in FakeLoadDataTestModel.objects.all()
            ],
            [('field1_first_updated', ''), ('field1_second_updated', '')],
        )
        self.assertEqual(
            [x.name for x in FakeLoadDataSecondTestModel._meta.get_fields()], ['id', 'field3', 'field4']
        )
        self.assertEqual(
            [
                (record.field3, getattr(record, 'field4', None))
                for record in FakeLoadDataSecondTestModel.objects.all()
            ],
            [('field3_first_updated', ''), ('field3_second_updated', '')],
        )

        call_command(
            LoadDataCommand(),
            './tests/test_loaddata2.json',
            check_fields=self.check_fields,
            debug=self.loaddata_debug,
        )

        self.assertEqual(
            [record.name for record in django_migrations.objects.filter(app='tests')],
            ['0001_initial', '0002_loaddatasecondtestmodel_field2_and_more'],
        )
        self.assertEqual(
            [x.name for x in FakeLoadDataTestModel._meta.get_fields()],
            ['created_at', 'updated_at', 'id', 'field1', 'field2'],
        )
        self.assertEqual(
            [
                (record.field1, getattr(record, 'field2', None))
                for record in FakeLoadDataTestModel.objects.all()
            ],
            [('field1_first_updated', 'field2_first'), ('field1_second_updated', 'field2_second')],
        )
        self.assertEqual(
            [x.name for x in FakeLoadDataSecondTestModel._meta.get_fields()], ['id', 'field3', 'field4']
        )
        self.assertEqual(
            [
                (record.field3, getattr(record, 'field4', None))
                for record in FakeLoadDataSecondTestModel.objects.all()
            ],
            [('field3_first_updated', 'field4_first'), ('field3_second_updated', 'field4_second')],
        )

    def test_without_check_fields_flag(self):
        """
        Run the test itself.
        """
        self._apply_hack_to_model()

        FakeLoadDataTestModel = self.new_state.apps.get_model('tests', 'LoadDataTestModel')  # noqa: N806
        FakeLoadDataSecondTestModel = self.new_state.apps.get_model(  # noqa: N806
            'tests', 'LoadDataSecondTestModel'
        )
        django_migrations = MigrationRecorder(connection).Migration

        self.assertEqual(
            [record.name for record in django_migrations.objects.filter(app='tests')],
            ['0001_initial', '0002_loaddatasecondtestmodel_field2_and_more'],
        )
        self.assertEqual(
            [x.name for x in FakeLoadDataTestModel._meta.get_fields()],
            ['created_at', 'updated_at', 'id', 'field1', 'field2'],
        )
        self.assertEqual(
            [
                (record.field1, getattr(record, 'field2', None))
                for record in FakeLoadDataTestModel.objects.all()
            ],
            [('field1_first_updated', ''), ('field1_second_updated', '')],
        )
        self.assertEqual(
            [x.name for x in FakeLoadDataSecondTestModel._meta.get_fields()], ['id', 'field3', 'field4']
        )
        self.assertEqual(
            [
                (record.field3, getattr(record, 'field4', None))
                for record in FakeLoadDataSecondTestModel.objects.all()
            ],
            [('field3_first_updated', ''), ('field3_second_updated', '')],
        )

        call_command(
            LoadDataCommand(),
            './tests/test_loaddata2.json',
            check_fields=self.check_fields,
            debug=self.loaddata_debug,
        )

        self.assertEqual(
            [record.name for record in django_migrations.objects.filter(app='tests')],
            ['0001_initial', '0002_loaddatasecondtestmodel_field2_and_more'],
        )
        self.assertEqual(
            [x.name for x in FakeLoadDataTestModel._meta.get_fields()],
            ['created_at', 'updated_at', 'id', 'field1', 'field2'],
        )
        self.assertEqual(
            [
                (record.field1, getattr(record, 'field2', None))
                for record in FakeLoadDataTestModel.objects.all()
            ],
            [('field1_first', 'field2_first'), ('field1_second', 'field2_second')],
        )
        self.assertEqual(
            [x.name for x in FakeLoadDataSecondTestModel._meta.get_fields()], ['id', 'field3', 'field4']
        )
        self.assertEqual(
            [
                (record.field3, getattr(record, 'field4', None))
                for record in FakeLoadDataSecondTestModel.objects.all()
            ],
            [('field3_first', 'field4_first'), ('field3_second', 'field4_second')],
        )

    def test_with_check_fields_flag_if_fixture_records_exists(self):
        """
        Run the test itself.
        """
        self._apply_hack_to_model()

        FakeLoadDataTestModel = self.new_state.apps.get_model('tests', 'LoadDataTestModel')  # noqa: N806
        FakeLoadDataSecondTestModel = self.new_state.apps.get_model(  # noqa: N806
            'tests', 'LoadDataSecondTestModel'
        )
        django_migrations = MigrationRecorder(connection).Migration

        self.assertEqual(
            [record.name for record in django_migrations.objects.filter(app='tests')],
            ['0001_initial', '0002_loaddatasecondtestmodel_field2_and_more'],
        )
        self.assertEqual(
            [x.name for x in FakeLoadDataTestModel._meta.get_fields()],
            ['created_at', 'updated_at', 'id', 'field1', 'field2'],
        )
        self.assertEqual(
            [
                (record.field1, getattr(record, 'field2', None))
                for record in FakeLoadDataTestModel.objects.all()
            ],
            [('field1_first_updated', ''), ('field1_second_updated', '')],
        )
        self.assertEqual(
            [x.name for x in FakeLoadDataSecondTestModel._meta.get_fields()], ['id', 'field3', 'field4']
        )
        self.assertEqual(
            [
                (record.field3, getattr(record, 'field4', None))
                for record in FakeLoadDataSecondTestModel.objects.all()
            ],
            [('field3_first_updated', ''), ('field3_second_updated', '')],
        )
        self.assertEqual(ModelFieldHistory.objects.count(), 0)

        call_command(
            LoadDataCommand(),
            './tests/test_loaddata2.json',
            check_fields=True,  # в prepare было False, принудительно делаем True
            debug=self.loaddata_debug,
        )

        self.assertEqual(
            [(record.model, record.fields) for record in ModelFieldHistory.objects.all()],
            [
                ('tests.loaddatatestmodel', ['created_at', 'updated_at', 'id', 'field1', 'field2']),
                ('tests.loaddatasecondtestmodel', ['id', 'field3', 'field4']),
            ],
        )
        self.assertEqual(
            [record.name for record in django_migrations.objects.filter(app='tests')],
            ['0001_initial', '0002_loaddatasecondtestmodel_field2_and_more'],
        )
        self.assertEqual(
            [x.name for x in FakeLoadDataTestModel._meta.get_fields()],
            ['created_at', 'updated_at', 'id', 'field1', 'field2'],
        )
        self.assertEqual(
            [
                (record.field1, getattr(record, 'field2', None))
                for record in FakeLoadDataTestModel.objects.all()
            ],
            [('field1_first_updated', ''), ('field1_second_updated', '')],
        )
        self.assertEqual(
            [x.name for x in FakeLoadDataSecondTestModel._meta.get_fields()], ['id', 'field3', 'field4']
        )
        self.assertEqual(
            [
                (record.field3, getattr(record, 'field4', None))
                for record in FakeLoadDataSecondTestModel.objects.all()
            ],
            [('field3_first_updated', ''), ('field3_second_updated', '')],
        )
