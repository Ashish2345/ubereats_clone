from django.apps import AppConfig


class TestingMultipleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'testing_multiple'
