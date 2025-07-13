from django.apps import AppConfig


class AppUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'StarInTheKitchen.app_users'

    def ready(self):
        import StarInTheKitchen.app_users.signals
