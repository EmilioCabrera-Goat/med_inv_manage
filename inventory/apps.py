from django.apps import AppConfig


class InventoryConfig(AppConfig):
    name = 'inventory'

class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    def ready(self):
        import inventory.signals
        