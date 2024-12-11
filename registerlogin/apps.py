from django.apps import AppConfig


class RegisterloginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'registerlogin'
    verbose_name='perfiles'

    def ready(self):
        import registerlogin.signals